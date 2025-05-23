#
# server side:
#
# $ echo $model
# neuralmagic/DeepSeek-R1-Distill-Llama-70B-quantized.w4a16
# (venv-vllm-cuda) quad-6:~$ vllm serve "$model" --gpu-memory-utilization 0.9 --max-model-len 9000  &> vllm_source/log.txt &
#
import faiss
import numpy
import sys
import datetime
from openai import OpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_text_splitters.base import TextSplitter
from langchain_community.vectorstores import FAISS
from sentence_transformers import SentenceTransformer

llmBaseUrl = r'http://localhost:8000/v1'
llmDefaultModel = r'neuralmagic/DeepSeek-R1-Distill-Llama-70B-quantized.w4a16'

def log(message: str):
    message = f"{datetime.datetime.now()}: {message}"
    print(message)

class RAGTools:

    def __init__(self, embeddingModel: str = 'sentence-transformers/all-MiniLM-L6-v2'):
        self.embeddingModel = embeddingModel
        self.sentenceTransformer = SentenceTransformer(embeddingModel)


    def split(self, text, splitter: TextSplitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=250)) -> list:
        self.chunks = splitter.split_documents(text)
        return self.chunks


    def embed(self, texts: list) -> list:
        return self.sentenceTransformer.encode(texts)


    def createIndex(self, embeddings: list):
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(numpy.array(embeddings))


    def searchRelevant(self, question: str, maxHitNumber: int = 3) -> list[str]:
        qEmbedding = self.sentenceTransformer.encode(question)

        distances, indices = self.index.search(numpy.array([ qEmbedding ]), k = maxHitNumber)
        log(f"Indicies of closest texts: {indices}")
        log(f"Distances: {distances}")

        searchResults = []
        for i in indices[0]:
            searchResults.append(self.chunks[i])
            # print(self.chunks[i])
            # print('============================================')

        return searchResults


    def sendQueryToOpenAI(self, question: str, context: str, /, llmUrl: str = llmBaseUrl, llmModel: str = llmDefaultModel, apiKey: str = "EMPTY") -> str:

        # Create an OpenAI client to interact with the API server
        client = OpenAI(
            api_key = apiKey,
            base_url = llmUrl,
        )

        contextContent = ""
        if len(context.strip()) > 0:
            contextContent = f"\n\nCONTEXT (or related document content):\n\n'{context.strip()}'"

        messageToLLM = f"QUESTION: \n'{question.strip()}'\nYour answer should be brief, maximum 3 sentences.{contextContent}"
        log(f"Message to LLM:\n{messageToLLM}")
        chat_completion = client.chat.completions.create(
            messages = [{
                "role": "system",
                "content": "You are a helpful assistant."
            }, {
                "role": "user",
                "content": messageToLLM
            }],
            model = llmModel,
        )

        # TODO: What if we have more choices?
        log(f"# OF CHOICES: {len(chat_completion.choices)}")
        response = chat_completion.choices[0].message.content
        log(f"Answer '{response}'")

        return chat_completion.choices[0].message.content
