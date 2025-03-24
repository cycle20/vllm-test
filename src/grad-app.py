import argparse
import gradio as gr
import re
import sys
import RAGTools
from langchain_community.document_loaders import PyMuPDFLoader

openai_api_key = "EMPTY"
llmDefaultModel = r'neuralmagic/DeepSeek-R1-Distill-Llama-70B-quantized.w4a16'
llmBaseUrl = r'http://localhost:8000/v1'

embeddingModel = r'sentence-transformers/all-MiniLM-L6-v2'

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


def process_pdf(pdf_bytes, tools: RAGTools.RAGTools):
    if pdf_bytes is None:
        return None, None, None

    loader = PyMuPDFLoader(pdf_bytes)
    data = loader.load()

    texts = []
    for doc in tools.split(data):
        texts.append(doc.page_content)
    return texts


def ask_question(pdf_bytes, question):
    global openai_api_key
    global args

    tools = RAGTools.RAGTools()

    context = ""
    if pdf_bytes != None:
        chunks = process_pdf(pdf_bytes, tools)
        embeddings = tools.embed(chunks)
        tools.createIndex(embeddings)
        hits = tools.searchRelevant(question)
        context = "\n\n==========================\n\n".join([doc.page_content for doc in hits])

    answer = tools.sendQueryToOpenAI(context, question, llmModel = args.llm_model, apiKey = openai_api_key)
    answer = re.sub(r".*?</think>", "", answer, flags = re.DOTALL).strip()

    print(f"ANSWER: {answer}")

    return answer


interface = gr.Interface(
    fn=ask_question,
    inputs=[
        gr.File(label="Upload PDF (optional)"),
        gr.Textbox(label="Ask a question"),
    ],
    outputs="text",
    title="Ask questions about your PDF",
    description=f"Use {args.llm_model}  to answer your questions about the uploaded PDF document.",
)

interface.launch(server_port = 9090)
