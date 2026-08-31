from fastapi import FastAPI
import pandas as pd
import os

app = FastAPI(title="SAT 69 & 69-B API", version="1.0")

# Cargar el archivo al iniciar la API de forma inteligente
try:
    path_69b = "data/art69b.csv"
    if os.path.exists(path_69b):
        # 1. Buscar en qué línea empiezan realmente los encabezados (donde dice RFC)
        skip_lines = 0
        with open(path_69b, 'r', encoding='latin1', errors='replace') as f:
            for i, line in enumerate(f):
                if 'RFC' in line.upper():
                    skip_lines = i
                    break
        
        # 2. Leer el CSV saltando el texto introductorio del SAT
        df_69b = pd.read_csv(path_69b, dtype=str, encoding='latin1', skiprows=skip_lines)
        df_69b.columns = df_69b.columns.str.strip()
    else:
        df_69b = pd.DataFrame()
except Exception as e:
    df_69b = pd.DataFrame()

@app.get("/")
def inicio():
    return {"mensaje": "API del SAT Articulo 69 y 69-B funcionando correctamente"}

@app.get("/verificar/{rfc}")
def verificar_rfc(rfc: str):
    rfc_busqueda = rfc.upper().strip()
    en_69b = False
    situacion = "No encontrado"
    
    if not df_69b.empty:
        # Buscar dinámicamente la columna del RFC
        col_rfc = next((col for col in df_69b.columns if 'RFC' in col.upper()), None)
        
        if col_rfc:
            # Encontrar el RFC exacto en la tabla
            match_69b = df_69b[df_69b[col_rfc].astype(str).str.upper().str.strip() == rfc_busqueda]
            en_69b = not match_69b.empty
            
            if en_69b:
                # Buscar dinámicamente la columna de situación o estado
                col_sit = next((col for col in match_69b.columns if 'SITUACI' in col.upper() or 'ESTADO' in col.upper()), None)
                situacion = str(match_69b.iloc[0][col_sit]).strip() if col_sit else "Definitivo (69-B)"

    # Generar alerta en color rojo si es definitivo o presunto
    es_alerta = en_69b
    if "DEFINITIVO" in situacion.upper() or "DEFINTIVO" in situacion.upper() or "PRESUNTO" in situacion.upper():
        es_alerta = True

    return {
        "rfc": rfc_busqueda,
        "en_articulo_69": False,
        "en_articulo_69b": en_69b,
        "estatus": situacion,
        "alerta": es_alerta
    }
