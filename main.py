from fastapi import FastAPI
import pandas as pd
import os

app = FastAPI(title="SAT 69 & 69-B API", version="1.0")

# Intentar cargar los archivos CSV si ya existen en la carpeta data/
try:
    df_69 = pd.read_csv("data/art69.csv", dtype=str)
    df_69b = pd.read_csv("data/art69b.csv", dtype=str)
    df_69.columns = df_69.columns.str.strip()
    df_69b.columns = df_69b.columns.str.strip()
except Exception:
    df_69 = pd.DataFrame(columns=["RFC"])
    df_69b = pd.DataFrame(columns=["RFC"])

@app.get("/")
def inicio():
    return {"mensaje": "API del SAT Articulo 69 y 69-B funcionando correctamente"}

@app.get("/verificar/{rfc}")
def verificar_rfc(rfc: str):
    rfc_busqueda = rfc.upper().strip()
    
    en_69 = False
    if 'RFC' in df_69.columns:
        en_69 = rfc_busqueda in df_69['RFC'].str.upper().str.strip().values
        
    en_69b = False
    match_69b = pd.DataFrame()
    if 'RFC' in df_69b.columns:
        match_69b = df_69b[df_69b['RFC'].str.upper().str.strip() == rfc_busqueda]
        en_69b = not match_69b.empty
    
    situacion = "No encontrado"
    if en_69b:
        columnas_posibles = [col for col in match_69b.columns if 'situación' in col.lower() or 'estado' in col.lower()]
        if columnas_posibles:
            situacion = str(match_69b.iloc[0][columnas_posibles[0]])
        else:
            situacion = "Presunto/Definitivo (69-B)"
    elif en_69:
        situacion = "Listado Artículo 69"

    return {
        "rfc": rfc_busqueda,
        "en_articulo_69": en_69,
        "en_articulo_69b": en_69b,
        "estatus": situacion,
        "alerta": en_69 or en_69b
    }
