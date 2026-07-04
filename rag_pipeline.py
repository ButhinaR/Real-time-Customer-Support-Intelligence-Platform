import re
import pandas as pd
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer, CrossEncoder
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

def chunk_text(text, chunk_size=3, overlap=1):
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", str(text)) if s.strip()]
    chunks = []
    step = max(1, chunk_size - overlap)

    for i in range(0, len(sentences), step):
        chunk = " ".join(sentences[i:i + chunk_size]).strip()
        if chunk:
            chunks.append(chunk)

    return chunks

def rrf(rankings, k=60):
    scores = {}
    for ranking in rankings:
        for rank, doc_id in enumerate(ranking):
            scores[doc_id] = scores.get(doc_id, 0) + 1 / (k + rank + 1)
    return sorted(scores, key=scores.get, reverse=True)

def run_rag(input_path: str = "data/silver/validated_tweets.csv"):
    df = pd.read_csv(input_path).head(500)

    documents = []
    for _, row in df.iterrows():
        for chunk in chunk_text(row["text"]):
            documents.append({"doc_id": len(documents), "text": chunk})

    texts = [doc["text"] for doc in documents]

    embedding_model = SentenceTransformer("BAAI/bge-small-en-v1.5")
    vectors = embedding_model.encode(texts, show_progress_bar=True)

    qdrant = QdrantClient(":memory:")
    collection = "support_chunks"

    qdrant.create_collection(
        collection_name=collection,
        vectors_config=VectorParams(size=vectors.shape[1], distance=Distance.COSINE)
    )

    qdrant.upsert(
        collection_name=collection,
        points=[
            PointStruct(id=doc["doc_id"], vector=vectors[doc["doc_id"]].tolist(), payload={"text": doc["text"]})
            for doc in documents
        ]
    )

    bm25 = BM25Okapi([text.lower().split() for text in texts])
    query = "I forgot my password and cannot log in"

    vector_results = qdrant.query_points(
        collection_name=collection,
        query=embedding_model.encode(query).tolist(),
        limit=10
    ).points

    vector_ids = [r.id for r in vector_results]
    bm25_scores = bm25.get_scores(query.lower().split())
    bm25_ids = sorted(range(len(bm25_scores)), key=lambda i: bm25_scores[i], reverse=True)[:10]

    hybrid_ids = rrf([vector_ids, bm25_ids])[:5]
    retrieved_docs = [texts[i] for i in hybrid_ids]

    reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
    scores = reranker.predict([(query, doc) for doc in retrieved_docs])

    reranked = sorted(zip(retrieved_docs, scores), key=lambda x: x[1], reverse=True)

    for doc, score in reranked:
        print(score, doc[:200])

if __name__ == "__main__":
    run_rag()