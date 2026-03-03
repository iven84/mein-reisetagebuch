import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Family Travel", page_icon="🌍")

# HIER DEINEN LINK EINTRAGEN
MEIN_TABELLEN_LINK = "DEIN_GOOGLE_SHEETS_LINK_HIER"
# HIER PRÜFEN: Heißt es unten in Google "Tabelle1" oder "Sheet1"?
BLATT_NAME = "Tabelle1" 

st.title("🌍 Unser Familien-Reisetagebuch")

conn = st.connection("gsheets", type=GSheetsConnection)

with st.form(key="reise_form"):
    datum = st.date_input("Wann?")
    name = st.selectbox("Wer schreibt?", ["Mama", "Papa", "Kind 1", "Kind 2", "Daliyah"])
    ort = st.text_input("Wo sind wir?")
    stimmung = st.select_slider("Stimmung", options=["😢", "😐", "🙂", "🤩", "🚀"])
    erlebnis = st.text_area("Was ist passiert?")
    submit = st.form_submit_button(label="Erinnerung speichern! ✨")

if submit:
    try:
        # 1. Bestehende Daten laden
        existing_data = conn.read(spreadsheet=https://docs.google.com/spreadsheets/d/1aIMSYHxW89-d-FIQsxq9FQJLrrROVdmYceABxglZmq8/edit?usp=drivesdk, worksheet=BLATT_NAME)
        
        # 2. Neuen Eintrag bauen
        new_entry = pd.DataFrame([{
            "Datum": str(datum),
            "Name": name,
            "Ort": ort,
            "Stimmung": stimmung,
            "Erlebnis": erlebnis
        }])
        
        # 3. Kombinieren (falls Tabelle leer ist, nur neuen Eintrag nehmen)
        if existing_data is not None and not existing_data.empty:
            updated_df = pd.concat([existing_data, new_entry], ignore_index=True)
        else:
            updated_df = new_entry
            
        # 4. Hochladen
        conn.update(spreadsheet=https://docs.google.com/spreadsheets/d/1aIMSYHxW89-d-FIQsxq9FQJLrrROVdmYceABxglZmq8/edit?usp=drivesdk, worksheet=BLATT_NAME, data=updated_df)
        
        st.balloons()
        st.success("Gespeichert! Viel Spaß in Italien! 🇮🇹")
    except Exception as e:
        st.error(f"Fehler beim Speichern: {e}")
        st.info(f"Tipp: Prüfe, ob das Blatt in Google wirklich '{BLATT_NAME}' heißt!")

st.divider()
st.subheader("📖 Unsere bisherigen Abenteuer")
try:
    data = conn.read(spreadsheet=MEIN_TABELLEN_LINK, worksheet=BLATT_NAME)
    if data is not None and not data.empty:
        st.dataframe(data.iloc[::-1], use_container_width=True)
    else:
        st.write("Noch keine Einträge vorhanden.")
except:
    st.write("Schreib den ersten Eintrag!")
    
    
