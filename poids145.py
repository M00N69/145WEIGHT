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
            st.subheader("Boxplots des poids des packs par ressource et lot")

            # Boxplot Altair
            chart = (
                alt.Chart(df)
                .mark_boxplot()
                .encode(
                    alt.X("LOT PROTEAN:N", title="LOT PROTEAN"),
                    alt.Y("PackWeight:Q", title="Poids du pack")
                )
            )
            st.altair_chart(chart, use_container_width=True)

            # Boxplot Matplotlib
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.boxplot([df[df["LOT PROTEAN"] == lot]["PackWeight"] for lot in df["LOT PROTEAN"].unique()], vert=False, patch_artist=True, labels=df["LOT PROTEAN"].unique())
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

        # Suppression de la colonne BatchNumber
        df = df.drop("BatchNumber", axis=1)

        # Convertir la colonne Timestamp en datetime
        df["Timestamp"] = pd.to_datetime(df["Timestamp"], format='%d/%m/%Y %H:%M:%S', errors='coerce')

        # Vérifier si la conversion a réussi
        if df["Timestamp"].isnull().any():
            st.error("Certaines valeurs de Timestamp ne peuvent pas être converties. Veuillez vérifier le format des dates dans le fichier.")
        else:
            # Calcul du surpoids basé sur le poids médian par ressource
            median_weights = df.groupby("Ressource")["PackWeight"].median().reset_index()
            median_weights.columns = ["Ressource", "MedianWeight"]
            df = df.merge(median_weights, on="Ressource")
            df["Surpoids"] = df["PackWeight"] - df["MedianWeight"]

            # Filtrer les ressources avec surpoids
            df_overweight = df[df["Surpoids"] > 0]

            # Grouper par ressource et calculer le surpoids total
            overweight_summary = df_overweight.groupby("Ressource")["Surpoids"].sum().reset_index()

            # Afficher les résultats
            st.subheader("Résumé des surpoids par ressource")
            st.dataframe(overweight_summary)

            # Statistiques descriptives
            st.subheader("Statistiques descriptives des surpoids par ressource")
            descriptive_stats = df_overweight.groupby("Ressource")["Surpoids"].describe()
            st.dataframe(descriptive_stats)

            # Graphique en barres des surpoids par ressource
            st.subheader("Graphique des surpoids par ressource")
            bar_chart = alt.Chart(overweight_summary).mark_bar().encode(
                x=alt.X('Ressource:N', title='Ressource'),
                y=alt.Y('Surpoids:Q', title='Total du surpoids')
            )
            st.altair_chart(bar_chart, use_container_width=True)

            # Histogramme des surpoids par ressource
            st.subheader("Histogramme des surpoids par ressource")
            for res in df_overweight["Ressource"].unique():
                res_data = df_overweight[df_overweight["Ressource"] == res]
                st.write(f"Ressource: {res}")
                fig, ax = plt.subplots(figsize=(12, 6))
                ax.hist(res_data["Surpoids"], bins=20, color='blue', edgecolor='black')
                ax.set_xlabel("Surpoids")
                ax.set_ylabel("Fréquence")
                ax.set_title(f"Histogramme des surpoids pour la ressource {res}")
                st.pyplot(fig)

    else:
        st.info("Veuillez charger un fichier XLSX.")

# Barre latérale de navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Aller à", ["Analyse des poids", "Ressources avec surpoids"])

# Routage des pages
if page == "Analyse des poids":
    main_page()
elif page == "Ressources avec surpoids":
    overweight_page()
