import os
import sys
from datetime import datetime

# Adiciona o diretório raiz do projeto ao sys.path
# para permitir a importação de módulos da aplicação (ex: app.mongo)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.mongo import get_mongodb

def migrate_data():
    """
    Script para migrar os dados de membros no MongoDB, utilizando a conexão da app.
    - Força o uso do banco de dados 'ipb'.
    - Converte o campo 'nascimento' de string 'dd/mm/yyyy' para datetime.
    - Garante que todos os novos campos do schema existam nos documentos.
    """
    # --- Força as variáveis de ambiente para a conexão correta ---
    os.environ["MONGO_HOST"] = "localhost"
    os.environ["MONGO_USERNAME"] = "admin"
    os.environ["MONGO_PASSWORD"] = "NuMX)J~&\\4KRBg&r_E|."
    os.environ["MONGO_DB_NAME"] = "ipb" # Força o uso do DB 'ipb'

    print(f"Conectando ao MongoDB usando a configuração da aplicação...")
    
    try:
        db = get_mongodb()
        
        # Testa a conexão
        db.client.admin.command('ping') 
        print("Conexão com MongoDB bem-sucedida.")
        print(f"Usando banco de dados: {db.name}")

        collections = db.list_collection_names()
        if not collections:
            print("[ERRO] Nenhuma coleção encontrada no banco de dados. Verifique o nome do DB e as permissões.")
            return

        print("Coleções disponíveis:")
        for coll in collections:
            print(f"  - {coll}")

        if 'membros' not in collections:
            print("[ERRO] A coleção 'membros' não foi encontrada no banco de dados 'ipb'.")
            return

        collection = db['membros']
        print(f"Usando coleção: {collection.name}")

    except Exception as e:
        print(f"Erro ao conectar ou comunicar com o MongoDB: {e}")
        return

    # --- Lógica da Migração ---
    try:
        membros_a_migrar = list(collection.find({}))
        print(f"\nEncontrados {len(membros_a_migrar)} membros para verificar.")
        if not membros_a_migrar:
            print("Nenhum membro encontrado para migrar.")
            return
            
    except Exception as e:
        print(f"Erro ao buscar documentos na coleção 'membros': {e}")
        return

    # Campos novos a serem adicionados se não existirem
    novos_campos = [
        'pais', 'nome_pai', 'nome_mae', 'nome_conjuge', 'data_casamento', 'rg',
        'batismo_data', 'batismo_pastor', 'batismo_igreja',
        'profissao_fe_data', 'profissao_fe_pastor', 'profissao_fe_igreja'
    ]

    migrados_count = 0
    erros_conversao = 0
    for membro in membros_a_migrar:
        update_operations = {}
        
        # 1. Converter 'nascimento' para datetime
        if 'nascimento' in membro and isinstance(membro['nascimento'], str):
            try:
                # Tenta converter do formato 'dd/mm/yyyy'
                nascimento_dt = datetime.strptime(membro['nascimento'], '%d/%m/%Y')
                update_operations['nascimento'] = nascimento_dt
            except (ValueError, TypeError):
                print(f"  - [AVISO] ID: {membro.get('_id')}: Formato de data inválido para 'nascimento': {membro['nascimento']}. Ignorando conversão.")
                erros_conversao += 1

        # 2. Adicionar novos campos com valor None se não existirem
        for campo in novos_campos:
            if campo not in membro:
                update_operations[campo] = None

        # 3. Executar a atualização se houver operações a fazer
        if update_operations:
            try:
                collection.update_one(
                    {'_id': membro['_id']},
                    {'$set': update_operations}
                )
                migrados_count += 1
            except Exception as e:
                print(f"  - [ERRO] ID: {membro.get('_id')}: Falha ao atualizar documento: {e}")


    print(f"\nMigração concluída.")
    print(f"Total de membros verificados: {len(membros_a_migrar)}")
    print(f"Membros que necessitavam de atualização: {migrados_count}")
    print(f"Campos 'nascimento' com formato de data inválido: {erros_conversao}")


if __name__ == "__main__":
    migrate_data()