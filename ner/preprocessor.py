"""Preprocessor module for Vietnamese Medical NER pipeline.

Responsibilities:
  1. Whitespace normalization (preserving medical content and symbols).
  2. Word & punctuation tokenization using regex `\\w+|[^\\w\\s]`.
     Punctuation is strictly decoupled from words so it never sticks to entities.
  3. Sentence-level chunking for long texts exceeding max_position_embeddings (258),
     never cutting mid-word and preserving exact document-level character offsets.
  4. Handling edge cases (empty strings, whitespace-only, punctuation-only).
"""
import re
from dataclasses import dataclass
from typing import List

from .config import MAX_SUBTOKENS_PER_CHUNK
from .logger import NERPipelineLogger, get_logger


@dataclass
class WordToken:
    """Represents a single word or punctuation token with character offsets."""
    text: str
    start_char: int
    end_char: int
    is_punct: bool

    def __repr__(self) -> str:
        return f"WordToken({self.text!r}, [{self.start_char}:{self.end_char}])"


@dataclass
class TextChunk:
    """Represents a chunk of tokens conforming to model length limits."""
    words: List[WordToken]
    start_char: int
    end_char: int
    text: str

    def __repr__(self) -> str:
        return f"TextChunk(tokens={len(self.words)}, [{self.start_char}:{self.end_char}])"


class TextPreprocessor:
    """Preprocesses Vietnamese medical text for token-classification inference."""

    SENTENCE_END_PUNCT = {".", "!", "?", ";", "\n"}
    CLAUSE_BREAK_PUNCT = {",", ":", "-", "–", "—"}

    def __init__(self, logger: NERPipelineLogger = None):
        self.logger = logger or get_logger()

    def normalize_whitespace(self, text: str) -> str:
        """Normalize whitespace without altering medical numbers, units, or symbols."""
        if not text:
            return ""
        text = text.replace("\u00a0", " ").replace("\t", " ")
        text = re.sub(r" {2,}", " ", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()

    def tokenize_words(self, text: str) -> List[WordToken]:
        """Tokenize text into words and separate punctuation tokens with exact character spans.

        Uses regex `\\w+|[^\\w\\s]` ensuring punctuation NEVER sticks to entities.
        Example: "đau dạ dày," -> ["đau", "dạ", "dày", ","]
        """
        tokens: List[WordToken] = []
        if not text:
            return tokens

        pattern = re.compile(r"\w+|[^\w\s]")
        for match in pattern.finditer(text):
            token_text = match.group()
            start_c = match.start()
            end_c = match.end()
            is_punct = not bool(re.match(r"^\w+$", token_text))
            tokens.append(
                WordToken(
                    text=token_text,
                    start_char=start_c,
                    end_char=end_c,
                    is_punct=is_punct,
                )
            )

        self.logger.debug(
            "PREPROCESS",
            f"Tokenized {len(tokens)} word tokens from input text length {len(text)}."
        )
        return tokens

    def chunk_tokens(
        self,
        tokens: List[WordToken],
        full_text: str,
        max_words_per_chunk: int = 120,
    ) -> List[TextChunk]:
        """Group word tokens into chunks safely within max subtoken limits.

        Performs sentence-level chunking:
          - Chunks at sentence endings ('.', '!', '?', ';', '\n')
          - If a single sentence exceeds max_words_per_chunk, splits at clause breaks
          - NEVER splits in the middle of a word token.
        Each chunk carries WordTokens with character offsets matching the full original text.
        """
        if not tokens:
            return []

        chunks: List[TextChunk] = []
        current_chunk_tokens: List[WordToken] = []

        i = 0
        n = len(tokens)

        while i < n:
            token = tokens[i]
            current_chunk_tokens.append(token)

            is_sentence_end = token.text in self.SENTENCE_END_PUNCT
            is_clause_break = token.text in self.CLAUSE_BREAK_PUNCT
            chunk_len = len(current_chunk_tokens)

            should_split = False

            if is_sentence_end and chunk_len >= 35:
                should_split = True
            elif is_sentence_end and chunk_len >= 15 and (i + 1 < n and n - i >= 15):
                should_split = True
            elif chunk_len >= max_words_per_chunk and is_clause_break:
                should_split = True
            elif chunk_len >= (max_words_per_chunk + 20):
                should_split = True
            elif i == n - 1:
                should_split = True

            if should_split and current_chunk_tokens:
                start_c = current_chunk_tokens[0].start_char
                end_c = current_chunk_tokens[-1].end_char
                chunk_slice_text = full_text[start_c:end_c]
                chunks.append(
                    TextChunk(
                        words=current_chunk_tokens,
                        start_char=start_c,
                        end_char=end_c,
                        text=chunk_slice_text,
                    )
                )
                current_chunk_tokens = []

            i += 1

        if current_chunk_tokens:
            start_c = current_chunk_tokens[0].start_char
            end_c = current_chunk_tokens[-1].end_char
            chunks.append(
                TextChunk(
                    words=current_chunk_tokens,
                    start_char=start_c,
                    end_char=end_c,
                    text=full_text[start_c:end_c],
                )
            )

        self.logger.info(
            "PREPROCESS",
            f"Segmented {len(tokens)} tokens into {len(chunks)} sentence chunks."
        )
        return chunks

        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()
