#
# server side:
#
# $ echo $model
# neuralmagic/DeepSeek-R1-Distill-Llama-70B-quantized.w4a16
# (venv-vllm-cuda) quad-6:~$ vllm serve "$model" --gpu-memory-utilization 0.9 --max-model-len 9000  &> vllm_source/log.txt &
#
import argparse
import pymupdf4llm
import faiss
import numpy
import sys
from openai import OpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.vectorstores import FAISS
from sentence_transformers import SentenceTransformer

llmDefaultModel = 'neuralmagic/DeepSeek-R1-Distill-Llama-70B-quantized.w4a16'
llmBaseUrl = 'http://localhost:8000/v1'

embeddingModel = 'sentence-transformers/all-MiniLM-L6-v2'

question = 'What is TmAlphaFold?'


# Argument parser setup
parser = argparse.ArgumentParser(
    description='Embedding and inference for chat completions')
parser.add_argument('--llm-url',
                    type=str,
                    default=llmBaseUrl,
                    help=f'LLM Base URL. Default: {llmBaseUrl}')
parser.add_argument('--llm-model',
                    type=str,
                    default=llmDefaultModel,
                    help=f'Model name for the LLM (used for inferencing). Default: {llmDefaultModel}')
parser.add_argument('--embedding-model',
                    type=str,
                    default=embeddingModel,
                    help=f'Model name for embedding used for vector database. Default: {embeddingModel}')


# Parse the arguments
args = parser.parse_args()

# fileName = 'Result-Intermediate-Text-Extraction-From-PDF.md'
# with open(fileName, 'r', encoding='utf-8') as file:
#     # sentences = [ file.read() ]
#     md_text = file.read()

embeddingModel = args.embedding_model

loader = PyMuPDFLoader(file_path='gkac928.pdf')
data = loader.load()
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=250
)

# for doc in data:
#     print(doc.page_content)
# print("===================== END OF DOCUMENT ===========================================")

chunks = text_splitter.split_documents(data)

# sentences = [ "What is TmAlphaFold?" ]

model = SentenceTransformer(embeddingModel)
# embeddings = model.encode_multi_process(chunks, ...
embeddings = []
texts = []
for doc in chunks:
    texts.append(doc.page_content)

embeddings = model.encode(texts)

# for index in range(0, len(embeddings)):
#     print("\nEMBEDDIGNS: " + len(embeddings[index]).__str__() + "\n")
#     print(chunks[index].page_content + "\n")
#     print("===================================================")

# sys.exit()

###########################################################xx

dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(numpy.array(embeddings))

qEmbedding = model.encode(question)
distances, indices = index.search(numpy.array([ qEmbedding ]), k = 3)

print(f"Indicies of closest texts: {indices}")
print(f"Distances: {distances}")

searchResults = []
for i in indices[0]:
    searchResults.append(texts[i])
    print(texts[i])
    print('============================================')

###########################################################xx


# Set OpenAI's API key and API base to use vLLM's API server.
openai_api_key = "EMPTY"
llm_api_base = args.llm_url
llm_model = args.llm_model



# Create an OpenAI client to interact with the API server
client = OpenAI(
    api_key=openai_api_key,
    base_url=llm_api_base,
)

context = "\n===============================\n".join(searchResults)
chat_completion = client.chat.completions.create(
    messages=[{
        "role": "system",
        "content": "You are a helpful assistant."
    }, {
        "role": "user",
        "content": f"Question: {question}\n\nYour answer should be brief.\n\nContext:\n\n{context}"
    }],
    model=llm_model,
)

print("Chat completion results:")
print(chat_completion.choices[0].message.content)
