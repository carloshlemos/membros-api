import pandas as pd
import re

def parse_membros(text):
    member_blocks = re.split(r'\n(?=([A-Z][a-z]+\s){1,4}[A-Z][a-z]+$)', text, flags=re.MULTILINE)
    
    all_members_data = []

    for block in member_blocks:
        if not block.strip() or "Igreja Presbiteriana" in block:
            continue

        data = {}
        lines = block.strip().split('\n')
        
        data['nome'] = lines[0].strip()
        
        # Initialize fields
        data['id_membro'] = None
        data['endereco'] = None
        data['bairro'] = None
        data['cep'] = None
        data['cidade'] = None
        data['estado'] = None
        data['telefone'] = None
        data['celular'] = None
        data['email'] = None
        data['nascimento'] = None
        data['naturalidade'] = None
        data['filiacao'] = None
        data['estado_civil'] = None
        data['conjuge'] = None
        data['escolaridade'] = None
        data['profissao'] = None
        data['igreja'] = None
        data['data_admissao'] = None
        data['meio_admissao'] = None
        data['data_batismo'] = None
        data['igreja_batismo'] = None
        data['oficiante_batismo'] = None
        data['data_profissao_fe'] = None
        data['igreja_profissao_fe'] = None
        data['pastor'] = None
        data['tipo_membro'] = None
        data['oficio'] = None

        for i, line in enumerate(lines[1:]):
            line = line.strip()
            if not line:
                continue

            # ID
            if re.match(r'^\d+$', line):
                data['id_membro'] = line
                continue

            # Endereco e Bairro
            if line.startswith('Rua') or line.startswith('Av.') or line.startswith('Endereço:'):
                if '- Bairro' in line:
                    parts = line.split('- Bairro')
                    data['endereco'] = parts[0].strip()
                    data['bairro'] = parts[1].strip()
                else:
                    data['endereco'] = line
                continue

            # CEP
            if line.startswith('CEP.') or line.startswith('СЕР.'):
                data['cep'] = line.replace('CEP.', '').replace('СЕР.', '').strip()
                continue

            # Cidade e Estado
            if re.match(r'^[A-Z][a-zçãéâôíú]+.*\s-\s[A-Z]{2}\s-\sBrasil$', line):
                parts = line.split(' - ')
                data['cidade'] = parts[0]
                data['estado'] = parts[1]
                continue

            # Tel, Cel, Email
            if line.startswith('Tel:'):
                match = re.search(r'Tel:\s*([^ -]+)', line)
                if match:
                    data['telefone'] = match.group(1).strip()
                match = re.search(r'Cel:\s*([^ -]+)', line)
                if match:
                    data['celular'] = match.group(1).strip()
                match = re.search(r'Email:\s*(.*)', line)
                if match:
                    data['email'] = match.group(1).strip()
                continue

            # Nascimento e Naturalidade
            if line.startswith('Data de nascimento:'):
                match = re.search(r'Data de nascimento:\s*([^ -]+)', line)
                if match:
                    data['nascimento'] = match.group(1).strip()
                match = re.search(r'Naturalidade:\s*(.*)', line)
                if match:
                    data['naturalidade'] = match.group(1).strip()
                continue

            # Filiação
            if line.startswith('Filiação:'):
                data['filiacao'] = line.replace('Filiação:', '').strip()
                continue

            # Estado Civil
            if line.startswith('Estado civil:'):
                data['estado_civil'] = line.replace('Estado civil:', '').strip()
                continue

            # Cônjuge
            if line.startswith('Cônjuge:'):
                data['conjuge'] = line.replace('Cônjuge:', '').strip()
                continue

            # Escolaridade e Profissão
            if line.startswith('Escolaridade:'):
                match = re.search(r'Escolaridade:\s*([^ -]+)', line)
                if match:
                    data['escolaridade'] = match.group(1).strip()
                match = re.search(r'Profissão:\s*(.*)', line)
                if match:
                    data['profissao'] = match.group(1).strip()
                continue

            # Local onde congrega
            if line.startswith('Local onde congrega:'):
                data['igreja'] = line.replace('Local onde congrega:', '').strip()
                continue
            
            # Número de ordem
            if line.startswith('Número de ordem:'):
                data['id_membro'] = line.replace('Número de ordem:', '').strip()
                continue

            # Data de admissão
            if line.startswith('Data de admissão:'):
                data['data_admissao'] = line.replace('Data de admissão:', '').strip()
                continue

            # Meio de admissão
            if line.startswith('Meio de admissão:'):
                data['meio_admissao'] = line.replace('Meio de admissão:', '').strip()
                continue

            # Data do batismo
            if line.startswith('Data do batismo:'):
                data['data_batismo'] = line.replace('Data do batismo:', '').strip()
                continue

            # Igreja onde foi batizado(a)
            if line.startswith('Igreja onde foi batizado(a):'):
                data['igreja_batismo'] = line.replace('Igreja onde foi batizado(a):', '').strip()
                continue

            # Oficiante do batismo
            if line.startswith('Oficiante do batismo:'):
                data['oficiante_batismo'] = line.replace('Oficiante do batismo:', '').strip()
                continue

            # Data da profissão de fé
            if line.startswith('Data da profissão de fé:'):
                data['data_profissao_fe'] = line.replace('Data da profissão de fé:', '').strip()
                continue

            # Igreja onde fez profissão de fé
            if line.startswith('Igreja onde fez profissão de fé:'):
                data['igreja_profissao_fe'] = line.replace('Igreja onde fez profissão de fé:', '').strip()
                continue

            # Pastor
            if line.startswith('Pastor:'):
                data['pastor'] = line.replace('Pastor:', '').strip()
                continue

            # Tipo de membro
            if 'Membro' in line:
                data['tipo_membro'] = line.strip()
                continue

            # Ofício
            if line.startswith('Ofício:'):
                data['oficio'] = line.replace('Ofício:', '').strip()
                continue

        all_members_data.append(data)
        
    return all_members_data

with open("membros_ipbmp.txt", "r", encoding="utf-8") as f:
    pdf_text = f.read()

# The first line is the church name, so we remove it.
pdf_text = "\n".join(pdf_text.split('\n')[1:])

final_data = parse_membros(pdf_text)

df = pd.DataFrame(final_data)

output_filename = "membros_ipbmp.csv"
df.to_csv(output_filename, index=False, encoding="utf-8-sig")

print(f"Dados de {len(df)} membros extraídos e salvos em '{output_filename}'.")
print("\nVisualização das 5 primeiras linhas:")
print(df.head())