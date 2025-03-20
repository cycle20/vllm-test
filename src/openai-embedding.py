#
# server side:
#
# $ echo $model
# neuralmagic/DeepSeek-R1-Distill-Llama-70B-quantized.w4a16
# (venv-vllm-cuda) quad-6:~$ vllm serve "$model" --task embed --gpu-memory-utilization 0.9 --max-model-len 9000  &> vllm_source/log.txt &
#


import argparse
import pymupdf4llm
import faiss
import sys
from langchain_openai import OpenAIEmbeddings
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from langchain_core.vectorstores import InMemoryVectorStore

# Argument parser setup
parser = argparse.ArgumentParser(
    description='Embedding for chat completions')
parser.add_argument('--model-url',
                    type=str,
                    default='http://localhost:8000/v1',
                    help='Model URL')
parser.add_argument('-m',
                    '--model',
                    type=str,
                    required=True,
                    help='Model name for the chatbot')
parser.add_argument('-p',
                    '--pdf-file',
                    type=str,
                    required=True,
                    help='Path of input PDF file')


# Parse the arguments
args = parser.parse_args()

# Parse the arguments
args = parser.parse_args()

md_text = pymupdf4llm.to_markdown(args.pdf_file)
md_text = md_text[:3900]


# Set OpenAI's API key and API base to use vLLM's API server.
openai_api_key = "EMPTY"
openai_api_base = args.model_url


embeddings = OpenAIEmbeddings(
    model=args.model,
    openai_api_key=openai_api_key,
    openai_api_base=openai_api_base,
    show_progress_bar=True
)



# vectorstore = InMemoryVectorStore.from_texts(
#     [md_text],
#     embedding=embeddings,
# )
# 
# # Use the vectorstore as a retriever
# retriever = vectorstore.as_retriever()
# 
# # Retrieve the most similar text
# retrieved_documents = retriever.invoke("What is TmAlphaFold?")
# 
# # show the retrieved document's content
# print(retrieved_documents[0].page_content)
# 
# 
# sys.exit()


###########################################################xx

# print("Calling embed_query...")
# result = embeddings.embed_query(md_text)
# 
# print(embeddings)
# print("Vector -----------------")
# print(result)

#print("Storing into FAISS db...")


index = faiss.IndexFlatL2(len(embeddings.embed_query(md_text)))

vector_store = FAISS(
    embedding_function=embeddings,
    index=index,
    docstore=InMemoryDocstore(),
    index_to_docstore_id={},
)

vector_store.save_local("faiss_index")

