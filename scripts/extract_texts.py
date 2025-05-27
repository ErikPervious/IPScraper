import os
from pdf2image import convert_from_path
import pytesseract
from pycolor import print_color as print
import pdfplumber

def extract_texts(pdf_path):
    if pdf_path and not os.path.exists(pdf_path):
        print(f"Arquivo não encontrado: {pdf_path}", fg_color='red')
        exit()
    if not pdf_path:
        pdf_path = "documents/arquivo.pdf"
        if not os.path.exists(pdf_path):
            print(f"Arquivo padrão não encontrado: {pdf_path}", fg_color='red')
            exit()

    print("Carregando arquivo PDF...", fg_color='green')

    # Configura o caminho do executável do Tesseract
    pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"
    pytesseract.get_tesseract_version()
    
    # Caminho do poppler
    path_poppler = r"C:\PythonLibs\poppler-24.08.0\Library\bin"

    # Saída do texto extraído
    output_text = "documents/extracted_texts.txt"
    output_csv = "documents/extracted_tables.csv"
    
    # Caminho da pasta de imagens
    images_dir = "images"
    
    # Converte o PDF em imagens
    imagens = convert_from_path(pdf_path, poppler_path=path_poppler)
    
    # Cria a pasta de imagens, se ela não existir
    if not os.path.exists("images"):
        os.makedirs("images")

    print(f"Extraindo texto do arquivo '{pdf_path}'...", fg_color='green')

    print("""
    Existem duas opções para extrair texto de um PDF:

    i - Usando OCR (Optical Character Recognition):
        - Converte o PDF em imagens e depois extrai o texto dessas imagens
        - Melhor para PDFs que são digitalizações ou contêm texto como imagem
        - Mais lento mas pode reconhecer texto em imagens

    t - Extração direta de texto e tabelas:
        - Extrai o texto e tabelas diretamente do PDF se ele contiver texto selecionável
        - Mais rápido e preciso para PDFs com texto nativo
        - Não funciona para texto em imagens ou PDFs digitalizados
    """, fg_color='white')
    
    option = input("Deseja extrair imagem ou texto? (i/t):")
    
    if option == "i":
        with open(output_text, "w", encoding="utf-8") as output_file:
            for i, img in enumerate(imagens):
                # Salva a imagem na pasta especificada
                image_file = os.path.join("images", f"pagina_{i+1}.png")
                img.save(image_file, "PNG")

                # Extrai o texto da imagem
                texto = pytesseract.image_to_string(img, config="--psm 6")

                print(f"Extraindo texto da página {i+1}/{len(imagens)}", fg_color='grey23')

                output_file.write(f"\n\n### Página {i+1} ###\n\n")
                output_file.write(texto)
                
    elif option == "t":
        with pdfplumber.open(pdf_path) as pdf:
            with open(output_text, "w", encoding="utf-8") as output_file:
                for i, page in enumerate(pdf.pages):
                    print(f"Extraindo conteúdo da página {i + 1}/{len(pdf.pages)}", fg_color='grey23')

                    # Extrai tabelas da página
                    tables = page.extract_tables()
                    
                    output_file.write(f"\n\n### Página {i + 1} ###\n\n")
                    
                    if tables:
                        output_file.write("=== TABELAS ENCONTRADAS ===\n\n")
                        for table_num, table in enumerate(tables, 1):
                            output_file.write(f"--- Tabela {table_num} ---\n")
                            # Formata cada linha da tabela
                            for row in table:
                                # Remove valores None e espaços em branco
                                row = ['' if cell is None else str(cell).strip() for cell in row]
                                # Une as células com tabulação
                                output_file.write('\t'.join(row) + '\n')
                            output_file.write('\n')
                    
                    # Extrai o texto normal da página
                    texto = page.extract_text()
                    if texto:
                        output_file.write("=== TEXTO ===\n")
                        output_file.write(texto + '\n')

    print(f"Extração concluída! Conteúdo salvo em '{output_text}'", fg_color='green')
    if option == "t":
        print(f"As tabelas foram formatadas com tabulação para melhor visualização", fg_color='green')

if __name__ == "__main__":
    extract_texts("C:\Projects\Projects\python-extract-pdftable\documents\07-05-2025\DOC.01 - Fuso GMT -3 - 1014990-96.2025.8.26.0100.pdf")