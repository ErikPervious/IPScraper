import io

# Converter texto extraído em DataFrame (simples, para tabelas bem estruturadas)
df = pd.read_csv(io.StringIO(extracted_text), sep="\t")

print(df)
df.to_csv("tabela_extraida.csv", index=False)
