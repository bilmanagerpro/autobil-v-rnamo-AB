import pandas as pd
import streamlit as st

st.set_page_config(page_title="Autobil Värnamo AB", page_icon="🚗", layout="wide")

# --- INITIALISERING ---
if "bilar" not in st.session_state:
    st.session_state.bilar = pd.DataFrame(columns=["ID", "Bilmodell", "Reg.nr", "Mätarställning", "Inköpspris", "Rep.kostnad", "Status"])

if "utgifter" not in st.session_state:
    st.session_state.utgifter = pd.DataFrame(columns=["Kategori", "Belopp (SEK)", "Datum"])

st.sidebar.title("📌 Huvudmeny")
menu = st.sidebar.radio("Välj sektion:", ["🚗 Lagerhantering", "💸 Utgifter & Ekonomi"])

st.title("🚗 Autobil Värnamo AB")

# --- 1. LAGERHANTERING ---
if menu == "🚗 Lagerhantering":
    st.header("📦 Lagerhantering")
    with st.form("bil_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            bilmodell = st.text_input("Bilmodell")
            reg_nr = st.text_input("REG. nummer")
            inkopspris = st.number_input("Inköpspris (SEK)", min_value=0)
        with col2:
            rep_kostnad = st.number_input("Reparationskostnad (SEK)", min_value=0)
            status = st.selectbox("Status", ["I lager", "Såld"])
        
        submit_bil = st.form_submit_button("Lägg till bil")
        if submit_bil:
            new_row = pd.DataFrame({"ID": [len(st.session_state.bilar)+1], "Bilmodell": [bilmodell], "Reg.nr": [reg_nr], "Mätarställning": [0], "Inköpspris": [inkopspris], "Rep.kostnad": [rep_kostnad], "Status": [status]})
            st.session_state.bilar = pd.concat([st.session_state.bilar, new_row], ignore_index=True)

    st.subheader("Bilar i systemet")
    st.session_state.bilar = st.data_editor(st.session_state.bilar, use_container_width=True)

# --- 2. UTGIFTER & EKONOMI ---
elif menu == "💸 Utgifter & Ekonomi":
    st.header("💸 Utgifter & Resultat")
    
    # قسم المصاريف
    with st.form("utgift_form"):
        kategori = st.text_input("Kategori (t.ex. Hyra, Verktyg)")
        belopp = st.number_input("Belopp (SEK)", min_value=0)
        if st.form_submit_button("Lägg till utgift"):
            st.session_state.utgifter = pd.concat([st.session_state.utgifter, pd.DataFrame({"Kategori": [kategori], "Belopp (SEK)": [belopp], "Datum": [str(pd.Timestamp.now().date())]})], ignore_index=True)
    
    # عرض المجموع المالي
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.subheader("📊 Ekonomisk översikt")
        total_utgifter = st.session_state.utgifter["Belopp (SEK)"].sum()
        total_inkop = st.session_state.bilar["Inköpspris"].sum()
        total_rep = st.session_state.bilar["Rep.kostnad"].sum()
        
        st.metric("Totala Inköpskostnader", f"{total_inkop} SEK")
        st.metric("Totala Reparationer", f"{total_rep} SEK")
        st.metric("Övriga Utgifter", f"{total_utgifter} SEK")
        st.divider()
        st.metric("TOTAL UTGIFT (Alla poster)", f"{total_inkop + total_rep + total_utgifter} SEK")

    with col_b:
        st.subheader("📋 Detaljerade tabeller")
        st.write("Utgifter:")
        st.dataframe(st.session_state.utgifter, use_container_width=True)
        st.write("Bil-status:")
        st.dataframe(st.session_state.bilar[["Bilmodell", "Status", "Inköpspris", "Rep.kostnad"]], use_container_width=True)
