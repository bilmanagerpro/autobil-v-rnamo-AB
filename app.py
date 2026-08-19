import pandas as pd
import streamlit as st

st.set_page_config(page_title="Autobil Värnamo AB", page_icon="🚗", layout="wide")

# --- INITIALISERING AV DATA FÖR LAGER ---
if "bilar" not in st.session_state:
    st.session_state.bilar = pd.DataFrame(
        columns=[
            "ID",
            "Bilmodell",
            "Reg.nr",
            "Mätarställning",
            "Inköpspris",
            "Rep.kostnad",
            "Status",
        ]
    )

# --- SIDOMENY ---
st.sidebar.title("📌 Huvudmeny")
menu = st.sidebar.radio("Välj sektion:", ["🚗 Lagerhantering"])

st.title("🚗 Autobil Värnamo AB - Lagerhantering")

# --- 1. LAGERHANTERING ---
if menu == "🚗 Lagerhantering":
  st.header("Registrera ny bil i lager")

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

    if submit_bil:
      if bilmodell and reg_nr:
        new_row = pd.DataFrame({
            "ID": [len(st.session_state.bilar) + 1],
            "Bilmodell": [bilmodell],
            "Reg.nr": [reg_nr],
            "Mätarställning": [matarstallning],
            "Inköpspris": [inkopspris],
            "Rep.kostnad": [rep_kostnad],
            "Status": [status],
        })
        st.session_state.bilar = pd.concat(
            [st.session_state.bilar, new_row], ignore_index=True
        )
        st.success("Bilen har lagts till i lager!")
      else:
        st.warning(
            "Vänligen fyll åtminstone i Bilmodell och REG. nummer."
        )

  st.divider()
  st.subheader("Bilar i lager")
  if not st.session_state.bilar.empty:
    st.session_state.bilar = st.data_editor(
        st.session_state.bilar, num_rows="dynamic", use_container_width=True
    )
  else:
    st.info("Inga bilar registrerade än.")
