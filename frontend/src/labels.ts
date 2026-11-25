export const ENTITY_TYPES = ["CONDITION", "DRUG", "BODY_PART", "TEST", "PROCEDURE", "DOSAGE"] as const;

export const ENTITY_LABEL: Record<string, string> = {
  CONDITION: "Bệnh / triệu chứng",
  DRUG: "Thuốc",
  BODY_PART: "Bộ phận cơ thể",
  TEST: "Xét nghiệm",
  PROCEDURE: "Thủ thuật / điều trị",
  DOSAGE: "Liều dùng",
};

export const ENTITY_COLOR: Record<string, string> = {
  CONDITION: "#d9485f",
  DRUG: "#2b8a3e",
  BODY_PART: "#c77c02",
  TEST: "#6741d9",
  PROCEDURE: "#1c7ed6",
  DOSAGE: "#0b7285",
};

export const RELATIONS = ["located_at", "treated_by", "treated_by_procedure", "diagnosed_by", "has_dosage"] as const;

export const RELATION_LABEL: Record<string, string> = {
  located_at: "vị trí tại",
  treated_by: "điều trị bằng thuốc",
  treated_by_procedure: "điều trị bằng thủ thuật",
  diagnosed_by: "chẩn đoán bằng",
  has_dosage: "liều dùng",
};

export const METHOD_LABEL: Record<string, string> = {
  exact: "khớp chính xác",
  synonym: "từ đồng nghĩa",
  fuzzy: "khớp gần đúng",
  retrieval: "truy hồi",
  api: "RxNav API",
  alias: "bí danh",
};
