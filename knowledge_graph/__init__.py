"""Knowledge graph built from NER -> normalization -> RE results.

Nodes are medical concepts, merged across documents by their standard code
(ICD-10 / RxNorm) when normalization found one, otherwise by entity type plus
normalized surface text. Edges are relation triples aggregated over documents,
with counts, sources (model / rule) and example sentences.
"""
from knowledge_graph.extract import HybridRelationExtractor
from knowledge_graph.graph import KnowledgeGraph, node_key

__all__ = ["HybridRelationExtractor", "KnowledgeGraph", "node_key"]
