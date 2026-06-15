import streamlit as st
import requests
import os

st.set_page_config(page_title="PropSelectAI", layout="wide", page_icon="✈️")

st.title("PropSelectAI: Sistema Inteligente de Seleção de Hélices")
st.write("Insira os parâmetros do projeto de aeronave para receber as melhores recomendações utilizando IA (LLM+RAG).")

with st.sidebar:
    st.header("Parâmetros do Projeto")
    mission_type = st.selectbox("Tipo de Missão", ["Transporte", "Acrobacia", "VANT / Drone", "Treinamento"])
    weight_kg = st.number_input("Peso da Aeronave (kg)", min_value=0.1, value=1000.0)
    engine_power_hp = st.number_input("Potência do Motor (HP)", min_value=1.0, value=150.0)
    cruise_speed_ms = st.number_input("Velocidade de Cruzeiro (m/s)", min_value=1.0, value=50.0)
    altitude_m = st.number_input("Altitude (m)", min_value=0.0, value=1000.0)
    max_diameter = st.number_input("Diâmetro Máximo (Opcional - polegadas)", min_value=0.0, value=0.0)

if st.button("Buscar Recomendações", type="primary"):
    with st.spinner("Analisando banco de dados, ranqueando propulsores e gerando justificativas com IA..."):
        payload = {
            "weight_kg": weight_kg,
            "engine_power_hp": engine_power_hp,
            "cruise_speed_ms": cruise_speed_ms,
            "altitude_m": altitude_m,
            "mission_type": mission_type,
        }
        if max_diameter > 0:
            payload["max_diameter_inches"] = max_diameter
            
        try:
            # Comunicação interna via Docker (container backend porta 8000)
            api_url = "http://backend:8000/api/recommend"
            
            res = requests.post(api_url, json=payload)
            
            if res.status_code == 200:
                data = res.json()
                st.success("Recomendações e PDR gerados com sucesso!")
                
                recs = data.get("recommendations", [])
                for i, rec in enumerate(recs):
                    with st.expander(f"🏆 Top {i+1}: {rec['name']}"):
                        col1, col2, col3 = st.columns(3)
                        col1.metric("Eficiência", f"{rec['efficiency']:.2f}")
                        col2.metric("Empuxo Máximo", f"{rec['thrust']:.2f} N")
                        col3.metric("Diâmetro", f"{rec['diameter']}\"")
                        st.info(f"**Justificativa Técnica da IA:**\n\n{rec['justification']}")
                        
                report_path = data.get("report_path")
                if report_path:
                    filename = report_path.split("/")[-1]
                    local_pdf = f"/app/data/pdf_gerados/{filename}"
                    
                    if os.path.exists(local_pdf):
                        with open(local_pdf, "rb") as pdf_file:
                            st.download_button(
                                label="📥 Baixar Relatório (PDR) Completo",
                                data=pdf_file,
                                file_name=filename,
                                mime="application/pdf"
                            )
            else:
                st.error(f"Ocorreu um erro na API: {res.text}")
        except Exception as e:
            st.error(f"Erro de conexão com o servidor: {e}. Verifique se o backend está rodando no docker-compose.")
