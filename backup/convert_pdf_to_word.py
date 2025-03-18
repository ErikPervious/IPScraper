from pdf2docx import Converter

def convert_pdf_to_word(pdf_file, docx_file):
    # Cria um conversor
    cv = Converter(pdf_file)
    
    # Converte o PDF para o arquivo Word (docx)
    cv.convert(docx_file, start=0, end=None)  # Converte do início ao fim do PDF
    
    # Finaliza o processo de conversão
    cv.close()

# Exemplo de uso
pdf_file = 'C:/Users/ErikMatheusFernandes/Desktop/python-extract-pdftable/documents/arquivo.pdf'  # Caminho para o arquivo PDF de entrada
docx_file = 'C:/Users/ErikMatheusFernandes/Desktop/python-extract-pdftable/documents/arquivo.docx'  # Caminho para o arquivo Word de saída

convert_pdf_to_word(pdf_file, docx_file)
