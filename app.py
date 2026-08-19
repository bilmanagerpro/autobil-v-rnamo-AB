import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Autobil Värnamo AB - Lagerhantering", page_icon="🚗", layout="wide"
)

# --- INITIALISERING AV LAGER ---
if "bilar" not in st.session_state:
    st.session_state.bilar = pd.DataFrame(columns=[
        "ID",
        "Bilmodell",
        "Reg.nr",
        "Mätarställning",
        "Inköpspris",
        "Rep.kostnad",
        "Totalt",
        "Status",
    ])

# --- SIDOMENY ---
st.sidebar.title("📌 Huvudmeny")
menu = st.sidebar.radio("Välj sektion:", ["🚗 Lagerhantering"])

st.title("🚗 Autobil Värnamo AB - Lagerhantering")

if menu == "🚗 Lagerhantering":
    col_form, col_search = st.columns([2, 1])

    with col_form:
        st.subheader("Registrera ny bil i lager")
        with st.form("bil_form", clear_on_submit=True):
            c1, c2 = st.columns(2)
            with c1:
                bilmodell = st.text_input("Bilmodell / Årsmodell")
                reg_nr = st.text_input("REG. nummer")
                matarstallning = st.text_input("Mätarställning / mil")
            with c2:
                inkopspris_str = st.text_input("Inköpspris (SEK)")
                rep_kostnad_str = st.text_input("Reparationskostnad (SEK)")
                status = st.selectbox("Status", ["I lager", "Såld"])

            submit_bil = st.form_submit_button("Lägg till bil i lager")
            if submit_bil:
                if bilmodell and reg_nr:
                    try:
                        inköp = float(inkopspris_str) if inkopspris_str else 0.0
                    except:
                        inköp = 0.0
                    try:
                        rep = float(rep_kostnad_str) if rep_kostnad_str else 0.0
                    except:
                        rep = 0.0

                    totalt = inköp + rep

                    if st.session_state.bilar.empty or "ID" not in st.session_state.bilar.columns:
                        new_id = 1
                    else:
                        max_id = pd.to_numeric(st.session_state.bilar["ID"], errors="coerce").max()
                        new_id = int(max_id) + 1 if pd.notna(max_id) else 1

                    new_row = pd.DataFrame({
                        "ID": [new_id],
                        "Bilmodell": [bilmodell],
                        "Reg.nr": [reg_nr],
                        "Mätarställning": [matarstallning],
                        "Inköpspris": [inkopspris_str],
                        "Rep.kostnad": [rep_kostnad_str],
                        "Totalt": [str(totalt)],
                        "Status": [status],
                    })
                    
                    # ربط مباشر وفوري مع الذاكرة الأساسية للسيارات
                    st.session_state.bilar = pd.concat(
                        [st.session_state.bilar, new_row], ignore_index=True
                    )
                    st.success("Bilen har lagts till i lager!")
                else:
                    st.warning("Vänligen fyll i åtminstone Bilmodell och REG. nummer.")

    with col_search:
        st.subheader("Sök fordon")
        search_query = st.text_input("Sök med reg.nr")

    st.divider()
    st.subheader("📦 Bilar i systemet")

    df_display = st.session_state.bilar.copy()
    if search_query:
        df_display = df_display[
            df_display["Reg.nr"].str.contains(search_query, case=False, na=False)
        ]

    if not df_display.empty:
        edited_df = st.data_editor(
            df_display, use_container_width=True, key="lager_editor"
        )

        for _, row in edited_df.iterrows():
            orig_id = row["ID"]
            try:
                i_val = float(str(row["Inköpspris"]))
            except:
                i_val = 0.0
            try:
                r_val = float(str(row["Rep.kostnad"]))
            except:
                r_val = 0.0
            row["Totalt"] = str(i_val + r_val)

            st.session_state.bilar.loc[
                st.session_state.bilar["ID"] == orig_id
            ] = row

        st.divider()

        col_a, col_b = st.columns(2)

        with col_a:
            st.markdown(
                "### <span style='color:green;'>🟢 Bilar i lager</span>",
                unsafe_allow_html=True,
            )
            avail = st.session_state.bilar[
                st.session_state.bilar["Status"] == "I lager"
            ]
            if not avail.empty:
                st.dataframe(avail, use_container_width=True)
            else:
                st.info("Inga bilar i lager just nu.")

        with col_b:
            st.markdown(
                "### <span style='color:red;'>🔴 Sålda bilar</span>",
                unsafe_allow_html=True,
            )
            sold = st.session_state.bilar[
                st.session_state.bilar["Status"] == "Såld"
            ]
            if not sold.empty:
                st.dataframe(sold, use_container_width=True)
            else:
                st.info("Inga sålda bilar än.")
    else:
        st.info("Inga bilar hittades.")
