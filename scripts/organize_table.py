import re
import pandas as pd


def organize_table(input_file='documents/extracted_texts.txt', output_clean='documents/extracted_texts_clean.txt',
                   output_trash='documents/extracted_texts_trash.txt'):
    def separate_content(text):
        # Padrão para matching de linhas da tabela (data no formato dd/mm/yyyy seguida por hora)
        table_pattern = r'^(\d{2}/\d{2}/\d{4}\s+\d{2}:\d{2}:\d{2}\s+[^\s]+\s+\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})$'
        # Padrão para o cabeçalho
        header_pattern = r'^Data\s+Hora\s+Email\s+IP$'

        # Divide o texto em linhas
        lines = text.split('\n')
        clean_lines = []
        removed_lines = []

        # Processa cada linha
        for line in lines:
            line = line.strip()
            if not line:  # Ignora linhas vazias
                continue

            # Verifica se é cabeçalho ou linha da tabela
            if re.match(header_pattern, line) or re.match(table_pattern, line):
                clean_lines.append(line)
            else:
                # Se não for o título da página (que já foi adicionado), adiciona às removidas
                if not line.startswith("### Página"):
                    removed_lines.append(line)

        return '\n'.join(clean_lines), '\n'.join(removed_lines)

    # Lê o arquivo original
    with open(input_file, 'r', encoding='utf-8') as file:
        original_text = file.read()

    # Separa o conteúdo em limpo e removido
    clean_text, removed_text = separate_content(original_text)

    # Salva o texto limpo
    with open(output_clean, 'w', encoding='utf-8') as file:
        file.write(clean_text)

    # Cria DataFrame e salva como CSV
    lines = clean_text.split('\n')
    data = []
    header = []
    for line in lines:
        if re.match(r'^Data\s+Hora\s+Email\s+IP$', line):
            header = ['Date and Hour (GMT -0)', 'Email', 'IP']
        elif line.strip():
            fields = line.split()
            if len(fields) >= 4:
                datetime = f"{fields[0]} {fields[1]} UTC"
                data.append([datetime, fields[2], fields[3]])

    if data:
        df = pd.DataFrame(data, columns=header)
        csv_path = output_clean.replace('.txt', '.csv')
        df.to_csv(csv_path, sep='$', index=False, encoding='utf-8')

    # Salva o conteúdo removido
    with open(output_trash, 'w', encoding='utf-8') as file:
        file.write("### Removed Content ###\n\n")
        file.write(removed_text)

    # Verifica IPs no arquivo extracted_texts_trash.txt
    with open(output_trash, 'r', encoding='utf-8') as file:
        trash_lines = file.readlines()
        ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
        for i, line in enumerate(trash_lines, 1):
            if re.search(ip_pattern, line):
                print(f"\nPossível IP encontrado na linha {i} do arquivo trash.txt:")
                print(f"Linha: {line.strip()}")

    print("\nProcessing completed!")
    print(f"- Clean table saved to: {output_clean}")
    print(f"- CSV file saved to: {csv_path}")
    print(f"- Removed content saved to: {output_trash}")


if __name__ == "__main__":
    organize_table()
