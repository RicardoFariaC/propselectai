  ### Exemplo 1: Aeronave de Treinamento / Cruzeiro (ex: Cessna 172)                                                                                                                                        
                                                                                                                                                                                                            
  • Peso (kg):  1100 
  • Potência Mínima do Motor (hp):  150
  • Potência Máxima do Motor (hp):  160
  • Velocidade de Cruzeiro (m/s):  62  (Aproximadamente 120 nós)
  • Altitude (m):  2500  (Aproximadamente 8.200 pés)
  • Tipo de Missão:  Cruzeiro  (ou  Treinamento )
  • Diâmetro Máximo (polegadas):  75  (Opcional)
  ──────
  ### Como testar via API (Se você estiver usando Postman, cURL ou a documentação do FastAPI/Swagger):
  
  Você pode enviar o seguinte corpo JSON (Payload) na rota de recomendação (ex:  POST /recommend ):
  
    {
      "weight_kg": 1100.0,
      "min_engine_power_hp": 150.0,
      "max_engine_power_hp": 160.0,
      "cruise_speed_ms": 62.0,
      "altitude_m": 2500.0,
      "mission_type": "Cruzeiro",
      "max_diameter_inches": 75.0
    }
  
  ### Exemplo 2: Drone Comercial / VANT Pesado
  
  Caso queira testar um cenário diferente para forçar o sistema a buscar hélices menores e motores elétricos ou de menor cilindrada:
  
  • Peso (kg):  25 
  • Potência Mínima do Motor (hp):  10 
  • Potência Máxima do Motor (hp):  15 
  • Velocidade de Cruzeiro (m/s):  20 
  • Altitude (m):  500 
  • Tipo de Missão:  Mapeamento / Fotogrametria 
  • Diâmetro Máximo (polegadas):  30 
