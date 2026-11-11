from ollama import embed

text = "The quick brown fox jumps over the lazy dog while the moon glows softly above the quiet meadow."

response = embed(model="embeddinggemma", input=text)

embeddings = response.embeddings[0]

print(f"Embedding Dimensions: {len(embeddings)}")
print(f"First 10 values: {embeddings[:10]}")
