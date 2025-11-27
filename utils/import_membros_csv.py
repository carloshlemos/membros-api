import csv
import os
from uuid import uuid4
from dotenv import load_dotenv
from pymongo import MongoClient
from urllib.parse import quote_plus

def import_membros_from_csv():
    # Carrega as variáveis de ambiente do arquivo variables.env
    load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', 'variables.env'))

    # Obtém as credenciais do MongoDB a partir das variáveis de ambiente
    host = os.getenv("MONGO_HOST")
    username = os.getenv("MONGO_USERNAME")
    password = os.getenv("MONGO_PASSWORD")
    db_name = os.getenv("MONGO_DB_NAME")

    # Escapa o nome de usuário e a senha
    escaped_username = quote_plus(username)
    escaped_password = quote_plus(password)

    # String de conexão com o MongoDB
    uri = f"mongodb://{escaped_username}:{escaped_password}@{host}/{db_name}?authSource=admin"

    try:
        # Conecta ao MongoDB
        client = MongoClient(uri)
        db = client[db_name]
        collection = db.membros
        
        # Limpa a coleção antes de importar
        collection.delete_many({})
        print("Coleção 'membros' limpa.")

        # Caminho para o arquivo CSV
        csv_file_path = 'membros.csv'

        # Abre o arquivo CSV e o lê
        with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            
            # Itera sobre as linhas do CSV e as insere no MongoDB
            for row in csv_reader:
                # Limpa as chaves (nomes das colunas) de caracteres estranhos
                cleaned_row = {key.lstrip('\ufeff'): value for key, value in row.items()}
                # Adiciona o campo 'id' com um UUID
                cleaned_row['id'] = str(uuid4())
                collection.insert_one(cleaned_row)

        print("Importação concluída com sucesso!")

    except Exception as e:
        print(f"Ocorreu um erro: {e}")

if __name__ == "__main__":
    import_membros_from_csv()
