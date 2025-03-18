import pytesseract
from pdf2image import convert_from_path
import cv2
import numpy as np
import pandas as pd

# Se estiver no Windows, defina o caminho do Tesseract
pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"

# Caminho para Poppler no Windows (ajuste para o seu caminho correto)
path_poppler = r"C:\poppler-24.08.0\Library\bin"

# Converter PDF para imagens
pdf_path = "C:/Users/ErikMatheusFernandes/Desktop/python-extract-pdftable/arquivo.pdf"
images = convert_from_path(pdf_path, poppler_path=path_poppler)

# Processar cada página do PDF
for i, image in enumerate(images):
    # Converter a imagem para numpy array
    image_np = np.array(image)
    
    # Converter para escala de cinza
    gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)

    # Aplicar threshold para melhorar o reconhecimento do OCR
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Extrair texto da imagem usando Tesseract OCR
    extracted_text = pytesseract.image_to_string(thresh, config="--psm 12")

    print(f"Texto extraído da página {i + 1}:\n")
    print(extracted_text)

    # Você pode salvar a saída em um arquivo .txt para análise
    with open(f"pagina_{i + 1}.txt", "w", encoding="utf-8") as f:
        f.write(extracted_text)
