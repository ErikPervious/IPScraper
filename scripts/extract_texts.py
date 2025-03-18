import os
from pdf2image import convert_from_path
import pytesseract
from pycolor import print_color as print

def extract_texts(pdf_path):
    if pdf_path and not os.path.exists(pdf_path):
        print(f"Arquivo não encontrado: {pdf_path}", fg_color='red')
        exit()
    if not pdf_path:
        pdf_path = "documents/arquivo.pdf"
        if not os.path.exists(pdf_path):
            print(f"Arquivo padrão não encontrado: {pdf_path}", fg_color='red')
            exit()
        

    # Configura o caminho do executável do Tesseract
    pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"
    pytesseract.get_tesseract_version()
    
    # Caminho do poppler
    path_poppler = r"C:\poppler-24.08.0\Library\bin"

    # Saída do texto extraído
    output_text = "documents/extracted_texts.txt"
    
    # Caminho da pasta de imagens
    images_dir = "images"
    
    # Converte o PDF em imagens
    imagens = convert_from_path(pdf_path, poppler_path=path_poppler)
    
    # Cria a pasta de imagens, se ela não existir
    if not os.path.exists("images"):
        os.makedirs("images")

    print(f"Extraindo texto do arquivo '{pdf_path}'...", fg_color='green')
    
    with open(output_text, "w", encoding="utf-8") as output_file:
        for i, img in enumerate(imagens):
            # Salva a imagem na pasta especificada
            image_file = os.path.join("images", f"pagina_{i+1}.png")
            img.save(image_file, "PNG")
            
            # Extrai o texto da imagem
            texto = pytesseract.image_to_string(img, config="--psm 12")

            print(f"Extraindo texto da página {i+1}/{len(imagens)}", fg_color='grey23')
            
            output_file.write(f"\n\n### Página {i+1} ###\n\n")
            output_file.write(texto)
    
    print(f"Extração concluída! Texto salvo em '{output_text}' e imagens na pasta '{images_dir}'.", fg_color='green')


if __name__ == "__main__":
    extract_table("documents/arquivo.pdf")