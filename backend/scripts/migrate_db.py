import os
import pandas as pd
from sqlalchemy import create_engine
import glob

# Try to get from environment, fallback to localhost for direct script run
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://propselect:propselect@localhost:5432/propselect")

def migrate():
    print(f"Conectando ao banco de dados...")
    engine = create_engine(DATABASE_URL)
    
    path = os.path.join(os.path.dirname(__file__), '../../data/planilhas')
    excel_files = glob.glob(os.path.join(path, '*.xlsx'))
    
    if not excel_files:
        print("Nenhum arquivo .xlsx encontrado em", path)
        return

    # List of expected columns to keep (ignoring Unnamed columns and comments)
    expected_cols = [
        'apcCT ', 'NOME HÉLICE', 'TIPO DE AERONAVE', 'TIPO DE PROPULSÃO', 
        'ROTAÇÃO (RPM)', 'DIAMETRO ', 'PITCH', 'VELOCIDADE (m/s)', 
        'Advanced Ratio ', 'Eficiência', 'Ct', 'Cp', 'Power (W)', 
        'Torque (N.m)', 'Trust (N)', 'g/W', 'Mach', 'Rey × 10^6', 'FOM'
    ]

    all_dfs = []
    for file in excel_files:
        print(f"Processando {os.path.basename(file)}...")
        try:
            df = pd.read_excel(file, sheet_name='Página1')
            
            # Select only valid columns
            cols_to_use = [c for c in expected_cols if c in df.columns]
            df = df[cols_to_use]
            
            # Standardize column names for postgres (lowercase, no spaces/special chars)
            def clean_col(c):
                c = c.strip().lower().replace(' ', '_').replace('(', '').replace(')', '')
                c = c.replace('/', '_').replace('×_10^6', 'e6').replace('.', '').replace('ç', 'c').replace('ã', 'a').replace('é', 'e')
                return c
                
            df.columns = [clean_col(c) for c in df.columns]
            
            # Optional: Add source file tracking
            df['source_file'] = os.path.basename(file)
            
            all_dfs.append(df)
        except Exception as e:
            print(f"Erro ao processar {file}: {e}")
            
    if all_dfs:
        final_df = pd.concat(all_dfs, ignore_index=True)
        table_name = "propeller_data"
        print(f"\nInserindo {len(final_df)} registros na tabela '{table_name}'...")
        final_df.to_sql(table_name, engine, if_exists='replace', index=False)
        print("Migração concluída com sucesso!")
    else:
        print("Nenhum dado válido para migrar.")

if __name__ == "__main__":
    migrate()
