from dotenv import load_dotenv
load_dotenv()
import os
from langchain_community.document_loaders import PyPDFLoader,TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

### Load PDFs and Chunk the Text

# Load PDF
# pdf_path = "example.pdf"  # Update with your PDF file path
# loader = PyPDFLoader(pdf_path)
path = "./RAG/risqi.txt"  # Update with your PDF file path
loader = TextLoader(path)
documents = loader.load()

# Split text into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
chunks = text_splitter.split_documents(documents)
# print(chunks[0])

### Embed and Store Data in Pinecone

from langchain_community.vectorstores import Pinecone
from langchain_openai import OpenAIEmbeddings
from pinecone import Pinecone, ServerlessSpec

# Initialize Pinecone

pc = Pinecone(
        api_key=os.environ.get("PINECONE_API_KEY")
    )

# get or create pinecone index
import time
index_name = "testing"  # change if desired
def create_pinecone_index(pc, index_name):
    existing_indexes = [index_info["name"] for index_info in pc.list_indexes()]
    if index_name not in existing_indexes:
        pc.create_index(
            name=index_name,
            dimension=3072,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        )
        while not pc.describe_index(index_name).status["ready"]:
            time.sleep(1)

    return pc.Index(index_name)
index = create_pinecone_index(pc, index_name)

# Define embedding model
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")  # Ensure it matches your index

# Store in Pinecone
from langchain_pinecone import PineconeVectorStore
# vector_store = PineconeVectorStore(index=index, embedding=embeddings)
# vector_store.add_documents(chunks)

# results = vector_store.similarity_search(
#     "What is Risqi location?",
#     k=2,
# )
# for res in results:
#     print(res.page_content)
#     print("----")

# get vector store from existing index
vector_store = PineconeVectorStore.from_existing_index(index_name, embeddings)

retriever = vector_store.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={"k": 2, "score_threshold": 0.5},
)
# print(retriever.invoke("Who is Risqi Ikhsani?"))

### USE LLM

from langchain_openai import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

# Initialize the Language Model
llm = ChatOpenAI(
    model_name="gpt-4o",
    temperature=0.7
)

# Initialize conversation memory
memory = ConversationBufferMemory(memory_key="chat_history", input_key='question', output_key='answer', return_messages=True)
# Create the RAG chain
qa_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    memory=memory,
    return_source_documents=True,
    verbose=True
)

# Example conversation
question = "Who is Risqi Ikhsani and what are his skills?"
result = qa_chain.invoke({"question": question})

# Print the response
print("\nQuestion:", question)
print("\nAnswer:", result["answer"])
print("\nSource Documents:")
for doc in result["source_documents"]:
    print("---")
    print(doc.page_content)


