import requests
import re
import pandas as pd
import html  # Para manejar caracteres especiales
import os  # Para manejar archivos y directorios

# 📌 Configuración
API_URL = "https://tramitacion.senado.cl/wspublico/tramitacion.php?boletin="
OUTPUT_DIR = "boletines_data"

# Crear la carpeta de salida si no existe
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 📌 Función para extraer el contenido de <descripcion>
def extraer_descripcion(xml_content):
    match = re.search(r"<descripcion>(.*?)</descripcion>", xml_content, re.DOTALL)
    if match:
        return html.unescape(match.group(1).strip())  # 🔹 Decodificar caracteres especiales
    return None

# 📌 Función para parsear <descripcion> en un diccionario
def parsear_descripcion(descripcion_xml):
    data = {}
    for campo in ["boletin", "titulo", "fecha_ingreso", "iniciativa", "camara_origen",
                  "urgencia_actual", "etapa", "subetapa", "leynro", "diariooficial",
                  "estado", "refundidos", "link_mensaje_mocion"]:
        match = re.search(rf"<{campo}>(.*?)</{campo}>", descripcion_xml, re.DOTALL)
        data[campo] = html.unescape(match.group(1).strip()) if match else None
    return data

# 📌 Leer los boletines desde un archivo CSV (o pedirlos manualmente)
archivo_boletines = "boletines_2023.xlsx"
try:
    df_boletines = pd.read_excel(archivo_boletines, engine="openpyxl")
    df_boletines.rename(columns={"N° Boletín": "boletin_id"}, inplace=True)
    boletines = df_boletines["boletin_id"].astype(str).str.split("-").str[0].tolist()  # 🔹 Extraer primeros 5 dígitos
except Exception as e:
    print(f"⚠️ No se pudo leer {archivo_boletines}: {e}")
    boletines = input("Ingrese los boletines separados por comas: ").split(",")

# 📌 Procesar cada boletín y guardar en una lista
data_proyectos = []

for boletin in boletines:
    boletin = boletin.strip()
    url = f"{API_URL}{boletin}"
    print(f"🔍 Consultando API con boletín {boletin}...")

    response = requests.get(url)

    if response.status_code == 200:
        xml_content = response.text.strip()

        # Extraer solo la parte de <descripcion>
        descripcion_xml = extraer_descripcion(xml_content)

        if descripcion_xml:
            # Parsear la información de <descripcion> y añadir a la lista
            data_proyecto = parsear_descripcion(descripcion_xml)
            data_proyectos.append(data_proyecto)
        else:
            print(f"⚠️ No se encontró la sección <descripcion> en el XML para boletín {boletin}.")
    else:
        print(f"⚠️ Error HTTP {response.status_code} al consultar el boletín {boletin}.")

# 📌 Guardar todos los datos en un solo archivo consolidado
df_final = pd.DataFrame(data_proyectos)
output_final_csv = os.path.join(OUTPUT_DIR, "proyectos_legislativos.csv")
output_final_json = os.path.join(OUTPUT_DIR, "proyectos_legislativos.json")

df_final.to_csv(output_final_csv, index=False, encoding="utf-8")
df_final.to_json(output_final_json, orient="records", indent=4, force_ascii=False)

print(f"📁 Archivo consolidado guardado en '{output_final_csv}' y '{output_final_json}'")
