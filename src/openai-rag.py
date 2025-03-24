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
import RAGTools
from openai import OpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.vectorstores import FAISS
from sentence_transformers import SentenceTransformer

llmDefaultModel = r'neuralmagic/DeepSeek-R1-Distill-Llama-70B-quantized.w4a16'
llmBaseUrl = r'http://localhost:8000/v1'

embeddingModel = r'sentence-transformers/all-MiniLM-L6-v2'

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

tools = RAGTools.RAGTools()
loader = PyMuPDFLoader(file_path='gkac928.pdf')
data = loader.load()

texts = []
for doc in tools.split(data):
    texts.append(doc.page_content)

embeddings = tools.embed(texts)
tools.createIndex(embeddings)
hits = tools.searchRelevant(question)

# Set OpenAI's API key and API base to use vLLM's API server.
openai_api_key = "EMPTY"

context = "\n\n==========================\n\n".join([doc.page_content for doc in hits])
print([context, question, args.llm_url, args.llm_model, openai_api_key])
answer = tools.sendQueryToOpenAI(context, question, llmModel = args.llm_model, apiKey = openai_api_key)

print(f'\n\nANSWER:\n\n{answer}')
