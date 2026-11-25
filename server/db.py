"""Lưu các văn bản đã phân tích và kết quả (JSONB trên PostgreSQL, JSON trên SQLite)."""
from datetime import datetime, timezone

from sqlalchemy import JSON, DateTime, Integer, String, Text, create_engine, func, select
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker


class Base(DeclarativeBase):
    pass


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True,
                                                 default=lambda: datetime.now(timezone.utc))
    source: Mapped[str] = mapped_column(String(32), default="user", index=True)  # user | seed
    external_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    text: Mapped[str] = mapped_column(Text)
    n_entities: Mapped[int] = mapped_column(Integer, default=0)
    n_relations: Mapped[int] = mapped_column(Integer, default=0)
    elapsed_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    result: Mapped[dict] = mapped_column(JSON().with_variant(JSONB(), "postgresql"))

    def summary(self):
        return {"id": self.id, "created_at": self.created_at.isoformat() if self.created_at else None,
                "source": self.source, "external_id": self.external_id, "text": self.text,
                "n_entities": self.n_entities, "n_relations": self.n_relations, "elapsed_ms": self.elapsed_ms}

    def full(self):
        return {**self.summary(), "result": self.result}


class Database:
    def __init__(self, url):
        kw = {"connect_args": {"check_same_thread": False}} if url.startswith("sqlite") else {"pool_pre_ping": True}
        self.engine = create_engine(url, **kw)
        self.Session = sessionmaker(self.engine, expire_on_commit=False)

    def create_all(self):
        Base.metadata.create_all(self.engine)

    def ping(self):
        try:
            with self.engine.connect() as c:
                c.exec_driver_sql("SELECT 1")
            return True
        except Exception:
            return False

    def add(self, result, source="user", external_id=None, elapsed_ms=None):
        doc = Document(source=source, external_id=external_id, text=result["text"], result=result,
                       n_entities=len(result.get("entities", [])), n_relations=len(result.get("relations", [])),
                       elapsed_ms=elapsed_ms)
        with self.Session() as s:
            s.add(doc)
            s.commit()
        return doc

    def add_many(self, items, source="seed"):
        """items: (external_id, result) — dùng khi nạp sẵn dữ liệu."""
        with self.Session() as s:
            s.add_all([Document(source=source, external_id=eid, text=r["text"], result=r,
                                n_entities=len(r.get("entities", [])), n_relations=len(r.get("relations", [])))
                       for eid, r in items])
            s.commit()

    def count(self, source=None):
        q = select(func.count(Document.id))
        if source:
            q = q.where(Document.source == source)
        with self.Session() as s:
            return s.scalar(q)

    def list(self, limit=20, offset=0, q=None, source=None):
        stmt = select(Document)
        if q:
            stmt = stmt.where(Document.text.ilike(f"%{q}%"))
        if source:
            stmt = stmt.where(Document.source == source)
        with self.Session() as s:
            total = s.scalar(select(func.count()).select_from(stmt.subquery()))
            rows = s.scalars(stmt.order_by(Document.id.desc()).limit(limit).offset(offset)).all()
        return total, rows

    def get(self, doc_id):
        with self.Session() as s:
            return s.get(Document, doc_id)

    def delete(self, doc_id):
        with self.Session() as s:
            doc = s.get(Document, doc_id)
            if doc is None:
                return False
            s.delete(doc)
            s.commit()
            return True

    def iter_results(self, batch=500):
        """(id, result) của mọi văn bản, theo thứ tự id — để dựng đồ thị tri thức."""
        last = 0
        with self.Session() as s:
            while True:
                rows = s.execute(select(Document.id, Document.result).where(Document.id > last)
                                 .order_by(Document.id).limit(batch)).all()
                if not rows:
                    return
                yield from rows
                last = rows[-1][0]
