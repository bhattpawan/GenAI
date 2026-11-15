import ollama
import chromadb
import pymupdf


def chunk_text(text, chunk_size=500, overlap=100):
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

for page_num, page in enumerate(doc):
    text = page.get_text().strip()
    if not text:
        continue

    page_chunks = chunk_text(text)
    for chunk_idx, chunk in enumerate(page_chunks):
        chunk_info = {
            "page": page_num,
            "text": chunk,
            "chunk_index": chunk_idx,
            "chunk_id": f"doc_p{page_num}_c{chunk_idx}",
        }
        all_chunks.append(chunk_info)

print(all_chunks)
