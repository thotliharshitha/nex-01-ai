from utils.embeddings import split_text

sample_text = """
Cloud Computing is a specialized form of distributed computing.
It provides on-demand access to computing resources.
Users pay only for the resources they consume.
Cloud offers scalability, flexibility, and cost savings.
""" * 50

chunks = split_text(sample_text)

print(f"Total Chunks: {len(chunks)}")

for i, chunk in enumerate(chunks, start=1):
    print(f"\n----- Chunk {i} -----")
    print(chunk[:150])