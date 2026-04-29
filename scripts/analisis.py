import pandas as pd
import os

# Cargo el archivo CSV con los comentarios
df = pd.read_csv("datos/comentarios.csv")

# Uno todos los comentarios en un solo texto
texto_completo = ""
for comentario in df["comentario"]:
    texto_completo = texto_completo + " " + comentario.lower()

# Separo el texto en palabras individuales
todas_las_palabras = texto_completo.split()

# Palabras que no me interesan contar (palabras vacias)
stopwords = ["me", "el", "la", "lo", "un", "no", "muy", "al", "de",
             "en", "es", "le", "mi", "se", "si", "su", "y", "a"]

# Cuento cuantas veces aparece cada palabra
frecuencia = {}
for palabra in todas_las_palabras:
    if palabra not in stopwords and len(palabra) > 2:
        if palabra in frecuencia:
            frecuencia[palabra] = frecuencia[palabra] + 1
        else:
            frecuencia[palabra] = 1

# Ordeno las palabras de mayor a menor frecuencia y tomo las 10 primeras
top_palabras = sorted(frecuencia.items(), key=lambda x: x[1], reverse=True)[:10]

# Listas de palabras para clasificar comentarios
positivas = ["encanto", "excelente", "fantastico", "buenisimo", "perfecto", "conforme", "buena"]
negativas = ["terrible", "malo", "pesimo", "basura", "roto", "tardo", "gusto"]

# Clasifico cada comentario revisando si contiene palabras clave
resultados_sentimiento = []

for comentario in df["comentario"]:
    comentario_minuscula = comentario.lower()
    sentimiento = "Neutro"

    for palabra in positivas:
        if palabra in comentario_minuscula:
            sentimiento = "Positivo"
            break

    for palabra in negativas:
        if palabra in comentario_minuscula:
            sentimiento = "Negativo"
            break

    resultados_sentimiento.append(sentimiento)

df["sentimiento"] = resultados_sentimiento

# Guardo los resultados en un archivo de texto
os.makedirs("resultados", exist_ok=True)
archivo = open("resultados/informe.txt", "w")
archivo.write("=== ANALISIS DE COMENTARIOS ===\n\n")
archivo.write("TOP 10 PALABRAS MAS FRECUENTES:\n")

for palabra, count in top_palabras:
    archivo.write("  " + palabra + ": " + str(count) + "\n")

archivo.write("\n

#Se ha utilizado la IA para algunas cosas, como la parte de guardar resultados en archivos, dado que un no tengo ese conocimiento