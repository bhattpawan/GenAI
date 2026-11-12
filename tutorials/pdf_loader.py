import ollama
import chromadb
import pymupdf


def chunk_text(text, chunk_size=500, overlap=50):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks


client = chromadb.PersistentClient(path="./chroma_data")

collection = client.get_or_create_collection(
    name="mydocs", configuration={"hnsw": {"space": "cosine"}}
)

doc = pymupdf.open("./docs/dummy_doc.pdf")

all_chunks = []
all_metadata = []
all_ids = []

for page_num, page in enumerate(doc):
    text = page.get_text().strip()
    if not text:
        continue

    page_chunks = chunk_text(text)
    for chunk_idx, chunk in enumerate(page_chunks):
        all_chunks.append(chunk)
        all_metadata.append({"source": "dummy_doc.pdf", "page": page_num + 1})
        all_ids.append(f"doc_p{page_num+1}_c{chunk_idx}")

print(f"Prepared {len(all_chunks)} chunks from the {len(doc)} pages.")

response = ollama.embed(model="embeddinggemma", input=all_chunks)

embeddings = response.embeddings

collection.upsert(
    ids=all_ids,
    documents=all_chunks,
    embeddings=embeddings,
    metadatas=all_metadata,
)

print(f"Stored {collection.count()} chunks in chromadb")

query = input("Enter your query:")

query_embedding = ollama.embed(model="embeddinggemma", input=query)["embeddings"]

results = collection.query(query_embeddings=query_embedding, n_results=3)

print(results["documents"])
print(results["distances"])
