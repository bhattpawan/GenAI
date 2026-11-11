import ollama
import chromadb

client = chromadb.PersistentClient(path="./chroma_data")

collection = client.get_or_create_collection(
    name="de_docs", configuration={"hnsw": {"space": "cosine"}}
)

documents = [
    "ASP is calculated using sales divided by units.",
    "Average selling price is revenue per unit.",
    "How do I calculate monthly sales?",
    "PySpark is a Python API for Apache Spark.",
    "Spark is used for distributed data processing.",
]

ids = [f"doc_{i}" for i in range(len(documents))]

embeddings_response = ollama.embed(model="embeddinggemma", input=documents)

embeddings = embeddings_response.embeddings

collection.add(
    ids=ids,
    documents=documents,
    embeddings=embeddings,
    metadatas=[
        {"topic": "sales"},
        {"topic": "sales"},
        {"topic": "sales"},
        {"topic": "spark"},
        {"topic": "spark"},
    ],
)

print(f"Documents Stored: {collection.count()}")

query = "How is ASP calculated?"

query_response = ollama.embed(model="embeddinggemma", input=query)

query_embedding = query_response.embeddings[0]

results = collection.query(query_embeddings=[query_embedding], n_results=3)

print(results["documents"])
print(results["distances"])
