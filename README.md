# PyWhois - Extração de Textos, Organização de IPs e Busca WHOIS

Este projeto permite a extração de textos de arquivos PDF, a organização de endereços IP em uma tabela Excel e a busca de informações WHOIS para esses IPs. Agora, ele oferece uma interface de menu interativa que simplifica o uso e permite a automação completa do processo.    

## Funcionalidades

O programa apresenta quatro opções principais acessíveis por meio de um menu interativo:    

1. **Extrair textos de um arquivo PDF**: Converte um PDF em texto e salva o resultado em um arquivo `.txt`.
2. **Organizar os IPs extraídos em uma tabela Excel**: Lê o arquivo de texto, extrai os IPs (IPv4 e IPv6) e os organiza em uma planilha Excel.
3. **Buscar informações de cada endereço IP**: Lê os IPs de uma planilha Excel e busca suas informações WHOIS, atualizando a planilha com os resultados.
4. **Fazer todas as etapas anteriores de uma só vez**: Executa automaticamente as etapas 1 a 3 em sequência, começando com um PDF e gerando uma planilha Excel com informações WHOIS.   

## Pré-requisitos

- **Tesseract OCR**: Necessário para a extração de texto de imagens. Instale e configure o caminho corretamente.
- **Poppler**: Usado para converter PDFs em imagens. Certifique-se de que está configurado no caminho adequado.
- **Bibliotecas Python**: Instale as dependências listadas em `requirements.txt` ou manualmente:
  ```bash
  pip install pandas pdf2image pytesseract pycolor ipwhois openpyxl
  ```

## Estrutura de Diretórios

O projeto está organizado da seguinte forma:

```
projeto/
├── main.py                # Arquivo principal com o menu interativo
├── scripts/               # Pasta com os scripts auxiliares
│   ├── extract_texts.py   # Etapa 1: Extrair textos do PDF
│   ├── filter_ips.py      # Etapa 2: Organizar IPs em Excel
│   └── search_ip_info.py  # Etapa 3: Buscar informações WHOIS
├── documents/             # Pasta para arquivos de entrada (PDFs e textos extraídos)       
└── databases/             # Pasta para arquivos de saída (planilhas Excel)
```

- Certifique-se de que as pastas `documents/` e `databases/` existam. Caso contrário, crie-as manualmente ou adicione este código no início do `main.py`:
  ```python
  import os
  os.makedirs("documents", exist_ok=True)
  os.makedirs("databases", exist_ok=True)
  ```

## Instruções de Uso

### Executando o Programa

1. **Inicie o programa** executando o arquivo `main.py`:
   ```bash
   python main.py
   ```

2. **Escolha uma opção** no menu interativo:
   - **Opção 1: Extrair textos de um arquivo PDF**
     - Forneça o caminho do PDF ou deixe em branco para usar o padrão (`documents/arquivo.pdf`).
   - **Opção 2: Organizar IPs em uma tabela Excel**
     - Forneça o caminho do arquivo de texto ou deixe em branco para usar o padrão (`documents/extracted_texts.txt`).
   - **Opção 3: Buscar informações WHOIS dos IPs**
     - Forneça o caminho do arquivo Excel ou deixe em branco para usar o padrão (`databases/Planilhamento de IPs.xlsx`).
   - **Opção 4: Executar todas as etapas em sequência**
     - Forneça o caminho do PDF ou deixe em branco para usar o padrão. O programa executará automaticamente as etapas 1 a 3.

3. **Acompanhe o progresso** por meio de mensagens coloridas no terminal, que indicam o status de cada operação.

### Detalhes das Etapas

- **Etapa 1: Extrair textos do PDF**
  - Converte o PDF em imagens e usa o Tesseract OCR para extrair o texto.
  - Salva o resultado em `documents/extracted_texts.txt`.

- **Etapa 2: Organizar IPs em uma tabela Excel**
  - Lê o arquivo de texto e extrai IPs (IPv4 e IPv6) usando expressões regulares.
  - Gera uma planilha Excel com a coluna "IP Address" (IPv4 seguido de IPv6).
  - Salva em `databases/Planilhamento de IPs.xlsx`.

- **Etapa 3: Buscar informações WHOIS**
  - Lê os IPs da coluna "IP Address" da planilha Excel.
  - Busca informações WHOIS em paralelo usando a biblioteca `ipwhois`.
  - Atualiza a planilha com os resultados na coluna "Whois Result".

- **Opção 4: Executar todas as etapas**
  - Automatiza o fluxo completo: extrai o texto do PDF, organiza os IPs e busca as informações WHOIS, gerando uma planilha atualizada.

## Notas Adicionais

- **Caminhos Padrão**: Se os caminhos não forem fornecidos, o programa usará:
  - PDF: `documents/arquivo.pdf`
  - Texto extraído: `documents/extracted_texts.txt`
  - Planilha Excel: `databases/Planilhamento de IPs.xlsx`

- **Feedback Visual**: Mensagens coloridas indicam o progresso e status das operações (requer a biblioteca `pycolor`).

- **Robustez**: O programa valida a existência de arquivos e colunas, exibindo mensagens de erro claras quando necessário.

## Alternativas de Uso (Legado)

As opções abaixo refletem os padrões de uso anteriores e podem ser úteis em cenários específicos:

### Extração via Chat Opice
1. Converter o documento `.pdf` para `.docx`.
2. Capturar as imagens que contêm tabelas do DOCX.
3. Enviar as imagens para o Chat Opice (chat com IA) para extrair, de forma estruturada, os dados das tabelas.
4. Gerar um arquivo Excel contendo o nome *'Planilhamento de IPs'* e com os IPs extraídos na coluna *'IP Address'*.
5. Executar o script `main.py` e escolher a opção 3 passando a localização do arquivo Excel gerado.
6. Caso ocorra erro (timeout ou outro), rode novamente o script `main.py` ou reporte o erro.