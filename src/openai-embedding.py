#
# server side:
#
# $ echo $model
# neuralmagic/DeepSeek-R1-Distill-Llama-70B-quantized.w4a16
# (venv-vllm-cuda) quad-6:~$ vllm serve "$model" --gpu-memory-utilization 0.9 --max-model-len 9000  &> vllm_source/log.txt &
#
# OR for embedding:
#
# (venv-vllm-cuda) quad-6:~$ vllm serve "$model" --task embed --gpu-memory-utilization 0.9 --max-model-len 9000  &> vllm.log &
#
#
#
#
#
# NOTE: embedding does not working through OpenAI API calls:
# through API calls: similar errors: Token id 98588 is out of vocabulary.
# It cannot process "TmAlphaFold", only "TmAlphaFol"!!! is acceptable to the API.
# Input question was: "What is TmAlphaFold?"
# But it works with the SentenceTransformer module.
#
# serve the transformer:
#
# (venv-vllm-cuda) csongor@quad-6:~$ echo $model
# sentence-transformers/all-MiniLM-L6-v2
# (venv-vllm-cuda) csongor@quad-6:~$ vllm serve "$model" --port 8001  &> transformer.log &
#
#

import argparse
import pymupdf4llm
import faiss
import sys
from langchain_openai import OpenAIEmbeddings
from langchain_experimental.text_splitter import SemanticChunker
from langchain_text_splitters import CharacterTextSplitter
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_core.vectorstores import InMemoryVectorStore

llmDefaultModel = 'neuralmagic/DeepSeek-R1-Distill-Llama-70B-quantized.w4a16'
llmBaseUrl = 'http://localhost:8000/v1'

embeddingModel = 'sentence-transformers/all-MiniLM-L6-v2'
# embeddingUrl = 'http://localhost:8001/v1'

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

parser.add_argument('--embedding-url',
                    type=str,
                    default=embeddingUrl,
                    help=f'Embedding Base URL. Default: {embeddingUrl}')
parser.add_argument('--embedding-model',
                    type=str,
                    default=embeddingModel,
                    help=f'Model name for embedding used for vector database. Default: {embeddingModel}')


# Parse the arguments
args = parser.parse_args()

# md_text = pymupdf4llm.to_markdown(args.pdf_file)
# md_text = md_text[:3900]
fileName = 'Result-Intermediate-Text-Extraction-From-PDF.md'
with open(fileName, 'r', encoding='utf-8') as file:
    # sentences = [ file.read() ]
    md_text = file.read()

#loader = PyMuPDFLoader(file_path='gkac928.pdf')

from sentence_transformers import SentenceTransformer
sentences = ["This is an example sentence", "Each sentence is converted"]
sentences = [ "TmAlphaFold database: membrane localization and evaluation of AlphaFold2 predicted alpha-helical transmembrane protein structures" ]
sentences = [ "What is TmAlphaFold?" ]

model = SentenceTransformer(embeddingModel)
embeddings = model.encode(sentences)
print(embeddings)
print(sentences)
sys.exit()


# Set OpenAI's API key and API base to use vLLM's API server.
openai_api_key = "EMPTY"
embedding_api_base = args.embedding_url
embedding_model = args.embedding_model

llm_api_base = args.llm_url
llm_model = args.llm_model

embeddings = OpenAIEmbeddings(
    model=embedding_model,
    openai_api_key=openai_api_key,
    openai_api_base=embedding_api_base,
    show_progress_bar=True
)

# Chunks

def markDownChunker(markdown_document):
    headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
    ]

    markdown_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on = headers_to_split_on,
        strip_headers = False
    )
    md_header_splits = markdown_splitter.split_text(markdown_document)

    chunk_size = 250
    chunk_overlap = 30
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )

    # Split
    # splits = text_splitter.split_documents([markdown_document])
    splits = text_splitter.split_text(markdown_document)

    return splits

def semanticChunker(embeddings, docs):
    text_splitter = SemanticChunker(embeddings)
    docs = text_splitter.create_documents(docs)
    return docs


print(len(embeddings.embed_query('What is TmAlphaFol?')))
sys.exit()

#print(semanticChunker(embeddings, markDownChunker(md_text)))
data = loader.load()
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=256, chunk_overlap=20
)
chunks = text_splitter.split_documents(data)
for chunk in chunks:
    chunk.metadata.clear()
    print(embeddings.embed_query(chunk.page_content))
    print('=====================================')

sys.exit()



# result = embeddings.embed_query(md_text)
# print(len(result))
# print(result)

###########################################################xx

vectorstore = InMemoryVectorStore.from_texts(
    [md_text],
    embedding=embeddings,
)

# Use the vectorstore as a retriever
retriever = vectorstore.as_retriever()

# Retrieve the most similar text
retrieved_documents = retriever.invoke(question)

# show the retrieved document's content
print(retrieved_documents)
print(retrieved_documents[0].page_content)

sys.exit()


###########################################################xx

# print("Calling embed_query...")
# result = embeddings.embed_query(md_text)
# 
# print(embeddings)
# print("Vector -----------------")
# print(result)

#print("Storing into FAISS db...")


# index = faiss.IndexFlatL2(len(embeddings.embed_query(md_text)))
# 
# vector_store = FAISS(
#     embedding_function=embeddings,
#     index=index,
#     docstore=InMemoryDocstore(),
#     index_to_docstore_id={},
# )
# 
# vector_store.save_local("faiss_index")


###########################################################xx


# Create an OpenAI client to interact with the API server
client = OpenAI(
    api_key=openai_api_key,
    base_url=llm_api_base,
)

chat_completion = client.chat.completions.create(
    messages=[{
        "role": "system",
        "content": "You are a helpful assistant."
    }, {
        "role": "user",
        "content": f"Question: What is TmAlphaFold based on this text?\n\nContext: {md_text}"
    }],
    model=llm_model,
)

print("Chat completion results:")
print(chat_completion.choices[0].message.content)
