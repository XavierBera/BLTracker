
import streamlit as st
import requests
import pandas as pd

# Título de la aplicación
st.set_page_config(page_title="Breadline Tracker", layout="wide")
st.title("📊 Breadline Tracker - Berachain")

# Dirección de la wallet (por ahora fija)
address = "0x5487cb78417aa5923b80cdcf046a6554ca395874"
url = f"https://api.berascan.com/api/txs?a={address}&p=1"

# Obtener datos desde la API de Berascan (reemplazar si hay API oficial en el futuro)
headers = {
    "User-Agent": "Mozilla/5.0"
}

try:
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    data = response.json()
    txs = data.get("txs", [])
except Exception as e:
    st.error(f"Error al obtener los datos: {e}")
    st.stop()

# Procesar las transacciones que parecen ser entradas a la Breadline
breadline_data = []
for tx in txs:
    if "breadline" in tx.get("method", "").lower() or "ticket" in tx.get("method", "").lower():
        breadline_data.append({
            "Wallet": tx.get("from"),
            "Hash": tx.get("hash"),
            "Fecha": tx.get("timestamp"),
            "Monto (BERA)": float(tx.get("value", 0)) / 1e18,
            "Tickets": round(float(tx.get("value", 0)) / 0.69e18, 2)
        })

# Crear DataFrame
df = pd.DataFrame(breadline_data)
df["Fecha"] = pd.to_datetime(df["Fecha"], unit='s')
df = df.sort_values(by="Fecha", ascending=False)

# Mostrar tabla
st.dataframe(df, use_container_width=True)
