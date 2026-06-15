import os
import json
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import PromptTemplate
import chromadb

CHROMA_HOST = os.getenv("CHROMA_HOST", "chromadb")
CHROMA_PORT = int(os.getenv("CHROMA_PORT", 8000))
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def get_chroma_client():
    return chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)

def generate_justification(propeller, mission_type):
    if not OPENAI_API_KEY or OPENAI_API_KEY == "your-openai-api-key-here":
        return "Configure a chave da API da OpenAI no arquivo .env para gerar a justificativa técnica com RAG.", []
        
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small", openai_api_key=OPENAI_API_KEY)
    
    references = set()
    try:
        vectorstore = Chroma(client=get_chroma_client(), embedding_function=embeddings, collection_name="propellers")
        query = f"Hélice {propeller['nome_helice']} para missão de {mission_type}"
        # Fetch more children since multiple might point to same parent
        docs = vectorstore.similarity_search(query, k=5)
        
        # PDR Load Parent Docs JSON
        parent_store_path = os.path.join(os.path.dirname(__file__), '../data/parent_docs.json')
        parent_docs_dict = {}
        if os.path.exists(parent_store_path):
            with open(parent_store_path, 'r', encoding='utf-8') as f:
                parent_docs_dict = json.load(f)
                
        context_parts = []
        retrieved_parent_ids = set()
        
        for doc in docs:
            doc_id = doc.metadata.get('doc_id')
            
            # If PDR mapped, fetch the large parent text
            if doc_id and doc_id in parent_docs_dict and doc_id not in retrieved_parent_ids:
                retrieved_parent_ids.add(doc_id)
                parent_data = parent_docs_dict[doc_id]
                source = parent_data['metadata'].get('source', 'Documento Desconhecido')
                filename = os.path.basename(source)
                page = parent_data['metadata'].get('page', 0)
                content = parent_data['page_content']
            elif not doc_id:
                # Fallback to standard chunk if no doc_id (legacy mode)
                source = doc.metadata.get('source', 'Documento Desconhecido')
                filename = os.path.basename(source)
                page = doc.metadata.get('page', 0)
                content = doc.page_content
            else:
                continue
                
            # Simple ABNT reference mapping
            ref_entry = f"{filename.upper()}. Catálogo Técnico/Artigo. Página {page}."
            references.add(ref_entry)
            
            context_parts.append(f"[Fonte: {filename}, p. {page}]\n{content}")
            
        context = "\n\n".join(context_parts)
    except Exception as e:
        print(f"Error reading from ChromaDB/PDR: {e}")
        context = "Nenhuma informação extra nos manuais (falha ao conectar no ChromaDB ou base vazia)."

    llm = ChatOpenAI(temperature=0.0, openai_api_key=OPENAI_API_KEY)
    
    prompt = PromptTemplate(
        input_variables=["propeller_name", "mission", "context", "efficiency", "thrust"],
        template="""
        Você é um especialista aeroespacial projetando sistemas de propulsão.
        Baseado EXCLUSIVAMENTE nos documentos extraídos dos manuais abaixo:
        {context}
        
        Justifique por que a hélice {propeller_name} é uma boa escolha para uma missão do tipo "{mission}".
        A hélice selecionada possui eficiência de {efficiency} e empuxo de {thrust} N.
        
        Regras:
        1. Forneça uma explicação técnica e concisa (máx 5 frases).
        2. Utilize citações indiretas no texto, referenciando os autores ou manuais fornecidos no contexto no formato ABNT (Ex: Segundo MANUAL (p. 12)...).
        3. Evite suposições ou informações não presentes nos documentos.
        4. Liste as referências utilizadas no final da justificativa, seguindo o formato: "NOME_ARQUIVO. Catálogo Técnico/Artigo. Página X.".
        """
    )
    
    chain = prompt | llm
    response = chain.invoke({
        "propeller_name": propeller['nome_helice'],
        "mission": mission_type,
        "context": context,
        "efficiency": propeller['eficiência'],
        "thrust": propeller['trust_n']
    })
    
    return response.content, list(references)
