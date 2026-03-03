import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Konfiguration
st.set_page_config(page_title="Family Travel", page_icon="🌍")

# HIER DEINEN LINK EINTRAGEN:
MEIN_TABELLEN_LINK = "DEINE_URL_HIER_EINSETZEN"

st.title("🌍 Unser Familien-Reisetagebuch")
st.write("Schreib auf, was wir heute erlebt haben! 😂")

# Verbindung direkt mit der URL herstellen
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
        # Daten mit der expliziten URL lesen
        existing_data = conn.read(spreadsheet=MEIN_TABELLEN_LINK, worksheet="Sheet1")
        
        new_entry = pd.DataFrame([{
            "Datum": str(datum),
            "Name": name,
            "Ort": ort,
            "Stimmung": stimmung,
            "Erlebnis": erlebnis
        }])
        
        updated_df = pd.concat([existing_data, new_entry], ignore_index=True)
        
        # Daten mit der expliziten URL speichern
        conn.update(spreadsheet=MEIN_TABELLEN_LINK, worksheet="Sheet1", data=updated_df)
        
        st.balloons()
        st.success("Gespeichert! Italien kann kommen! 🇮🇹")
    except Exception as e:
        st.error(f"Oh weh, da gab es ein Problem: {e}")

# Historie anzeigen
st.divider()
st.subheader("📖 Unsere bisherigen Abenteuer")
try:
    data = conn.read(spreadsheet=MEIN_TABELLEN_LINK, worksheet="Sheet1")
    if not data.empty:
        st.dataframe(data.iloc[::-1]) 
    else:
        st.info("Noch keine Einträge vorhanden.")
except:
    st.info("Schreib den ersten Eintrag!")
    
