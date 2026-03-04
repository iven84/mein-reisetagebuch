import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. Konfiguration
st.set_page_config(page_title="Family Travel", page_icon="🌍")

# 2. DEIN LINK (Hier den Link zwischen die " " kopieren!)
MEIN_TABELLEN_LINK = " https://docs.google.com/spreadsheets/d/1aIMSYHxw89-d-FIqsxq9FQJLrrROVdmYceABxglZmq8/edit?usp=sharing "

# 3. BLATT NAME (Prüfe ob es in Google 'Tabelle1' oder 'Sheet1' heißt)
BLATT_NAME = "Tabelle1" 

st.title("🌍 Unser Familien-Reisetagebuch")
st.write("Schreib auf, was wir heute erlebt haben! 😂")

# Verbindung aufbauen
conn = st.connection("gsheets", type=GSheetsConnection)

# Formular
with st.form(key="reise_form"):
    datum = st.date_input("Wann?", value=pd.to_datetime("today"))
    name = st.selectbox("Wer schreibt?", ["Mama", "Papa", "Daliyah", "Matze", "Fabi", "Sabine"])
    ort = st.text_input("Wo sind wir?", placeholder="z.B. Gardasee")
    stimmung = st.select_slider("Stimmung", options=["😢", "😐", "🙂", "🤩", "🚀"])
    erlebnis = st.text_area("Was ist passiert?")
    submit = st.form_submit_button(label="Erinnerung speichern! ✨")

if submit:
    try:
        # Bestehende Daten lesen
        existing_data = conn.read(spreadsheet=MEIN_TABELLEN_LINK, worksheet=BLATT_NAME)
        
        # Neuen Eintrag erstellen
        new_entry = pd.DataFrame([{
            "Datum": str(datum),
            "Name": name,
            "Ort": ort,
            "Stimmung": stimmung,
            "Erlebnis": erlebnis
        }])
        
        # Daten zusammenfügen
        if existing_data is not None and not existing_data.empty:
            updated_df = pd.concat([existing_data, new_entry], ignore_index=True)
        else:
            updated_df = new_entry
            
        # Zurückschreiben zu Google
        conn.update(spreadsheet=MEIN_TABELLEN_LINK, worksheet=BLATT_NAME, data=updated_df)
        
        st.balloons()
        st.success("Gespeichert! Viel Spaß in Italien! 🇮🇹")
    except Exception as e:
        st.error(f"Fehler: {e}")

# Liste anzeigen
st.divider()
st.subheader("📖 Unsere bisherigen Abenteuer")
try:
    data = conn.read(spreadsheet=MEIN_TABELLEN_LINK, worksheet=BLATT_NAME)
    if data is not None and not data.empty:
        st.dataframe(data.iloc[::-1], use_container_width=True)
except:
    st.info("Noch keine Einträge vorhanden.")
    
