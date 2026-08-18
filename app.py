import datetime
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Autobil Värnamo AB", page_icon="🚗", layout="wide")

# --- INITIALISERING AV DATA ---
if "bilar" not in st.session_state:
    st.session_state.bilar = pd.DataFrame(columns=["ID", "Bilmodell", "Reg.nr", "Mätarställning", "Inköpspris", "Rep.kostnad", "Status"])

if "bil_fakturor" not in st.session_state:
    st.session_state.bil_fakturor = pd.DataFrame(columns=["Fakturanr", "Datum", "Reg.nr", "Mätarställning", "Arsmodell", "Fordonstatus", "Namn", "Personnummer", "Gatuadress", "PostnummerOrt", "PrisSEK", "Betalningssätt", "KontantInsats", "Anteckningar"])

if "utgifter" not in st.session_state:
    st.session_state.utgifter = pd.DataFrame(columns=["Kategori", "Belopp (SEK)", "Datum"])

# --- SIDOMENY (Svenska) ---
st.sidebar.title("📌 Huvudmeny")
menu = st.sidebar.radio(
    "Välj sektion:",
    [
        "🚗 Lagerhantering", 
        "📄 Bilförsäljningsfaktura", 
        "💸 Utgifter", 
        "📊 Rapporter & Resultat"
    ]
)

st.title("🚗 Autobil Värnamo AB - System för bilförsäljning")

# --- 1. LAGERHANTERING ---
if menu == "🚗 Lagerhantering":
    st.header("🚗 Lagerhantering")
    with st.form("bil_form"):
        col1, col2 = st.columns(2)
        with col1:
            bilmodell = st.text_input("Bilmodell / Årsmodell")
            reg_nr = st.text_input("REG. nummer")
        with col2:
            matarstallning = st.text_input("Mätarställning / mil")
            inkopspris = st.text_input("Inköpspris (SEK)")
            rep_kostnad = st.text_input("Reparationskostnad (SEK)")
            status = st.selectbox("Fordonstatus", ["I lager", "Såld"])
        submit_bil = st.form_submit_button("Lägg till bil i lager")

        if submit_bil and bilmodell:
            new_row = pd.DataFrame({"ID": [len(st.session_state.bilar) + 1], "Bilmodell": [bilmodell], "Reg.nr": [reg_nr], "Mätarställning": [matarstallning], "Inköpspris": [inkopspris], "Rep.kostnad": [rep_kostnad], "Status": [status]})
            st.session_state.bilar = pd.concat([st.session_state.bilar, new_row], ignore_index=True)
            st.success("Bilen har lagts till!")

    st.subheader("Bilar i lager (Markera raden och tryck Delete för att radera)")
    if not st.session_state.bilar.empty:
        st.session_state.bilar = st.data_editor(st.session_state.bilar, num_rows="dynamic", use_container_width=True)
    else:
        st.info("Inga bilar registrerade än.")

# --- 2. BILFÖRSÄLJNINGSFAKTURA ---
elif menu == "📄 Bilförsäljningsfaktura":
    st.header("📄 Bilförsäljning - Faktura / Köpekontrakt")
    
    with st.form("bil_faktura_form"):
        st.subheader("1. Fordonsinformation")
        col1, col2 = st.columns(2)
        with col1:
            fakturanr = st.text_input("Faktura nr:", value=f"FAK-{len(st.session_state.bil_fakturor) + 1001}")
            reg_nummer = st.text_input("REG. nummer")
            arsmodell = st.text_input("Årsmodell / tillverk.")
        with col2:
            datum = st.date_input("Datum", datetime.date.today())
            matar = st.text_input("Mätarställning / mil")
            fordonstatus = st.text_input("Fordonstatus / Bilmärke", value="Begagnad")

        st.subheader("2. Köparens information")
        col3, col4 = st.columns(2)
        with col3:
            namn = st.text_input("Namn")
            gatuadress = st.text_input("Gatuadress")
        with col4:
            personnummer = st.text_input("Org. / Personnummer")
            postnummer_ort = st.text_input("Postnummer / Ort")

        st.subheader("3. Betalningsinformation")
        col5, col6, col7 = st.columns(3)
        with col5:
            pris_sek = st.text_input("Pris i SEK")
        with col6:
            betalningssatt = st.selectbox("Betalningssätt", ["Swish", "Bankgiro", "Kontant", "Faktura/Finans"])
        with col7:
            kontant_insats = st.text_input("Kontant insats i SEK")

        st.subheader("4. Fordonsskick & Anteckningar")
        standard_villkor = "Köparen har provkört bilen och godkänner den i förevisat skick. Autobil Värnamo AB frånskriver sig ansvar/garantier mot ex. antal nycklar, krock, skador, om lackering, antalet ägare och miltal. Köparen godkänner bilen i befintligt skick och godkänner ovanstående genom undertecknande av avtal. Bolaget tillämpar vinstmarginalbeskattning (VMB) för handel med begagnade varor enligt 20 kap mervärdesskattelagen (2023:200)."
        anteckningar = st.text_area("Anteckningar", value=standard_villkor)

        submit_bil_fak = st.form_submit_button("Spara kontrakt")

        if submit_bil_fak and namn:
            new_bil_fak = pd.DataFrame({
                "Fakturanr": [fakturanr], "Datum": [str(datum)], "Reg.nr": [reg_nummer], 
                "Mätarställning": [matar], "Arsmodell": [arsmodell], "Fordonstatus": [fordonstatus], 
                "Namn": [namn], "Personnummer": [personnummer], "Gatuadress": [gatuadress], 
                "PostnummerOrt": [postnummer_ort], "PrisSEK": [pris_sek], "Betalningssätt": [betalningssatt], 
                "KontantInsats": [kontant_insats], "Anteckningar": [anteckningar]
            })
            st.session_state.bil_fakturor = pd.concat([st.session_state.bil_fakturor, new_bil_fak], ignore_index=True)
            st.success("Kontrakt sparat!")

    st.divider()
    st.subheader("🖨️ Förhandsgranska och skriv ut")
    if not st.session_state.bil_fakturor.empty:
        selected_fak = st.selectbox("Välj fakturanummer:", st.session_state.bil_fakturor["Fakturanr"])
        row = st.session_state.bil_fakturor[st.session_state.bil_fakturor["Fakturanr"] == selected_fak].iloc[0]

        st.markdown(f"""
        <div style="border: 2px solid #000; padding: 20px; background-color: #fff; color: #000; border-radius: 5px;">
            <div style="display: flex; justify-content: space-between; border-bottom: 2px solid #000; padding-bottom: 10px;">
                <div>
                    <h2 style="margin:0; color:#333;">Autobil Värnamo AB</h2>
                    <p style="margin:2px 0;"><b>Org. nr:</b> 559565-5399 | <b>Tel nr:</b> 0737220799</p>
                    <p style="margin:2px 0;"><b>E-post:</b> info@autobilvarnamo.se</p>
                </div>
                <div style="text-align: right;">
                    <p style="margin:2px 0;"><b>Köper, Säljer, Byter, Förmedlar</b></p>
                    <p style="margin:2px 0;"><b>Begagnade bilar</b></p>
                    <p style="margin:2px 0;">Hagagatan 14, 33176 Rydaholm</p>
                </div>
            </div>
            
            <div style="display: flex; justify-content: space-between; margin-top: 15px;">
                <p><b>Datum:</b> {row['Datum']}</p>
                <p><b>Faktura nr:</b> {row['Fakturanr']}</p>
            </div>

            <h4 style="background: #ddd; padding: 5px; margin-top: 10px;">Fordon:</h4>
            <table style="width:100%; border-collapse: collapse; border: 1px solid #000;">
                <tr>
                    <td style="border: 1px solid #000; padding: 5px;"><b>REG. nummer:</b> {row['Reg.nr']}</td>
                    <td style="border: 1px solid #000; padding: 5px;"><b>Mätarställning/mil:</b> {row['Mätarställning']}</td>
                </tr>
                <tr>
                    <td style="border: 1px solid #000; padding: 5px;"><b>Årsmodell/tillverk:</b> {row['Arsmodell']}</td>
                    <td style="border: 1px solid #000; padding: 5px;"><b>Fordonstatus/Bilmärke:</b> {row['Fordonstatus']}</td>
                </tr>
            </table>

            <h4 style="background: #ddd; padding: 5px; margin-top: 10px;">Köpare:</h4>
            <table style="width:100%; border-collapse: collapse; border: 1px solid #000;">
                <tr>
                    <td style="border: 1px solid #000; padding: 5px;"><b>Namn:</b> {row['Namn']}</td>
                    <td style="border: 1px solid #000; padding: 5px;"><b>Org./personnummer:</b> {row['Personnummer']}</td>
                </tr>
                <tr>
                    <td style="border: 1px solid #000; padding: 5px;"><b>Gatuadress:</b> {row['Gatuadress']}</td>
                    <td style="border: 1px solid #000; padding: 5px;"><b>Postnummer/Ort:</b> {row['PostnummerOrt']}</td>
                </tr>
            </table>

            <h4 style="background: #ddd; padding: 5px; margin-top: 10px;">Betalning:</h4>
            <table style="width:100%; border-collapse: collapse; border: 1px solid #000;">
                <tr>
                    <td style="border: 1px solid #000; padding: 5px;"><b>Pris i SEK:</b> {row['PrisSEK']}</td>
                    <td style="border: 1px solid #000; padding: 5px;"><b>Betalningssätt:</b> {row['Betalningssätt']}</td>
                    <td style="border: 1px solid #000; padding: 5px;"><b>Kontant insats:</b> {row['KontantInsats']}</td>
                </tr>
            </table>

            <h4 style="background: #ddd; padding: 5px; margin-top: 10px;">Fordonsskick & Villkor:</h4>
            <p style="font-size: 11px; border: 1px solid #000; padding: 8px;">{row['Anteckningar']}</p>

            <div style="display: flex; justify-content: space-between; margin-top: 20px;">
                <div style="border: 1px solid #000; width: 48%; padding: 10px; height: 60px;"><b>Undertecknade Säljare:</b><br>Auto bil Värnamo AB</div>
                <div style="border: 1px solid #000; width: 48%; padding: 10px; height: 60px;"><b>Undertecknade Köpare:</b></div>
            </div>

            <div style="display: flex; justify-content: space-between; margin-top: 20px; font-size: 12px; border-top: 1px solid #000; padding-top: 5px;">
                <div><b>Bank:</b> SEB | <b>Bankkonto:</b> 5182 1018249</div>
                <div><b>Swish:</b> 1230293365 | <b>Bg:</b> 5223-7732</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.write("")
        if st.button("Radera faktura"):
            st.session_state.bil_fakturor = st.session_state.bil_fakturor[st.session_state.bil_fakturor["Fakturanr"] != selected_fak]
            st.rerun()
    else:
        st.info("Inga fakturor sparade.")

# --- 3. UTGIFTER ---
elif menu == "💸 Utgifter":
    st.header("💸 Utgifter")
    with st.form("utgift_form"):
        kategori = st.selectbox("Kategori", ["Reservdelar", "Hyra lokal", "Verktyg", "El & Värme", "Övrigt"])
        belopp = st.text_input("Belopp (SEK)")
        utgift_datum = st.date_input("Datum", datetime.date.today())
        submit_utgift = st.form_submit_button("Lägg till utgift")

        if submit_utgift and belopp:
            new_utg = pd.DataFrame({"Kategori": [kategori], "Belopp (SEK)": [belopp], "Datum": [str(utgift_datum)]})
            st.session_state.utgifter = pd.concat([st.session_state.utgifter, new_utg], ignore_index=True)
            st.success("Utgift sparad!")

    st.subheader("Registrerade utgifter")
    if not st.session_state.utgifter.empty:
        st.session_state.utgifter = st.data_editor(st.session_state.utgifter, num_rows="dynamic", use_container_width=True)
    else:
        st.info("Inga utgifter registrerade.")

# --- 4. RAPPORTER & RESULTAT ---
elif menu == "📊 Rapporter & Resultat":
    st.header("📊 Ekonomisk Sammanställning")
    st.info("Alla fält är nu textbaserade för manuell inmatning.")
