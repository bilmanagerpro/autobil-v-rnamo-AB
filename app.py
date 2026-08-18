import streamlit as st
import pandas as pd
from datetime import datetime

# Inställningar för sidan
st.set_page_config(page_title="Autobil Värnamo AB", page_icon="🚗", layout="wide")

st.title("🚗 Autobil Värnamo AB - System för bilförsäljning & verkstad")
st.markdown("---")

# Initiera datastrukturer
if 'bilar' not in st.session_state:
    st.session_state.bilar = pd.DataFrame(columns=['ID', 'Bilmodell', 'VIN', 'Inköpspris', 'Rep.kostnad', 'Total kostnad', 'Status'])

if 'fakturor' not in st.session_state:
    st.session_state.fakturor = pd.DataFrame(columns=['Faktura-nr', 'Typ', 'Kund', 'Pris ex moms', 'Moms', 'Att betala', 'Datum'])

if 'utgifter' not in st.session_state:
    st.session_state.utgifter = pd.DataFrame(columns=['Beskrivning', 'Belopp', 'Datum'])

# Menyn
menu = st.sidebar.selectbox("Välj sektion", ["Lagerhantering", "Skapa faktura", "Utgifter", "Rapporter & Resultat"])

# --- 1. Lagerhantering ---
if menu == "Lagerhantering":
    st.header("🚘 Lagerhantering")
    with st.form("add_car_form"):
        col1, col2 = st.columns(2)
        with col1:
            car_model = st.text_input("Bilmodell (t.ex. Volvo V60)")
            vin_num = st.text_input("Chassinummer (VIN)")
            purchase_price = st.number_input("Inköpspris (SEK)", min_value=0.0, step=100.0)
        with col2:
            repair_cost = st.number_input("Reparationskostnad (SEK)", min_value=0.0, step=100.0)
            car_status = st.selectbox("Status", ["I lager", "Bokad", "Såld"])
        
        if st.form_submit_button("Lägg till bil"):
            total = purchase_price + repair_cost
            new_row = pd.DataFrame({'ID': [len(st.session_state.bilar) + 1], 'Bilmodell': [car_model], 'VIN': [vin_num], 'Inköpspris': [purchase_price], 'Rep.kostnad': [repair_cost], 'Total kostnad': [total], 'Status': [car_status]})
            st.session_state.bilar = pd.concat([st.session_state.bilar, new_row], ignore_index=True)
            st.success("Bilen har lagts till!")

    st.dataframe(st.session_state.bilar, use_container_width=True)

# --- 2. Skapa faktura ---
elif menu == "Skapa faktura":
    st.header("📄 Fakturering")
    with st.form("invoice_form"):
        col1, col2 = st.columns(2)
        with col1:
            inv_type = st.selectbox("Fakturatyp", ["Bilförsäljning (VMB)", "Verkstad/Service (25% moms)"])
            customer = st.text_input("Kund / Företagsnamn")
            price_ex = st.number_input("Pris exkl. moms (SEK)", min_value=0.0, step=100.0)
        with col2:
            apply_moms = st.checkbox("Applicera 25% moms")
            date = st.date_input("Datum", datetime.today())
        
        if st.form_submit_button("Skapa faktura"):
            if apply_moms:
                total = price_ex * 1.25
                moms = f"{price_ex * 0.25:.2f} kr"
            else:
                total = price_ex
                moms = "0.00 kr (VMB)"
            
            new_inv = pd.DataFrame({'Faktura-nr': [f"INV-{len(st.session_state.fakturor) + 1001}"], 'Typ': [inv_type], 'Kund': [customer], 'Pris ex moms': [price_ex], 'Moms': [moms], 'Att betala': [total], 'Datum': [str(date)]})
            st.session_state.fakturor = pd.concat([st.session_state.fakturor, new_inv], ignore_index=True)
            st.success(f"Faktura skapad! Totalt: {total:.2f} kr")

    st.dataframe(st.session_state.fakturor, use_container_width=True)

# --- 3. Utgifter ---
elif menu == "Utgifter":
    st.header("📉 Utgifter")
    with st.form("expense_form"):
        desc = st.text_input("Beskrivning (t.ex. Hyra, El, Reservdelar)")
        amount = st.number_input("Belopp (SEK)", min_value=0.0, step=50.0)
        if st.form_submit_button("Registrera utgift"):
            new_exp = pd.DataFrame({'Beskrivning': [desc], 'Belopp': [amount], 'Datum': [str(datetime.today())]})
            st.session_state.utgifter = pd.concat([st.session_state.utgifter, new_exp], ignore_index=True)
            st.success("Utgift registrerad!")
    st.dataframe(st.session_state.utgifter, use_container_width=True)

# --- 4. Rapporter ---
elif menu == "Rapporter & Resultat":
    st.header("📈 Rapport: Autobil Värnamo AB")
    total_sales = st.session_state.fakturor['Att betala'].sum()
    total_exp = st.session_state.utgifter['Belopp'].sum()
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Total omsättning", f"{total_sales:,.2f} kr")
    c2.metric("Totala utgifter", f"{total_exp:,.2f} kr")
    c3.metric("Resultat", f"{total_sales - total_exp:,.2f} kr")
