import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt

st.set_page_config(layout="wide")

st.title("Analyse des poids des packs LOT PROTEAN")

# Upload du fichier XLSX
uploaded_file = st.file_uploader("Upload your XLSX file", type=["xlsx"])

if uploaded_file is not None:
    # Lecture du fichier XLSX
    df = pd.read_excel(uploaded_file)

    # Filtrage des données
    df = df[df.iloc[:, 12] == "LOT PROTEAN"]  # Filtrage du lot 
    df = df.drop("BatchNumber", axis=1)  # Suppression de la colonne BatchNumber

    # Convertir la colonne Timestamp en datetime
    # Assurez-vous que le format est CORRECT pour votre fichier XLSX
    df["Timestamp"] = pd.to_datetime(df["Timestamp"], format='%d/%m/%Y %H:%M:%S')

    # Créer une nouvelle colonne "Id Timestamp" en combinant Id et Timestamp
    df["Id Timestamp"] = df["Id"].astype(str) + " - " + df["Timestamp"].dt.strftime("%d/%m/%Y %H:%M:%S")

    # Slider pour le timestamp
    start_date, end_date = st.slider(
        "Sélectionnez la période",
        # Convertir les valeurs min et max en datetime pour le slider
        value=(pd.to_datetime(df["Timestamp"].min()), pd.to_datetime(df["Timestamp"].max())),
        format="MM/DD/YYYY HH:mm:ss",
    )
    df = df[
        (df["Timestamp"] >= start_date) & (df["Timestamp"] <= end_date)
    ]

    # Sélection de la ressource
    ressource = st.selectbox(
        "Choisissez une ressource",
        df["Ressource"].unique(),
    )
    df = df[df["Ressource"] == ressource]

    # Création des graphiques
    st.subheader("Boxplots des poids des packs par ressource")

    # Boxplot Altair
    chart = (
        alt.Chart(df)
        .mark_boxplot()
        .encode(
            alt.X("Ressource:N", title="Ressource"),
            alt.Y("PackWeight:Q", title="Poids du pack"),
        )
    )
    st.altair_chart(chart, use_container_width=True)

    # Boxplot Matplotlib
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.boxplot(df["PackWeight"], vert=False, patch_artist=True)
    ax.set_xlabel("Poids du pack")
    ax.set_ylabel("Ressource")
    ax.set_title("Boxplot des poids des packs pour la ressource " + ressource)
    st.pyplot(fig)

    # Autres graphiques (histogramme, scatter plot, etc.)
    # ...

else:
    st.info("Veuillez charger un fichier XLSX.")
