import os

from pymongo import MongoClient


def get_mongodb():
    host = os.getenv("MONGO_HOST", "localhost") # Adicionado fallback para localhost
    username = os.getenv("MONGO_USERNAME")
    password = os.getenv("MONGO_PASSWORD")
    db_name = os.getenv("MONGO_DB_NAME", "ipb") # Define 'ipb' como padrão
    
    # --- LOG DE DIAGNÓSTICO ---
    print("--- INFORMAÇÕES DE CONEXÃO MONGO ---")
    print(f"  - HOST: {host}")
    print(f"  - DATABASE NAME: {db_name}")
    print("------------------------------------")
    
    if not db_name:
        print("[ALERTA] A variável de ambiente MONGO_DB_NAME não está definida!")

    mode = os.getenv('MODE', 'development')
    tls = '&tls=true' if mode == 'production' else ''
    
    # Monta a URI de conexão. Lembre-se que um db_name vazio pode causar problemas.
    uri = f"mongodb://{username}:{password}@{host}/{db_name if db_name else ''}?authSource=admin&retryWrites=true&w=majority{tls}"

    client = MongoClient(uri)
    return client[db_name]