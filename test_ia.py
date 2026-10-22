import os
from dotenv import load_dotenv
import google.generativeai as genai

# Fuerza la relectura del .env ignorando variables viejas en memoria
load_dotenv(override=True)

llave = os.getenv("AP") or os.getenv("GOOGLE_API_KEY")
print("--- DIAGNÓSTICO DE IA ---")
print("1. Llave leída desde .env:", repr(llave))

if not llave:
    print("❌ ERROR: Python no encuentra la variable AP en el archivo .env")
else:
    try:
        genai.configure(api_key=llave.strip())
        modelo = genai.GenerativeModel("gemini-3.8-flash")
        respuesta = modelo.generate_content("Responde únicamente la palabra: Funciona")
        print("2. 🟢 ¡ÉXITO DE CONEXIÓN! Respuesta de Gemini:", respuesta.text)
    except Exception as e:
        print("2. 🔴 ERROR DEVUELTO POR LA API DE GOOGLE:")
        print(f"   Tipo: {type(e).__name__}")
        print(f"   Detalle: {e}")