from bs4 import BeautifulSoup
import pandas as pd
import re

# Carrega o conteúdo do arquivo, que inclui JS
with open("membros.html", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Extrai o HTML de dentro da variável JavaScript usando regex
# O padrão busca o conteúdo dentro de 'html': '...'
match = re.search(r"'html':\s*'(.*)'", content, re.DOTALL)
if not match:
    raise ValueError("Não foi possível encontrar o conteúdo HTML na variável JavaScript.")

html_content = match.group(1)
# Remove barras invertidas de escape de aspas simples
html_content = html_content.replace("\\'", "'")

# 2. Analisa o HTML extraído
soup = BeautifulSoup(html_content, "html.parser")

# 3. Encontra todos os blocos de membros
# Cada membro está em uma <td> com um estilo específico
member_blocks = soup.find_all("td", style="background-color: #ffffff; padding-left: 20px; padding-right: 20px;")

all_members_data = []

# 4. Itera sobre cada bloco de membro para extrair os dados
for block in member_blocks:
    # Ignora blocos que não contêm a estrutura de dados de um membro (como o título)
    if not block.find("table"):
        continue

    # Extrai o nome
    name_tag = block.find("b")
    if not name_tag:
        continue
    nome = name_tag.get_text(strip=True)

    # Extrai o texto com os demais dados
    data_text_container = block.find("td", valign="top")
    if not data_text_container:
        continue
    
    # Usa .stripped_strings para obter uma lista de textos limpos
    lines = list(data_text_container.stripped_strings)

    # Monta o dicionário de dados para o membro atual
    dados = {"nome": nome}
    
    # Mapeia os prefixos para os nomes das colunas
    field_map = {
        "Tel:": "telefone",
        "Cel:": "celular",
        "Email:": "email",
        "Data Nascimento:": "nascimento",
        "Naturalidade:": "naturalidade",
        "Estado Civil:": "estado_civil",
        "Escolaridade:": "escolaridade",
        "Profissão:": "profissao",
        "Cep.": "cep",
        "Bairro:": "bairro",
        "Local onde congrega:": "igreja",
    }

    full_address = []
    
    # Processa as linhas de texto
    raw_text = data_text_container.get_text(separator='\n', strip=True)
    raw_lines = raw_text.split('\n')

    # Extração de dados linha a linha
    for i, line in enumerate(raw_lines):
        # Endereço (geralmente as primeiras linhas antes dos campos com prefixo)
        if i < 4 and ":" not in line and "Cep." not in line and not any(prefix in line for prefix in field_map):
             # Adiciona a parte do endereço, evitando a cidade/estado que vem depois
            if " - " not in line or "Brasil" not in line:
                full_address.append(line.strip())

        if "Tel:" in line:
            parts = line.split("- Cel:")
            dados["telefone"] = parts[0].replace("Tel:", "").strip()
            dados["celular"] = parts[1].strip() if len(parts) > 1 else None
        elif any(prefix in line for prefix in field_map if prefix != "Tel:"):
            for prefix, key in field_map.items():
                if prefix in line:
                    dados[key] = line.replace(prefix, "").strip()
                    break
        elif "Membro" in line:
            dados["tipo_membro"] = line.strip()
        elif "Ofício:" in line:
            dados["oficio"] = line.replace("Ofício:", "").strip()

    dados["endereco"] = ", ".join(full_address) if full_address else None

    all_members_data.append(dados)

# 5. Converte a lista de dicionários em um DataFrame do Pandas
df = pd.DataFrame(all_members_data)

# 6. Salva o DataFrame em um arquivo CSV
output_filename = "membros.csv"
df.to_csv(output_filename, index=False, encoding="utf-8-sig")

print(f"Dados de {len(df)} membros extraídos e salvos em '{output_filename}'.")
print("\nVisualização das 5 primeiras linhas:")
print(df.head())