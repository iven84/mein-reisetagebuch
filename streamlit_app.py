 import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. Konfiguration (Browser-Übersetzung bitte ausschalten!)
st.set_page_config(page_title="Reisetagebuch", page_icon="🌍")

# 2. DEIN LINK - Absolut sauber ohne Leerzeichen!
# Falls dein Browser "Import" oder "aus" schreibt -> bitte manuell korrigieren!
URL = "https://docs.google.com/spreadsheets/d/1aIMSYHxw89-d-FIqsxq9FQJLrrROVdmYceABxglZmq8/edit?usp=sharing"
MEIN_TABELLEN_LINK = URL.strip()
BLATT_NAME = "Tabelle1"

st.title("🌍 Unser Familien-Reisetagebuch")

conn = st.connection("gsheets", type=GSheetsConnection)

with st.form(key="reise_form"):
    datum = st.date_input("Wann?", value=pd.to_datetime("today"))
    name = st.selectbox("Wer schreibt?", ["Mama", "Papa", "Daliyah", "Kind 1", "Kind 2"])
    ort = st.text_input("Wo sind wir?")
    stimmung = st.select_slider("Stimmung", options=["😢", "😐", "🙂", "🤩", "🚀"])
    erlebnis = st.text_area("Was ist passiert?")
    submit = st.form_submit_button(label="Erinnerung speichern! ✨")

if submit:
    try:
        # Daten lesen
        df = conn.read(spreadsheet=MEIN_TABELLEN_LINK, worksheet=BLATT_NAME)
        
        # Neuen Eintrag hinzufügen
        new_row = pd.DataFrame([{"Datum": str(datum), "Name": name, "Ort": ort, "Stimmung": stimmung, "Erlebnis": erlebnis}])
        
        if df is not None and not df.empty:
            updated_df = pd.concat([df, new_row], ignore_index=True)
        else:
            updated_df = new_row
            
        # Speichern
        conn.update(spreadsheet=MEIN_TABELLEN_LINK, worksheet=BLATT_NAME, data=updated_df)
        st.balloons()
        st.success("Erfolg! Der Eintrag ist in der Tabelle. 🇮🇹")
    except Exception as e:
        st.error(f"Fehler: {e}")

# Anzeige der Liste
st.divider()
try:
    data = conn.read(spreadsheet=MEIN_TABELLEN_LINK, worksheet=BLATT_NAME)
    if not data.empty:
        st.dataframe(data.iloc[::-1], use_container_width=True)
except:
    st.write("Noch keine Einträge vorhanden.")
    
            
        
