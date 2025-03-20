from sentence_transformers import SentenceTransformer

fileName = 'test-results/Result-Intermediate-Text-Extraction-From-PDF.md'
# Load the model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# List of sentences
#sentences = ["This is an example sentence", "Each sentence is converted to an embedding"]

with open(fileName, 'r', encoding='utf-8') as file:
    sentences = [ file.read() ]

# Convert sentences to embeddings
embeddings = model.encode(sentences)

# Output the embeddings
print(len(embeddings[0]))

