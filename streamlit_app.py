import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. Konfiguration
st.set_page_config(page_title="Reisetagebuch", page_icon="🌍")

# 2. Dein Link (sauber ohne Leerzeichen am Rand)
URL = "https://docs.google.com/spreadsheets/d/1MPlJAMMUJQA0OXLQj-y0p6rS8pL1ZAn-xW6O9p8vUxE/edit?usp=sharing"
MEIN_TABELLEN_LINK = URL.strip()
BLATT_NAME = "Tabelle1"

st.title("🌍 Unser Familien-Reisetagebuch")

conn = st.connection("gsheets", type=GSheetsConnection)

with st.form(key="reise_form"):
    datum = st.date_input("Wann?", value=pd.to_datetime("today"))
    wer = st.selectbox("Wer schreibt?", ["Mama", "Papa", "Daliyah", "Kind 1", "Kind 2"])
    ort = st.text_input("Wo sind wir?")
    stimmung = st.select_slider("Stimmung", options=["😢", "😐", "🙂", "🤩", "🚀"])
    erlebnis = st.text_area("Was ist passiert?")
    submit = st.form_submit_button(label="Erinnerung speichern! ✨")

if submit:
    try:
        # Bestehende Daten lesen
        df = conn.read(spreadsheet=MEIN_TABELLEN_LINK, worksheet=BLATT_NAME)
        
        # Neuen Eintrag erstellen
        new_row = pd.DataFrame([{"Datum": str(datum), "Name": wer, "Ort": ort, "Stimmung": stimmung, "Erlebnis": erlebnis}])
        
        # Daten zusammenfügen
        if df is not None and not df.empty:
            updated_df = pd.concat([df, new_row], ignore_index=True)
        else:
            updated_df = new_row
            
        # Speichern
        conn.update(spreadsheet=MEIN_TABELLEN_LINK, worksheet=BLATT_NAME, data=updated_df)
        
        st.balloons()
        st.success("Gespeichert! Italien kann kommen! 🇮🇹")
        st.rerun()
    except Exception as e:
        st.error(f"Oh weh, da gab es ein Problem: {e}")

# Anzeige der bisherigen Abenteuer
st.divider()
st.subheader("📖 Unsere bisherigen Abenteuer")
try:
    data = conn.read(spreadsheet=MEIN_TABELLEN_LINK, worksheet=BLATT_NAME)
    if data is not None and not data.empty:
        st.dataframe(data.iloc[::-1], use_container_width=True)
except:
    st.info("Schreib den ersten Eintrag!")
    
