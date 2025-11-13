import streamlit as st
import pandas as pd
from datetime import date
import os

# --- Configuration ---
# Define export directory
EXPORT_DIR = "Wertpapier_transaktionen"
os.makedirs(EXPORT_DIR, exist_ok=True)

year = date.today().year
excel_path = os.path.join(EXPORT_DIR, f"Wertpapieruebersicht_{year}.xlsx")

# --- Streamlit UI ---
# Use a reliable icon: either an emoji or a local PNG
# Option 1: emoji (most browsers support 📊)
# Option 2: local icon file: put 'icon.png' in the same folder and use page_icon="icon.png"
st.set_page_config(page_title="Wertpapier Transaktionen", page_icon="📊", layout="wide")


st.title("Wertpapier Transaktionen 📊")

with st.form("transaktion_form"):
    datum = st.date_input("Datum", value=date.today())
    firma = st.text_input("Firma")
    typ = st.selectbox("Typ", ["Einkauf", "Verkauf"])
    art = st.selectbox(
        "Art",
        [
            "Aktienwerte", "Aktienfonds", "Rentenwerte", "Rentenfonds",
            "Mischfonds", "Sonstige Werte", "Sonstige Fonds",
        ],
    )
    anzahl = st.number_input("Anzahl", step=1, min_value=1)
    preis = st.number_input("Preis (€)", step=0.01)
    gebuehr = st.number_input("Gebühr (€)", step=0.01)
    submitted = st.form_submit_button("✅ Transaktion speichern")

# --- Save transaction ---
if submitted:
    if not firma.strip():
        st.error("Bitte Firma eingeben.")
    else:
        new_row = {
            "Datum": datum.strftime("%d-%m-%Y"),
            "Firma": firma,
            "Typ": typ,
            "Art": art,
            "Anzahl": int(anzahl),
            "Preis": float(preis),
            "Gebühr": float(gebuehr),
            "Gesamtpreis": anzahl * preis + gebuehr,
        }

        try:
            df = pd.read_excel(excel_path) if os.path.exists(excel_path) else pd.DataFrame()
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            df.to_excel(excel_path, index=False)
            st.success(f"✅ Gespeichert: {os.path.basename(excel_path)}")
        except PermissionError:
            st.error("❌ Datei ist möglicherweise geöffnet. Bitte schließen Sie sie.")
        except Exception as e:
            st.error(f"❌ Fehler: {e}")

# --- Display current transactions ---
st.subheader("Aktuelle Transaktionen 📋")
if os.path.exists(excel_path):
    try:
        df_display = pd.read_excel(excel_path)
        st.dataframe(df_display, use_container_width=True)

        total_einkauf = df_display[df_display["Typ"] == "Einkauf"]["Gesamtpreis"].sum()
        total_verkauf = df_display[df_display["Typ"] == "Verkauf"]["Gesamtpreis"].sum()
        total_gebuehr = df_display["Gebühr"].sum()
        st.write(f"**Gesamt Einkauf:** €{total_einkauf:.2f}")
        st.write(f"**Gesamt Verkauf:** €{total_verkauf:.2f}")
        st.write(f"**Gesamt Gebühren:** €{total_gebuehr:.2f}")
    except Exception as e:
        st.error(f"❌ Fehler beim Laden der Daten: {e}")
else:
    st.info("Noch keine Transaktionen erfasst.")

