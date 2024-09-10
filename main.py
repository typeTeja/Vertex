from typing import Optional
from fastapi import FastAPI
import psycopg2
import pandas as pd
import logging

app = FastAPI()

# Configurando o logger
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

# Função para obter dados do banco de dados usando pandas
def get_data(query, params=None):
    try:
        # Conexão com o banco de dados PostgreSQL usando a URL externa
        conn = psycopg2.connect(
            "postgresql://dashmonlcnunes_user:XbP8HgchWxRg2Ea9O1DDXw9Ou0J1jABO@dpg-crfltd3v2p9s73csj3m0-a.oregon-postgres.render.com/dashmonlcnunes",
            sslmode='require'  # Garantindo a conexão SSL
        )
        # Executa a consulta SQL e retorna um DataFrame
        df = pd.read_sql_query(query, conn, params=params)
        conn.close()
        return df
    except Exception as e:
        logger.error(f"Erro ao obter dados: {e}")
        return pd.DataFrame()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

@app.get("/empresa")
def get_empresa():
    try:
        # Consulta SQL para obter os dados
        query = "SELECT nom_razao_social FROM empresa LIMIT 1;"
        # Chama a função get_data para executar a consulta
        df = get_data(query)
        
        if not df.empty:
            return {"nom_razao_social": df.iloc[0, 0]}
        else:
            return {"error": "Nenhum dado encontrado"}
    except Exception as e:
        return {"error": str(e)}
