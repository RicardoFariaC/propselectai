import os
import pandas as pd
from sqlalchemy import create_engine

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://propselect:propselect@postgres:5432/propselect")
engine = create_engine(DATABASE_URL)

def get_filtered_propellers(thrust_req, min_efficiency, max_diameter=None):
    # Using regex to ensure the string is numeric to avoid parsing dates like "2025-08-06"
    numeric_pattern = r'^[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?$'
    
    query = f"""
    SELECT * FROM propeller_data
    WHERE "trust_n" ~ '{numeric_pattern}'
    AND CAST("trust_n" AS float) >= {thrust_req}
    AND "eficiência" ~ '{numeric_pattern}'
    AND CAST("eficiência" AS float) >= {min_efficiency}
    """
    
    if max_diameter:
        query += f" AND \"diametro\" ~ '{numeric_pattern}' AND CAST(\"diametro\" AS float) <= {max_diameter}"
        
    query += f" ORDER BY CAST(\"eficiência\" AS float) DESC LIMIT 10"

    
    try:
        df = pd.read_sql(query, engine)
        return df.to_dict('records')
    except Exception as e:
        print(f"Error querying DB: {e}")
        return []
