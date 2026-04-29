import pandas as pd
from collections import Counter
import re
import os

# Carga de datos con ruta relativa para reproducibilidad en Colab
df = pd.read_csv("datos/comentarios.csv")

# Unimos todos los comentarios y los limpiamos
texto_completo = " ".join(df["comentario"].str.lower())
palabras = re.findall(r"[a-z]+", texto_completo)
frecuencia = Counter(palabras)

# Eliminamos palabras vacias que no aportan significado
stopwords = {"me", "el", "la", "lo", "un", "no", "muy", "al", "de",
             "en", "es", "le", "mi", "se", "si", "su", "y", "a"}
frecuencia_filtrada = {p: c for p, c in frecuencia.items()
                       if p not in stopwords and len(p) > 2}

top_palabras = sorted(frecuencia_filtrada.items(),
                      key=lambda x: x[1], reverse=True)[:10]

# Clasificacion por palabras clave simples
palabras_positivas = ["encanto", "excelente", "fantastico",
                      "buenisimo", "perfecto", "conforme", "buena"]
palabras_negativas = ["terrible", "malo", "pesimo", "basura",
                      "roto", "tardo", "gusto"]

def clasificar(comentario):
    # Devuelve Positivo, Negativo o Neutro segun palabras clave
    c = comentario.lower()
    if any(p in c for p in palabras_positivas):
        return "Positivo"
    elif any(p in c for p in palabras_negativas):
        return "Negativo"
    return "Neutro"

df["sentimiento"] = df["comentario"].apply(clasificar)

# Guardamos los resultados en /resultados
os.makedirs("resultados", exist_ok=True)
with open("resultados/informe.txt", "w") as f:
    f.write("=== ANALISIS DE COMENTARIOS ===\n\n")
    f.write("TOP 10 PALABRAS MAS FRECUENTES:\n")
    for palabra, count in top_palabras:
        f.write("  " + palabra + ": " + str(count) + "\n")
    f.write("\nCLASIFICACION DE COMENTARIOS:\n")
    for _, row in df.iterrows():
        f.write("  [" + row["sentimiento"] + "] " + row["comentario"] + "\n")

print("Analisis completado. Resultados guardados en /resultados")
print("Top palabras:", top_palabras)
print(df[["comentario", "sentimiento"]])
