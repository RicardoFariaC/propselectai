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

def generate_justification(propeller, request):
    if not OPENAI_API_KEY or OPENAI_API_KEY == "your-openai-api-key-here":
        return "Configure a chave da API da OpenAI no arquivo .env para gerar a justificativa técnica com RAG."
        
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small", openai_api_key=OPENAI_API_KEY)
    try:
        vectorstore = Chroma(client=get_chroma_client(), embedding_function=embeddings, collection_name="propellers")
        mission_type = request.mission_type
        weight = request.weight_kg
        power = request.engine_power_hp
        diameter = propeller.get('diametro', 'N/A')
        pitch = propeller.get('pitch', 'N/A')
        
        # Query bilíngue para combater o viés de idioma do modelo de embeddings
        query = f"Hélice {propeller['nome_helice']} para missão de {mission_type}. Propeller aerodynamic characteristics and performance for {mission_type} mission."
        # Fetch more children since multiple might point to same parent
        docs = vectorstore.similarity_search(query, k=5)
        
        parent_store_path = os.path.join(os.path.dirname(__file__), '../data/parent_docs.json')
        parent_docs_dict = {}
        if os.path.exists(parent_store_path):
            with open(parent_store_path, 'r', encoding='utf-8') as f:
                parent_docs_dict = json.load(f)
                
        context_parts = []
        retrieved_parent_ids = set()
        
        local_reference_map = {}
        
        for doc in docs:
            doc_id = doc.metadata.get('doc_id')
            
            # If PDR mapped, fetch the large parent text
            if doc_id and doc_id in parent_docs_dict:
                if doc_id in retrieved_parent_ids:
                    continue
                retrieved_parent_ids.add(doc_id)
                parent_data = parent_docs_dict[doc_id]
                source = parent_data['metadata'].get('source', 'Documento Desconhecido')
                filename = os.path.basename(source)
                page = parent_data['metadata'].get('page', 0)
                content = parent_data['page_content']
            else:
                # Fallback to standard chunk if no doc_id or missing parent file
                source = doc.metadata.get('source', 'Documento Desconhecido')
                filename = os.path.basename(source)
                page = doc.metadata.get('page', 0)
                content = doc.page_content
                
            # ABNT reference mapping into local map
            ref_entry = f"{filename.upper()}. Catálogo Técnico/Artigo. Página {page}."
            if ref_entry not in local_reference_map.values():
                ref_idx = len(local_reference_map) + 1
                local_reference_map[ref_idx] = ref_entry
            else:
                ref_idx = next(k for k, v in local_reference_map.items() if v == ref_entry)
            
            context_parts.append(f"[{ref_idx}]\n{content}")
            
        context = "\n\n".join(context_parts)
    except Exception as e:
        print(f"Error reading from ChromaDB/PDR: {e}")
        context = "Nenhuma informação extra nos manuais (falha ao conectar no ChromaDB ou base vazia)."
        local_reference_map = {}

    llm = ChatOpenAI(temperature=0.0, openai_api_key=OPENAI_API_KEY)
    
    prompt = PromptTemplate(
        input_variables=["propeller_name", "mission", "context", "efficiency", "thrust", "weight", "power", "diameter", "pitch"],
        template="""
        Você é um Engenheiro Chefe de Aerodinâmica elaborando a justificativa técnica de um PDR (Preliminary Design Review).
        
        Sua tarefa é argumentar de forma avançada e ESTRITAMENTE ESPECÍFICA por que a hélice {propeller_name} (Diâmetro: {diameter}, Passo: {pitch}) foi selecionada para a aeronave com a missão de "{mission}".
        O veículo possui um peso de {weight} kg e potência de motor de {power} HP.
        Os dados aerodinâmicos calculados para esta hélice são: Eficiência de {efficiency} e Empuxo de {thrust} N.
        
        LITERATURA DE ENGENHARIA (Fontes Numeradas Locais):
        {context}
        
        DIRETRIZES OBRIGATÓRIAS:
        1. Escreva UM ÚNICO parágrafo extremamente técnico e detalhado focado em engenharia aeronáutica. O texto NÃO PODE ser genérico.
        2. Analise COMO o diâmetro de {diameter} e o passo de {pitch} interagem com a potência de {power} HP para gerar o empuxo de {thrust} N necessário para sustentar o peso de {weight} kg na missão de {mission}.
        3. Você DEVE usar a notação de colchetes para citar as fontes (Ex: "O empuxo de {thrust}N garante a subida, como analisado em [1], mitigando as perdas de ponta [2].").
        4. É OBRIGATÓRIO embasar a sua argumentação nas [Fontes] fornecidas, citando a numeração correspondente.
        5. JAMAIS escreva o nome do arquivo, PDF ou autor por extenso no texto. Use EXCLUSIVAMENTE a numeração em colchetes [X] da Fonte.
        """
    )
    
    chain = prompt | llm
    response = chain.invoke({
        "propeller_name": propeller['nome_helice'],
        "mission": mission_type,
        "context": context,
        "efficiency": propeller['eficiência'],
        "thrust": propeller['trust_n'],
        "weight": weight,
        "power": power,
        "diameter": diameter,
        "pitch": pitch
    })
    
    return response.content, local_reference_map
