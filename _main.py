from pycolor import print_color as print
from os import system
import sys

from scripts.extract_texts import extract_texts
from scripts.filter_ips import filter_ips
from scripts.search_ip_info import search_ip_info
from scripts.organize_table import organize_table

system('cls')
print('Bem vindo(a) ao PyWhois', fg_color='white')
print('''
1. Você pode extrair os textos de um arquivo PDF.
2. Organizar os IPs extraídos em uma tabela Excel.
3. Buscar informações de cada endereço IP.
4. Organizar a tabela do arquivo txt.
5. Fazer todas as etapas anteriores de uma só vez.
''', fg_color='white')

print('\nPara começarmos, escolha uma das opções acima passando o número ou deixe em branco para sair.')
print('Exemplo, digite "4" para executar todas as etapas.', fg_color='grey23')
user_choice = input('\n--> ')

if user_choice == '1':
  system('cls')
  print('Opção 1 selecionada (extrair textos de um arquivo pdf)', fg_color='green')
  print('Digite o caminho do arquivo PDF que deseja extrair os IPs, ou deixe em branco para usar o padrão (documents/arquivo.pdf)')
  pdf_file = input('\n--> ')
  extract_texts(pdf_file)
  organize = input('Deseja organizar os dados extraídos? (s/n)')
  if organize == 's':
    organize_table()
elif user_choice == '2':
  system('cls')
  print('Opção 2 selecionada (organizar IPs em uma tabela Excel)', fg_color='green')
  print('Digite o caminho do arquivo de texto que contém os IPs, ou deixe em branco para usar o padrão (documents/extracted_texts.txt)')
  txt_file = input('\n--> ')
  filter_ips(txt_file)
elif user_choice == '3':
  system('cls')
  print('Opção 3 selecionada (buscar informações de cada endereço IP)', fg_color='green')
  print('Digite o caminho do arquivo Excel que contém os IPs, ou deixe em branco para usar o padrão (databases/Planilhamento de IPs.xlsx)')
  excel_file = input('\n--> ')
  search_ip_info(excel_file)
elif user_choice == '4':
  system('cls')
  print("Opção 4 selecionada (organizar a tabela do arquivo txt)")
  organize_table()
elif user_choice == '5':
  system('cls')  # Limpa a tela (funciona no Windows; use 'clear' no Linux/Mac)
  print('Opção 5 selecionada (executar todas as etapas)', fg_color='green')
  print('Digite o caminho do arquivo PDF, ou deixe em branco para usar o padrão (documents/arquivo.pdf)')
  pdf_file = input('\n--> ')

  # Define caminhos padrão
  default_pdf_path = "documents/old/arquivo.pdf"
  txt_path = "documents/07-05-2025/extracted_texts.txt"
  excel_path = "databases/Planilhamento de IPs.xlsx"

  # Usa o caminho fornecido ou o padrão para o PDF
  pdf_path = pdf_file or default_pdf_path

  # Etapa 1: Extrair textos do PDF
  print("Iniciando Etapa 1: Extrair textos do PDF...", fg_color='green')
  extract_texts(pdf_path)
  print("Etapa 1 concluída!", fg_color='green')

  # Etapa 2: Organizar IPs em uma tabela Excel
  print("Iniciando Etapa 2: Organizar IPs em uma tabela Excel...", fg_color='green')
  filter_ips(txt_path)
  print("Etapa 2 concluída!", fg_color='green')

  # Etapa 3: Buscar informações WHOIS
  print("Iniciando Etapa 3: Buscar informações WHOIS...", fg_color='green')
  search_ip_info(excel_path)
  print("Etapa 3 concluída!", fg_color='green')

  print("Todas as etapas foram concluídas com sucesso!", fg_color='green')