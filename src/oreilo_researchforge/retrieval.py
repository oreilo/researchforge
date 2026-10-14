"""Local hybrid keyword retrieval, no vector service required."""
from collections import Counter
import math,re
from dataclasses import dataclass
@dataclass
class Chunk:
    id: str
    text: str
    source: str
    score: float = 0.0
def chunk_text(text: str,source: str,chunk_size=1200,overlap=150):
    if chunk_size<100 or overlap<0 or overlap>=chunk_size: raise ValueError('invalid chunk settings')
    out=[]; step=chunk_size-overlap
    for n,start in enumerate(range(0,len(text),step)):
        part=text[start:start+chunk_size]
        if part.strip(): out.append(Chunk(f'{source}:{n}',part,source))
        if start+chunk_size>=len(text): break
    return out
def tokens(text): return re.findall(r'[a-z0-9]{2,}',text.casefold())
def rank(query: str,chunks: list[Chunk],limit=8):
    if not chunks:return []
    query_terms=Counter(tokens(query)); n=len(chunks)
    df=Counter(t for c in chunks for t in set(tokens(c.text)))
    scored=[]
    for c in chunks:
        counts=Counter(tokens(c.text)); length=sum(counts.values()) or 1
        score=sum(math.log(1+(n-df[t]+0.5)/(df[t]+0.5))*((counts[t]*2.2)/(counts[t]+1.2*(0.25+0.75*length/200))) for t in query_terms if counts[t])
        scored.append(Chunk(c.id,c.text,c.source,round(score,6)))
    return sorted(scored,key=lambda x:-x.score)[:max(0,limit)]
