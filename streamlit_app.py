import streamlit as st
from streamlit_gsheets import GSheetsConnection

# Titel der App
st.title("🌍 Unser Familien-Reisetagebuch")
st.write("Schreib auf, was wir heute erlebt haben! 😂")

# Verbindung zur Tabelle definieren
conn = st.connection("gsheets", type=GSheetsConnection)

# Formular für die Eingabe
with st.form(key="reise_form"):
    datum = st.date_input("Wann?")
    name = st.selectbox("Wer schreibt?", ["Mama", "Papa", "Kind 1", "Kind 2"])
    ort = st.text_input("Wo sind wir?")
    stimmung = st.select_slider("Stimmung", options=["😢", "😐", "🙂", "🤩", "🚀"])
    erlebnis = st.text_area("Was ist passiert?")
    
    submit = st.form_submit_button(label="Erinnerung speichern! ✨")

if submit:
    # Daten aus der Tabelle laden
    existing_data = conn.read(worksheet="Sheet1")
    
    # Neuen Eintrag erstellen
    new_entry = {
        "Datum": str(datum),
        "Name": name,
        "Ort": ort,
        "Stimmung": stimmung,
        "Erlebnis": erlebnis
    }
    
    # Daten aktualisieren
    updated_df = existing_data.append(new_entry, ignore_index=True)
    conn.update(worksheet="Sheet1", data=updated_df)
    
    st.balloons()
    st.success("Gespeichert! Schau mal unten in die Liste.")

# Historie anzeigen
st.divider()
st.subheader("📖 Unsere bisherigen Abenteuer")
data = conn.read(worksheet="Sheet1")
st.dataframe(data.iloc[::-1]) # Neueste zuerst
