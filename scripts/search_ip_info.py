import os
import pandas as pd
from ipwhois import IPWhois
from concurrent.futures import ThreadPoolExecutor, as_completed
from pycolor import print_color as print
import time

def search_ip_info(excel_path=None):
    """
    Busca informações WHOIS para IPs em um arquivo Excel e atualiza a coluna 'Whois Result'.
    
    Parâmetros:
        excel_path (str, opcional): Caminho do arquivo Excel. Se None, usa o padrão.
    """
    # Define o caminho padrão se nenhum for fornecido
    default_path = "databases/Planilhamento de IPs.xlsx"
    excel_path = excel_path or default_path

    # Valida a existência do arquivo
    if not os.path.exists(excel_path):
        print(f"Erro: Arquivo '{excel_path}' não encontrado.", fg_color='red')
        exit()

    # Mensagem de carregamento
    print(f"Carregando tabela do Excel '{excel_path}'...", fg_color='green')

    # Carrega o DataFrame
    df = pd.read_excel(excel_path)

    # Verifica se a coluna "IP Address" existe
    if 'IP Address' not in df.columns:
        print("Erro: Coluna 'IP Address' não encontrada no arquivo Excel.", fg_color='red')
        exit()

    # Cria a coluna "Whois Result" se não existir
    if 'Whois Result' not in df.columns:
        df['Whois Result'] = ''
    df['Whois Result'] = df['Whois Result'].astype('object')  # Garante tipo correto

    # Função para obter informações WHOIS de um IP
    def get_whois_info(ip):
        try:
            start_time = time.time()
            obj = IPWhois(ip, timeout=10)  # Timeout global de 10 segundos
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

            # Extrai provedor e CNPJ/CPF
            if result.get('entities') and result.get('objects'):
                for entity in result['objects'].values():
                    if 'roles' in entity and 'registrant' in entity['roles']:
                        whois_data['provider'] = entity.get('contact', {}).get('name', 'N/A')
                        whois_data['cnpj_cpf'] = entity.get('handle', 'N/A')
                        break
            if whois_data['provider'] == 'N/A' and result['network'].get('name'):
                whois_data['provider'] = result['network']['name']

            # Localização
            whois_data['location'] = result['network'].get('country') or result.get('asn_country_code', 'N/A')

            # Email
            if result.get('entities') and result.get('objects'):
                for entity in result['objects'].values():
                    if 'contact' in entity and entity['contact'].get('email'):
                        whois_data['email'] = entity['contact']['email'][0]['value']
                        break

            # ASN e versão do IP
            whois_data['asn_description'] = result.get('asn_description', 'N/A')
            whois_data['ip_version'] = result['network'].get('ip_version', 'N/A')

            result_str = (
                f"Provider: {whois_data['provider']}, "
                f"Location: {whois_data['location']}, "
                f"Email: {whois_data['email']}, "
                f"ASN Description: {whois_data['asn_description']}, "
                f"IP Version: {whois_data['ip_version']}, "
                f"CNPJ/CPF: {whois_data['cnpj_cpf']}"
            )
            elapsed_time = time.time() - start_time
            return ip, f"{result_str} (Tempo: {elapsed_time:.2f}s)"
        except Exception as e:
            return ip, f"Erro: {str(e)}"

    # Processa IPs em paralelo com timeout por tarefa
    def process_ips_in_parallel(ips):
        results = {}
        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_ip = {executor.submit(get_whois_info, ip): ip for ip in ips}
            total_ips = len(ips)
            processed_count = 0

            for future in as_completed(future_to_ip):
                ip = future_to_ip[future]
                processed_count += 1
                try:
                    ip, result = future.result(timeout=15) 
                    results[ip] = result
                    print(f"[{processed_count}/{total_ips}] Processado IP: {ip} - {result}", fg_color='grey23')
                except Exception as e:
                    results[ip] = f"Erro: {str(e)}"
                    print(f"[{processed_count}/{total_ips}] Processado IP: {ip} - Resultado: Erro: {str(e)}", fg_color='red')
        return results

    # Coleta IPs da coluna "IP Address"
    ips = df['IP Address'].astype(str).tolist()
    print(f"Total de IPs a processar: {len(ips)}", fg_color='green')

    # Inicia a busca WHOIS
    print("Iniciando busca WHOIS para os IPs...", fg_color='green')
    results = process_ips_in_parallel(ips)

    # Atualiza o DataFrame
    print("Atualizando tabela com resultados...", fg_color='green')
    for ip, whois_result in results.items():
        df.loc[df['IP Address'].astype(str) == ip, 'Whois Result'] = whois_result

    # Salva o arquivo Excel
    df.to_excel(excel_path, index=False)
    print(f"Busca WHOIS concluída! Tabela atualizada em '{excel_path}'.", fg_color='green')

if __name__ == "__main__":
    search_ip_info("C:/Users/ErikMatheusFernandes/Desktop/python-extract-pdftable/Planilhamento de IPs (Apenas Erros).xlsx")