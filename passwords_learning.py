import asyncio
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans


async def read_passwords_from_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        passwords = file.read().splitlines()
    return passwords


async def preprocess_passwords(passwords):
    preprocessed_passwords = [re.sub(r"[^A-Za-z0-9]+", "", password) for password in passwords]
    return preprocessed_passwords


async def generate_regex():
    # Charger les mots de passe depuis le fichier
    passwords = await read_passwords_from_file("passwords.txt")

    # Prétraitement des mots de passe
    preprocessed_passwords = await preprocess_passwords(passwords)

    # Création des vecteurs de caractéristiques en utilisant TF-IDF
    vectorizer = TfidfVectorizer()
    features = vectorizer.fit_transform(preprocessed_passwords)

    # Clustering des mots de passe similaires en utilisant K-means
    kmeans = KMeans(n_clusters=1)  # Spécifiez le nombre de clusters souhaité
    kmeans.fit(features)

    # Récupération des mots de passe similaires dans le cluster
    cluster_passwords = [passwords[j] for j in range(len(passwords)) if kmeans.labels_[j] == 0]

    # Génération du regex à partir des mots de passe similaires
    regex = generate_regex_from_passwords(cluster_passwords)

    return regex


def generate_regex_from_passwords(passwords):
    # Implémentez ici votre algorithme pour générer le regex à partir des mots de passe donnés
    # ...
    regex = ""

    return regex


async def main():
    regex = await generate_regex()

    # Écriture du regex dans un fichier
    with open("generated_regex.txt", "w") as file:
        file.write(regex)

    print("Regex generated and saved successfully.")


asyncio.run(main())
