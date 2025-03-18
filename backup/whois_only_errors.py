import pandas as pd
from ipwhois import IPWhois
from concurrent.futures import ThreadPoolExecutor, as_completed

# Caminho do arquivo Excel
file_path = 'C:/Users/ErikMatheusFernandes/Desktop/python-extract-pdftable/databases/Planilhamento de IPs (Todos Inclusos).xlsx'

# Carrega a tabela do Excel
df = pd.read_excel(file_path)

# Verifica se a coluna "Whois Result" existe; se não, cria
if 'Whois Result' not in df.columns:
    df['Whois Result'] = ''
df['Whois Result'] = df['Whois Result'].astype('object')  # Garante que a coluna seja tratada como texto

# Função para verificar se o resultado é um erro específico que deve ser reprocessado
def is_specific_error(result):
    if isinstance(result, str) and result.startswith('Erro:'):
        if 'Rate limit exceeded' in result or 'error code 503' in result:
            return True
    return False

# Cria uma máscara para identificar as linhas com erros específicos
mask = df['Whois Result'].apply(is_specific_error)

# Coleta os IPs das linhas que precisam ser reprocessadas
ips_to_process = df.loc[mask, 'IP Address'].astype(str).tolist()

# Se não houver IPs para processar, apenas avisa e encerra
if not ips_to_process:
    print("Nenhum IP precisa ser reprocessado.")
else:
    # Função para obter informações WHOIS (mantida igual ao original)
    def get_whois_info(ip):
        try:
            obj = IPWhois(ip, timeout=10)
            result = obj.lookup_rdap()
            
            if not result or 'network' not in result:
                return ip, "Erro: Nenhum dado de rede retornado pela consulta WHOIS"
            
            whois_data = {
                'provider': 'N/A',
                'location': 'N/A',
                'email': 'N/A',
                'asn_description': 'N/A',
                'ip_version': 'N/A',
                'cnpj_cpf': 'N/A'
            }
            
            if result.get('entities') and result.get('objects'):
                for entity in result['objects'].values():
                    if 'roles' in entity and 'registrant' in entity['roles']:
                        whois_data['provider'] = entity.get('contact', {}).get('name', 'N/A')
                        whois_data['cnpj_cpf'] = entity.get('handle', 'N/A')
                        break
            if whois_data['provider'] == 'N/A' and result['network'].get('name'):
                whois_data['provider'] = result['network']['name']

            if result['network'].get('country'):
                whois_data['location'] = result['network']['country']
            elif result.get('asn_country_code'):
                whois_data['location'] = result['asn_country_code']

            if result.get('entities') and result.get('objects'):
                for entity in result['objects'].values():
                    if 'contact' in entity and entity['contact'].get('email'):
                        whois_data['email'] = entity['contact']['email'][0]['value']
                        break

            if result.get('asn_description'):
                whois_data['asn_description'] = result['asn_description']

            if result['network'].get('ip_version'):
                whois_data['ip_version'] = result['network']['ip_version']

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

    # Função para processar IPs em paralelo (mantida igual ao original)
    def process_ips_in_parallel(ips):
        results = {}
        with ThreadPoolExecutor(max_workers=10) as executor:
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

    # Processa os IPs selecionados em paralelo
    results = process_ips_in_parallel(ips_to_process)

    # Atualiza o DataFrame com os novos resultados
    for ip, whois_result in results.items():
        df.loc[df['IP Address'].astype(str) == ip, 'Whois Result'] = whois_result

    # Salva a tabela atualizada
    df.to_excel(file_path, index=False)
    print("Tabela atualizada com sucesso!")