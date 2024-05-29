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

            # Option d'exportation des données de surpoids
            csv = overweight_summary.to_csv(index=False)
            st.download_button(
                label="Télécharger le résumé des surpoids en CSV",
                data=csv,
                file_name='surpoids_par_ressource.csv',
                mime='text/csv',
            )

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

def report_page():
    st.title("Rapport d'analyse des surpoids par ressource")

    # Upload du fichier CSV contenant le résumé des surpoids
    uploaded_file = st.file_uploader("Upload the surpoids summary CSV file", type=["csv"], key="report")

    if uploaded_file is not None:
        # Lecture du fichier CSV
        df_surpoids = pd.read_csv(uploaded_file)

        # Calcul des statistiques descriptives
        stats = df_surpoids['Surpoids'].describe()

        # Affichage du rapport
        st.markdown("### Vue d'ensemble")
        st.write("Les données de surpoids par ressource montrent le total des surpoids pour chaque ressource. Analysons ces informations en détail.")

        st.markdown("### Distribution des Surpoids")
        st.write("Voici une analyse statistique descriptive pour mieux comprendre la distribution des surpoids.")
        
        st.markdown("#### Statistiques Descriptives")
        st.write(stats)

        st.markdown("### Résultats Statistiques")
        st.markdown(f"""
        - **Count** : {stats['count']} - Nombre de ressources analysées.
        - **Mean** : {stats['mean']:.2f} - Surpoids moyen.
        - **Std** : {stats['std']:.2f} - Ecart-type du surpoids, indiquant la dispersion des surpoids par rapport à la moyenne.
        - **Min** : {stats['min']:.2f} - Surpoids minimum enregistré.
        - **25%** : {stats['25%']:.2f} - Premier quartile, 25% des ressources ont un surpoids inférieur à cette valeur.
        - **50%** : {stats['50%']:.2f} - Médiane, la moitié des ressources ont un surpoids inférieur à cette valeur.
        - **75%** : {stats['75%']:.2f} - Troisième quartile, 75% des ressources ont un surpoids inférieur à cette valeur.
        - **Max** : {stats['max']:.2f} - Surpoids maximum enregistré.
        """)

        st.markdown("### Graphique des Surpoids par Ressource")
        st.write("Pour visualiser les données, nous allons créer un graphique en barres montrant le surpoids total par ressource.")
        
        # Graphique en barres
        fig, ax = plt.subplots(figsize=(14, 7))
        ax.bar(df_surpoids['Ressource'].astype(str), df_surpoids['Surpoids'], color='skyblue')
        ax.set_xlabel('Ressource')
        ax.set_ylabel('Total du surpoids (g)')
        ax.set_title('Total du surpoids par ressource')
        plt.xticks(rotation=90)
        st.pyplot(fig)

        st.markdown("### Interprétation des Résultats")
        st.markdown("""
        1. **Ressources avec le plus de surpoids** :
            - Les ressources 1127.0, 4470.0 et 14969.0 ont les surpoids totaux les plus élevés, avec des surpoids de 213147.0 g, 129966.0 g, et 202415.0 g respectivement.
        
        2. **Ressources avec le moins de surpoids** :
            - Les ressources ayant les surpoids les plus faibles peuvent indiquer une meilleure conformité aux poids médians attendus. Par exemple, la ressource 5359.0 a un surpoids de seulement 7161.0 g.
        
        3. **Variation des surpoids** :
            - Une variation significative dans les surpoids totaux entre les différentes ressources peut indiquer des problèmes spécifiques liés à certaines ressources, tels que des erreurs de production, des matières premières de qualité variable, ou des processus de fabrication inconsistants.
        """)

        st.markdown("### Actions Recommandées")
        st.markdown("""
        1. **Inspection des Processus de Production** :
            - Effectuer une revue détaillée des processus de production pour les ressources avec les surpoids les plus élevés. Rechercher les étapes où des écarts peuvent se produire.
        
        2. **Recalibration des Équipements** :
            - Vérifier et recalibrer les équipements de mesure et de production pour les ressources problématiques afin de réduire les écarts de poids.
        
        3. **Formation et Sensibilisation** :
            - Former les opérateurs sur l'importance de maintenir les poids des packs dans les limites spécifiées. Sensibiliser le personnel aux impacts des surpoids sur la qualité et les coûts.
        
        4. **Analyse Continue** :
            - Mettre en place un système de surveillance continue des poids pour identifier et corriger rapidement les écarts.
        
        5. **Comparaison avec les Standards de l'Industrie** :
            - Comparer les résultats obtenus avec les standards de l'industrie pour s'assurer que les performances sont alignées avec les meilleures pratiques.
        """)

        st.markdown("### Conclusion")
        st.write("L'analyse des surpoids par ressource a permis d'identifier les ressources les plus problématiques en termes de surpoids. En prenant des mesures correctives ciblées, il est possible de réduire les écarts et d'améliorer la conformité des poids des packs, conduisant à une meilleure qualité et une réduction des coûts associés aux surpoids.")
    else:
        st.info("Veuillez charger un fichier CSV contenant le résumé des surpoids.")

# Barre latérale de navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Aller à", ["Analyse des poids", "Ressources avec surpoids", "Rapport d'analyse"])

# Routage des pages
if page == "Analyse des poids":
    main_page()
elif page == "Ressources avec surpoids":
    overweight_page()
elif page == "Rapport d'analyse":
    report_page()
