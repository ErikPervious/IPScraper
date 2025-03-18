import os
import re
import pandas as pd
from pycolor import print_color as print

def filter_ips(txt_path):
    # Verifica se o caminho fornecido existe; se não, usa o padrão
    if txt_path and not os.path.exists(txt_path):
        print(f"Arquivo não encontrado: {txt_path}", fg_color='red')
        exit()
    if not txt_path:
        txt_path = "documents/extracted_texts.txt"
        if not os.path.exists(txt_path):
            print(f"Arquivo padrão não encontrado: {txt_path}", fg_color='red')
            exit()

    # Mensagem inicial
    print(f"Lendo arquivo de texto '{txt_path}'...", fg_color='green')

    # Lê o conteúdo do arquivo de texto
    with open(txt_path, "r", encoding="utf-8") as file:
        texto = file.read()

    # Extrai IPs com expressões regulares
    print("Extraindo IPs do texto...", fg_color='grey23')
    regex_ipv4 = r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
    regex_ipv6 = r"\b(?:[A-Fa-f0-9]{1,4}:){7}[A-Fa-f0-9]{1,4}\b"
    ips_v4 = re.findall(regex_ipv4, texto)
    ips_v6 = re.findall(regex_ipv6, texto)
    all_unique_ips = list(dict.fromkeys(ips_v4 + ips_v6))

    # Exibe o número de IPs encontrados
    print(f"IPs encontrados: IPv4: {len(ips_v4)}, IPv6: {len(ips_v6)}", fg_color='grey23')

    # Exibe os IPs únicos
    print(f"IPs únicos encontrados: {len(all_unique_ips)}", fg_color='grey23')

    # Organiza os IPs em uma única lista, IPv4 primeiro, depois IPv6
    all_ips = all_unique_ips

    # Verifica se há IPs para salvar
    if not all_ips:
        print("Nenhum IP encontrado para organizar.", fg_color='red')
        exit()

    # Organiza os IPs em uma tabela Excel
    print("Salvando IPs em uma tabela Excel...", fg_color='grey23')
    excel_path = "databases/Planilhamento de IPs.xlsx"

    # Cria um DataFrame com uma única coluna "IP Address"
    df = pd.DataFrame(all_ips, columns=["IP Address"])

    # Garante que a coluna seja do tipo string para evitar problemas de tipo
    df["IP Address"] = df["IP Address"].astype(str)

    # Salva o DataFrame em um arquivo Excel
    df.to_excel(excel_path, index=False)

    # Mensagem de conclusão
    print(f"Organização concluída! Tabela salva em '{excel_path}'.", fg_color='green')

if __name__ == "__main__":
    filter_ips("documents/extracted_texts.txt")