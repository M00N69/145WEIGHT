import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt

st.set_page_config(layout="wide")

def main_page():
    st.title("Analyse des poids des packs LOT PROTEAN")

    # Upload du fichier XLSX
    uploaded_file = st.file_uploader("Upload your XLSX file", type=["xlsx"])

    if uploaded_file is not None:
        # Lecture du fichier XLSX
        df = pd.read_excel(uploaded_file)

        # Filtrage des données pour le lot LOT PROTEAN
        df = df[df["LOT PROTEAN"] != 0]

        # Suppression de la colonne BatchNumber
        df = df.drop("BatchNumber", axis=1)

        # Convertir la colonne Timestamp en datetime
        df["Timestamp"] = pd.to_datetime(df["Timestamp"], format='%d/%m/%Y %H:%M:%S', errors='coerce')

        # Vérifier si la conversion a réussi
        if df["Timestamp"].isnull().any():
            st.error("Certaines valeurs de Timestamp ne peuvent pas être converties. Veuillez vérifier le format des dates dans le fichier.")
        else:
            # Slider pour le timestamp
            start_date, end_date = st.slider(
                "Sélectionnez la période",
                min_value=df["Timestamp"].min().to_pydatetime(),
                max_value=df["Timestamp"].max().to_pydatetime(),
                value=(df["Timestamp"].min().to_pydatetime(), df["Timestamp"].max().to_pydatetime()),
                format="DD/MM/YYYY HH:mm:ss"
            )

            df = df[(df["Timestamp"] >= start_date) & (df["Timestamp"] <= end_date)]

            # Sélection de la ressource
            ressource = st.selectbox(
                "Choisissez une ressource",
                df["Ressource"].dropna().unique()
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
                    alt.Y("PackWeight:Q", title="Poids du pack")
                )
            )
            st.altair_chart(chart, use_container_width=True)

            # Boxplot Matplotlib
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.boxplot(df["PackWeight"], vert=False, patch_artist=True)
            ax.set_xlabel("Poids du pack")
            ax.set_title("Boxplot des poids des packs pour la ressource " + str(ressource))
            st.pyplot(fig)

            # Autres graphiques (histogramme)
            st.subheader("Histogramme des poids des packs")
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.hist(df["PackWeight"], bins=20, color='blue', edgecolor='black')
            ax.set_xlabel("Poids du pack")
            ax.set_ylabel("Fréquence")
            ax.set_title("Histogramme des poids des packs pour la ressource " + str(ressource))
            st.pyplot(fig)

    else:
        st.info("Veuillez charger un fichier XLSX.")

def overweight_page():
    st.title("Ressources avec le plus de surpoids")

    # Upload du fichier XLSX
    uploaded_file = st.file_uploader("Upload your XLSX file", type=["xlsx"], key="overweight")

    if uploaded_file is not None:
        # Lecture du fichier XLSX
        df = pd.read_excel(uploaded_file)

        # Filtrage des données pour le lot LOT PROTEAN
        df = df[df["LOT PROTEAN"] != 0]

        # Suppression de la colonne BatchNumber
        df = df.drop("BatchNumber", axis=1)

        # Convertir la colonne Timestamp en datetime
        df["Timestamp"] = pd.to_datetime(df["Timestamp"], format='%d/%m/%Y %H:%M:%S', errors='coerce')

        # Vérifier si la conversion a réussi
        if df["Timestamp"].isnull().any():
            st.error("Certaines valeurs de Timestamp ne peuvent pas être converties. Veuillez vérifier le format des dates dans le fichier.")
        else:
            # Calcul du surpoids
            overweight_threshold = st.number_input("Définir le seuil de surpoids", value=1000)
            df["Surpoids"] = df["PackWeight"] - overweight_threshold

            # Filtrer les ressources avec surpoids
            df_overweight = df[df["Surpoids"] > 0]

            # Group by ressource and calculate the total overweight
            overweight_summary = df_overweight.groupby("Ressource")["Surpoids"].sum().reset_index()

            # Display the results
            st.subheader("Résumé des surpoids par ressource")
            st.dataframe(overweight_summary)

            # Bar chart of overweight by ressource
            st.subheader("Graphique des surpoids par ressource")
            bar_chart = alt.Chart(overweight_summary).mark_bar().encode(
                x=alt.X('Ressource:N', title='Ressource'),
                y=alt.Y('Surpoids:Q', title='Total du surpoids')
            )
            st.altair_chart(bar_chart, use_container_width=True)

    else:
        st.info("Veuillez charger un fichier XLSX.")

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Aller à", ["Analyse des poids", "Ressources avec surpoids"])

# Page routing
if page == "Analyse des poids":
    main_page()
elif page == "Ressources avec surpoids":
    overweight_page()
