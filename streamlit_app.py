import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Reisetagebuch", page_icon="🌍")

# DEIN LINK
URL = "https://docs.google.com/spreadsheets/d/1aIMSYHxW89-d-FIQsxq9FQJLrrROVdmYceABxglZmq8/edit?usp=drivesdk"
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
        # Wir laden die Daten ohne die erste Zeile zu prüfen
        df = conn.read(spreadsheet=MEIN_TABELLEN_LINK, worksheet=BLATT_NAME, header=None)
        
        # Wir erstellen eine einfache Liste der Daten
        neue_zeile = [str(datum), wer, ort, stimmung, erlebnis]
        
        # Wir fügen die Zeile einfach unten an
        neuer_df = pd.DataFrame([neue_zeile])
        if df is not None:
            final_df = pd.concat([df, neuer_df], ignore_index=True)
        else:
            final_df = neuer_df
            
        # Wir überschreiben die Tabelle komplett (das erzwingt das Speichern)
        conn.update(spreadsheet=MEIN_TABELLEN_LINK, worksheet=BLATT_NAME, data=final_df, header=False)
        
        st.balloons()
        st.success("Endlich! Gespeichert! 🇮🇹")
        st.rerun()
    except Exception as e:
        st.error(f"Fehler: {e}")

st.divider()
try:
    data = conn.read(spreadsheet=MEIN_TABELLEN_LINK, worksheet=BLATT_NAME, header=None)
    if data is not None:
        st.write("### Unsere Erlebnisse:")
        st.table(data.iloc[::-1])
except:
    st.info("Noch keine Einträge.")
    
