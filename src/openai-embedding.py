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

llmDefaultModel = 'neuralmagic/DeepSeek-R1-Distill-Llama-70B-quantized.w4a16'
llmBaseUrl = 'http://localhost:8000/v1'

embeddingModel = 'sentence-transformers/all-MiniLM-L6-v2'
embeddingUrl = 'http://localhost:8001/v1'

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

print(len(embeddings.embed_query('What is TmAlphaFol?')))
print(len(embeddings.embed_query('What is TmAlphaFold?')))

# Client side log:

# (venv) c@dev.ei:/bigdisk/users/csongor/rag$ python src/openai-embedding.py
# 100%|██████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 23.82it/s]
# 384
#   0%|                                                                                                      | 0/1 [00:00<?, ?it/s]
# Traceback (most recent call last):
#   File "/bigdisk/users/csongor/rag/src/openai-embedding.py", line 75, in <module>
#     print(len(embeddings.embed_query('What is TmAlphaFold?')))
#   File "/usr/local/share/grad-app/venv/lib/python3.10/site-packages/langchain_openai/embeddings/base.py", line 629, in embed_query
#     return self.embed_documents([text])[0]
#   File "/usr/local/share/grad-app/venv/lib/python3.10/site-packages/langchain_openai/embeddings/base.py", line 588, in embed_documents
#     return self._get_len_safe_embeddings(texts, engine=engine)
#   File "/usr/local/share/grad-app/venv/lib/python3.10/site-packages/langchain_openai/embeddings/base.py", line 483, in _get_len_safe_embeddings
#     response = self.client.create(
#   File "/usr/local/share/grad-app/venv/lib/python3.10/site-packages/openai/resources/embeddings.py", line 128, in create
#     return self._post(
#   File "/usr/local/share/grad-app/venv/lib/python3.10/site-packages/openai/_base_client.py", line 1242, in post
#     return cast(ResponseT, self.request(cast_to, opts, stream=stream, stream_cls=stream_cls))
#   File "/usr/local/share/grad-app/venv/lib/python3.10/site-packages/openai/_base_client.py", line 919, in request
#     return self._request(
#   File "/usr/local/share/grad-app/venv/lib/python3.10/site-packages/openai/_base_client.py", line 1023, in _request
#     raise self._make_status_error_from_response(err.response) from None
# openai.BadRequestError: Error code: 400 - {'object': 'error', 'message': 'Token id 76636 is out of vocabulary', 'type': 'BadRequestError', 'param': None, 'code': 400}




# Server side log:

# INFO 03-24 09:11:27 logger.py:39] Received request embd-04a2f7dc15d343539b3d5a87401dd575-0: prompt: 'urban [unused369] [unused345] [unused75] bolts [unused36] [unused332] [unused29]', params: PoolingParams(additional_metadata=None), prompt_token_ids: [3923, 374, 350, 76, 19947, 37, 337, 30], lora_request: None, prompt_adapter_request: None.
# INFO 03-24 09:11:27 engine.py:280] Added request embd-04a2f7dc15d343539b3d5a87401dd575-0.
# INFO 03-24 09:11:27 metrics.py:455] Avg prompt throughput: 1.0 tokens/s, Avg generation throughput: 0.1 tokens/s, Running: 0 reqs, Swapped: 0 reqs, Pending: 0 reqs, GPU KV cache usage: 0.0%, CPU KV cache usage: 0.0%.
# INFO:     127.0.0.1:42580 - "POST /v1/embeddings HTTP/1.1" 200 OK
# INFO 03-24 09:11:27 logger.py:39] Received request embd-9e18e1c6f7474999992758effbd62ae8-0: prompt: 'urban [unused369] [unused345] [unused75] bolts [unused29]', params: PoolingParams(additional_metadata=None), prompt_token_ids: [3923, 374, 350, 76, 19947, 76636, 30], lora_request: None, prompt_adapter_request: None.
# INFO:     127.0.0.1:42580 - "POST /v1/embeddings HTTP/1.1" 400 Bad Request
# INFO 03-24 09:11:27 engine.py:298] Aborted request embd-9e18e1c6f7474999992758effbd62ae8-0.
# INFO 03-24 09:11:37 metrics.py:455] Avg prompt throughput: 0.0 tokens/s, Avg generation throughput: 0.0 tokens/s, Running: 0 reqs, Swapped: 0 reqs, Pending: 0 reqs, GPU KV cache usage: 0.0%, CPU KV cache usage: 0.0%.
