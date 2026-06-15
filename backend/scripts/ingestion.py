import os
import glob
import json
import uuid
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
import chromadb

CHROMA_HOST = os.getenv("CHROMA_HOST", "chromadb")
CHROMA_PORT = int(os.getenv("CHROMA_PORT", 8000))
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def ingest_pdfs():
    if not OPENAI_API_KEY or OPENAI_API_KEY == "your-openai-api-key-here":
        print("Erro: OPENAI_API_KEY não configurada no .env. Impossível vetorizar os documentos.")
        return

    path = os.path.join(os.path.dirname(__file__), '../data/artigos')
    pdf_files = glob.glob(os.path.join(path, '*.pdf'))
    
    if not pdf_files:
        print(f"Nenhum arquivo PDF encontrado na pasta: {path}")
        return

    print("Iniciando PDR (Parent Document Retrieval) chunking dos manuais...")
    documents = []
    for file in pdf_files:
        print(f"Processando: {os.path.basename(file)}")
        try:
            loader = PyPDFLoader(file)
            docs = loader.load()
            documents.extend(docs)
        except Exception as e:
            print(f"Erro ao ler {file}: {e}")

    # PDR Configuration
    parent_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
    child_splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=50)

    parents = parent_splitter.split_documents(documents)
    
    parent_docs_dict = {}
    child_docs = []
    
    for parent in parents:
        doc_id = str(uuid.uuid4())
        
        # Save parent text and metadata to our dict
        parent_docs_dict[doc_id] = {
            "page_content": parent.page_content,
            "metadata": parent.metadata
        }
        
        # Create children for this parent
        children = child_splitter.split_documents([parent])
        for child in children:
            child.metadata["doc_id"] = doc_id
            child_docs.append(child)
            
    parent_store_path = os.path.join(os.path.dirname(__file__), '../data/parent_docs.json')
    with open(parent_store_path, 'w', encoding='utf-8') as f:
        json.dump(parent_docs_dict, f, ensure_ascii=False, indent=2)
        
    print(f"Total de Parent Docs (grandes): {len(parents)}")
    print(f"Total de Child Docs (pequenos): {len(child_docs)}")
    print("Iniciando processo de embedding dos Child Docs com text-embedding-3-small no ChromaDB...")

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small", openai_api_key=OPENAI_API_KEY)
    
    try:
        chroma_client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)
        # Clear existing collection if testing PDR from scratch (optional, but good for fresh state)
        try:
            chroma_client.delete_collection("propellers")
        except:
            pass
            
        vectorstore = Chroma(client=chroma_client, embedding_function=embeddings, collection_name="propellers")
        
        batch_size = 100
        for i in range(0, len(child_docs), batch_size):
            batch = child_docs[i:i+batch_size]
            vectorstore.add_documents(batch)
            print(f"Enviado {i + len(batch)} de {len(child_docs)} chunks.")

        print("\nIngestão PDR finalizada com sucesso! A base vetorial do RAG está pronta.")
    except Exception as e:
        print(f"Erro fatal na comunicação com ChromaDB ou OpenAI: {e}")

if __name__ == "__main__":
    ingest_pdfs()
