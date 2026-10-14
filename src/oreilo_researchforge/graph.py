"""Explainable lightweight co-occurrence graph (not an ontology)."""
from collections import Counter
from itertools import combinations
import re
def build_graph(texts: list[str],max_nodes=40):
    counts=Counter()
    for text in texts:
        counts.update(re.findall(r'\b[A-Z][a-zA-Z]{3,}(?:\s+[A-Z][a-zA-Z]{3,})?\b',text))
    nodes=[x for x,_ in counts.most_common(max_nodes)]
    edges=Counter()
    for text in texts:
        present=sorted({x for x in nodes if x in text})
        for a,b in combinations(present,2):edges[(a,b)]+=1
    return {"nodes":[{"id":n,"mentions":counts[n]} for n in nodes],"edges":[{"source":a,"target":b,"weight":w} for (a,b),w in edges.items()],"note":"Co-occurrence is not evidence of a causal relationship."}
