import pandas as pd
from ipwhois import IPWhois
from concurrent.futures import ThreadPoolExecutor, as_completed

# Adicione aqui o caminho completo do arquivo excel
file_path = 'C:/Users/ErikMatheusFernandes/Desktop/python-extract-pdftable/databases/Planilhamento de IPs.xlsx'

# Carrega a tabela do excel
df = pd.read_excel(file_path)

# Verifica se tem a coluna "Whois Result" e se não tiver, cria 
if 'Whois Result' not in df.columns:
    df['Whois Result'] = ''
df['Whois Result'] = df['Whois Result'].astype('object')  # Força um tipo para que a tabela seja legível

# Obtém as informações do WHOIS usando ipwhois
def get_whois_info(ip):
    try:
        # Instancia o objeto IPWhois e faz a busca (esse IPWhois definir de forma automática o servidor WHOIS)
        obj = IPWhois(ip, timeout=10)  
        result = obj.lookup_rdap()  # O RDAP serve para transformar o IP em um objeto JSON

        # Dicionário para armazenar os dados que precisa
        whois_data = {
            'provider': 'N/A',
            'location': 'N/A',
            'email': 'N/A',
            'asn_description': 'N/A',
            'ip_version': 'N/A',
            'cnpj_cpf': 'N/A'
        }

        # Retorna uma mensagem de erro caso não tenha nenhum dado de rede
        if not result or 'network' not in result:
            return ip, "Erro: Nenhum dado de rede retornado pela consulta WHOIS"
        
        # As demais funções abaixo são para pegar os dados do JSON e colocar no dicionário
        if result.get('entities') and result.get('objects'):
            for entity in result['objects'].values():
                if 'roles' in entity and 'registrant' in entity['roles']:
                    whois_data['provider'] = entity.get('contact', {}).get('name', 'N/A')
                    whois_data['cnpj_cpf'] = entity.get('handle', 'N/A')
                    break
        if whois_data['provider'] == 'N/A' and result['network'].get('name'):
            whois_data['provider'] = result['network']['name']

        # Local (país)
        if result['network'].get('country'):
            whois_data['location'] = result['network']['country']
        elif result.get('asn_country_code'):
            whois_data['location'] = result['asn_country_code']

        # Email (prioridade: technical, depois abuse)
        if result.get('entities') and result.get('objects'):
            for entity in result['objects'].values():
                if 'contact' in entity and entity['contact'].get('email'):
                    whois_data['email'] = entity['contact']['email'][0]['value']
                    break

        # ASN Description
        if result.get('asn_description'):
            whois_data['asn_description'] = result['asn_description']

        # IP Version
        if result['network'].get('ip_version'):
            whois_data['ip_version'] = result['network']['ip_version']

        # Retorna uma string com os dados
        result_str = (
            f"Provider: {whois_data['provider']}, "
            f"Location: {whois_data['location']}, "
            f"Email: {whois_data['email']}, "
            f"ASN Description: {whois_data['asn_description']}, "
            f"IP Version: {whois_data['ip_version']}, "
            f"CNPJ/CPF: {whois_data['cnpj_cpf']}"
        )
        return ip, result_str
    except Exception as e:
        return ip, f"Erro: {str(e)}"

# Por poder ser demorado, essa função permite que várias consultas sejam feitas em paralelo
def process_ips_in_parallel(ips):
    results = {}
    with ThreadPoolExecutor(max_workers=10) as executor:  # Define quantas execuções podem ser feitas ao mesmo tempo
        # Inicia as consultas em paralelo
        future_to_ip = {executor.submit(get_whois_info, ip): ip for ip in ips}
        for future in as_completed(future_to_ip):
            ip = future_to_ip[future]
            try:
                ip, result = future.result()
                results[ip] = result
                print(f"Processado IP: {ip} - Resultado: {result}")
            except Exception as e:
                results[ip] = f"Erro: {str(e)}"
                print(f"Processado IP: {ip} - Resultado: Erro: {str(e)}")
    return results

# Coleta todos os IPs da coluna "IP Address" e converte para uma lista
ips = df['IP Address'].astype(str).tolist()

# Processa os IPs em paralelo
results = process_ips_in_parallel(ips)

# Atualiza o DataFrame com os resultados
for ip, whois_result in results.items():
    df.loc[df['IP Address'].astype(str) == ip, 'Whois Result'] = whois_result

# Quando tudo finalizar, a tabela é salva no mesmo arquivo Excel
df.to_excel(file_path, index=False)
print("Tabela atualizada com sucesso!")