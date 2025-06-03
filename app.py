import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL objetivo (reemplazá la wallet si cambia)
URL = "https://berascan.com/txs?a=0x5487cb78417aa5923b80cdcf046a6554ca395874&p=1"

def obtener_datos():
    try:
        response = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        table = soup.find("table")
        if not table:
            raise ValueError("No se encontró la tabla en la página.")

        rows = table.find("tbody").find_all("tr")
        data = []
        for row in rows:
            cols = row.find_all("td")
            if len(cols) >= 5:
                data.append({
                    "Wallet": cols[0].get_text(strip=True),
                    "Position": cols[1].get_text(strip=True),
                    "NFT ID": cols[2].get_text(strip=True),
                    "Count": cols[3].get_text(strip=True),
                    "SP": cols[4].get_text(strip=True),
                })
        return pd.DataFrame(data)
    except Exception as e:
        st.error(f"Error al obtener los datos: {e}")
        return pd.DataFrame()

st.set_page_config(page_title="Breadline Tracker - Berachain", layout="wide")
st.title("📊 Breadline Tracker - Berachain")
st.markdown("Visualización de posiciones dentro de la Breadline en Berascan.")

df = obtener_datos()
if not df.empty:
    st.dataframe(df)
