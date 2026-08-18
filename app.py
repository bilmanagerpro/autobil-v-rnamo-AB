import datetime
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Autobil Värnamo AB", page_icon="🚗", layout="wide")

# --- INITIALISERING AV DATA ---
if "bilar" not in st.session_state:
    st.session_state.bilar = pd.DataFrame(columns=["ID", "Bilmodell", "Reg.nr", "Mätarställning", "Inköpspris", "Rep.kostnad", "Total kostnad", "Status"])

if "fakturor" not in st.session_state:
    st.session_state.fakturor = pd.DataFrame(columns=["Fakturanr", "Datum", "Reg.nr", "Bilmodell", "Köpare", "Personnummer", "Pris (SEK)", "Betalningssätt", "Anteckningar"])

if "utgifter" not in st.session_state:
    st.session_state.utgifter = pd.DataFrame(columns=["Kategori", "Belopp (SEK)", "Datum"])

st.title("🚗 Autobil Värnamo AB - System för bilförsäljning & verkstad")

menu = st.sidebar.selectbox("Välj sektion", ["Lagerhantering", "Skapa Bilfaktura / Kvitto", "Utgifter", "Rapporter & Resultat"])

# --- 1. LAGERHANTERING ---
if menu == "Lagerhantering":
    st.header("🚗 Lagerhantering")
    with st.form("bil_form"):
        col1, col2 = st.columns(2)
        with col1:
            bilmodell = st.text_input("Bilmodell / Årsmodell (t.ex. Volvo V60)")
            reg_nr = st.text_input("REG. nummer (t.ex. ABC 123)")
        with col2:
            matarstallning = st.text_input("Mätarställning / mil (t.ex. 12500)")
            inkopspris = st.number_input("Inköpspris (SEK)", min_value=0.0, step=1000.0)
            rep_kostnad = st.number_input("Reparationskostnad (SEK)", min_value=0.0, step=500.0)
            status = st.selectbox("Fordonstatus / Bilmärke", ["I lager", "Såld"])
        submit_bil = st.form_submit_button("Lägg till bil")

        if submit_bil and bilmodell:
            total_kostnad = inkopspris + rep_kostnad
            new_row = pd.DataFrame({"ID": [len(st.session_state.bilar) + 1], "Bilmodell": [bilmodell], "Reg.nr": [reg_nr], "Mätarställning": [matarstallning], "Inköpspris": [inkopspris], "Rep.kostnad": [rep_kostnad], "Total kostnad": [total_kostnad], "Status": [status]})
            st.session_state.bilar = pd.concat([st.session_state.bilar, new_row], ignore_index=True)
            st.success("Bilen har lagts till i lager!")

    st.subheader("Bilar i lager (Markera raden och tryck Delete för att radera)")
    if not st.session_state.bilar.empty:
        st.session_state.bilar = st.data_editor(st.session_state.bilar, num_rows="dynamic", use_container_width=True)
    else:
        st.info("Inga bilar registrerade än.")

# --- 2. SKAPA BILFAKTURA / KVITTO ---
elif menu == "Skapa Bilfaktura / Kvitto":
    st.header("📄 Faktura / Köpecontract (Bilförsäljning)")
    
    with st.form("faktura_form"):
        col1, col2 = st.columns(2)
        with col1:
            fakturanr = st.text_input("Faktura nr:", value=f"FAK-{len(st.session_state.fakturor) + 1001}")
            reg_nr = st.text_input("Fordon - REG. nummer")
            bilmodell = st.text_input("Fordon - Årsmodell / Bilmärke")
            matarstallning = st.text_input("Fordon - Mätarställning / mil")
        with col2:
            datum = st.date_input("Datum", datetime.date.today())
            kopare = st.text_input("Köpare - Namn")
            personnummer = st.text_input("Köpare - Org. / Personnummer")
            gatuadress = st.text_input("Köpare - Gatuadress & Postnummer/Ort")

        st.divider()
        col3, col4 = st.columns(2)
        with col3:
            pris = st.number_input("Pris i SEK (Inkl. ev. VMB)", min_value=0.0, step=1000.0)
        with col4:
            betalningssatt = st.selectbox("Betalningssätt", ["Swish", "Bankgiro", "Kontant", "Faktura/Finans"])

        anteckningar = st.text_area("Anteckningar (Övriga villkor)", value="Köparen har provkört bilen och godkänner den i förevisat skick. Autobil Värnamo AB frånskriver sig ansvar/garantier mot ex. antal nycklar, krock, skador, om lackering, antalet ägare och miltal. Köparen godkänner bilen i befintligt skick och godkänner ovanstående genom undertecknande av avtal. Bolaget tillämpar vinstmarginalbeskattning (VMB) för handel med begagnade varor enligt 20 kap mervärdesskattelagen (2023:200).")

        submit_faktura = st.form_submit_button("Spara faktura")

        if submit_faktura and kopare:
            new_fak = pd.DataFrame({
                "Fakturanr": [fakturanr],
                "Datum": [str(datum)],
                "Reg.nr": [reg_nr],
                "Bilmodell": [bilmodell],
                "Köpare": [kopare],
                "Personnummer": [personnummer],
                "Pris (SEK)": [pris],
                "Betalningssätt": [betalningssatt],
                "Anteckningar": [anteckningar]
            })
            st.session_state.fakturor = pd.concat([st.session_state.fakturor, new_fak], ignore_index=True)
            st.success(f"Faktura {fakturanr} för köparen {kopare} har sparats framgångsrikt!")

    st.subheader("Skapade bilfakturor (Markera och radera vid behov)")
    if not st.session_state.fakturor.empty:
        st.session_state.fakturor = st.data_editor(st.session_state.fakturor, num_rows="dynamic", use_container_width=True)
    else:
        st.info("Inga fakturor skapade än.")

# --- 3. UTGIFTER ---
elif menu == "Utgifter":
    st.header("💸 Utgifter & Inköp")
    with st.form("utgift_form"):
        kategori = st.selectbox("Kategori", ["Reservdelar", "Hyra lokal", "Verktyg", "El & Värme", "Övrigt"])
        belopp = st.number_input("Belopp (SEK)", min_value=0.0, step=100.0)
        utgift_datum = st.date_input("Datum", datetime.date.today())
        submit_utgift = st.form_submit_button("Lägg till utgift")

        if submit_utgift and belopp > 0:
            new_utg = pd.DataFrame({"Kategori": [kategori], "Belopp (SEK)": [belopp], "Datum": [str(utgift_datum)]})
            st.session_state.utgifter = pd.concat([st.session_state.utgifter, new_utg], ignore_index=True)
            st.success("Utgiften har sparats!")

    st.subheader("Registrerade utgifter")
    if not st.session_state.utgifter.empty:
        st.session_state.utgifter = st.data_editor(st.session_state.utgifter, num_rows="dynamic", use_container_width=True)
    else:
        st.info("Inga utgifter registrerade.")

# --- 4. RAPPORTER & RESULTAT ---
elif menu == "Rapporter & Resultat":
    st.header("📊 Ekonomisk Sammanställning")
    total_intakter = st.session_state.fakturor["Pris (SEK)"].sum() if not st.session_state.fakturor.empty else 0
    total_utgifter = st.session_state.utgifter["Belopp (SEK)"].sum() if not st.session_state.utgifter.empty else 0
    netto_resultat = total_intakter - total_utgifter

    col1, col2, col3 = st.columns(3)
    col1.metric("Totala Intäkter", f"{total_intakter:,.2f} SEK")
    col2.metric("Totala Utgifter", f"{total_utgifter:,.2f} SEK")
    col3.metric("Netto Resultat", f"{netto_resultat:,.2f} SEK")

    st.divider()
    st.subheader("Fakturor översikt")
    if not st.session_state.fakturor.empty:
        st.dataframe(st.session_state.fakturor[["Fakturanr", "Datum", "Reg.nr", "Köpare", "Pris (SEK)", "Betalningssätt"]], use_container_width=True)
