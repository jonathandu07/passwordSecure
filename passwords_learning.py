import re
import asyncio
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

# Fonction pour évaluer la sécurité d'un mot de passe
def evaluate_password_security(password):
    security_level = 0

    # Vérification des critères de sécurité
    if re.search(r"[A-Z]", password):
        security_level += 1
    if re.search(r"[a-z]", password):
        security_level += 1
    if re.search(r"\d", password):
        security_level += 1
    if re.search(r"[#?!@$%^&*-]", password):
        security_level += 1

    return security_level

# Fonction pour lire les mots de passe depuis un fichier de manière asynchrone
async def read_passwords_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        passwords = file.read().splitlines()
        passwords = [password.strip() for password in passwords]
        return passwords

# Fonction pour évaluer la sécurité des mots de passe en utilisant le machine learning
async def evaluate_password_security_ml(passwords):
    # Prétraitement des mots de passe en enlevant les caractères spéciaux
    preprocessed_passwords = [re.sub(r"[^A-Za-z0-9]+", "", password) for password in passwords]

    # Création des vecteurs de caractéristiques en utilisant TF-IDF
    vectorizer = TfidfVectorizer()
    features = vectorizer.fit_transform(preprocessed_passwords)

    # Clustering des mots de passe similaires en utilisant K-means
    kmeans = KMeans(n_clusters=5)  # Spécifiez le nombre de clusters souhaité
    kmeans.fit(features)

    # Rapport de sécurité des mots de passe
    report = []
    report.append("Rapport de sécurité des mots de passe\n")

    for i in range(kmeans.n_clusters):
        cluster_passwords = [passwords[j] for j in range(len(passwords)) if kmeans.labels_[j] == i]
        report.append(f"Cluster {i+1} - Nombre de mots de passe : {len(cluster_passwords)}")
        report.extend(cluster_passwords)
        report.append("")

    return report

# Fonction principale asynchrone
async def main():
    # Lecture des mots de passe du fichier generated_passwords.txt de manière asynchrone
    generated_passwords = await read_passwords_from_file("generated_passwords.txt")

    # Lecture des mots de passe du fichier passwords.txt de manière asynchrone
    existing_passwords = await read_passwords_from_file("passwords.txt")

    # Évaluation de la sécurité des mots de passe en utilisant le machine learning de manière asynchrone
    generated_report = await evaluate_password_security_ml(generated_passwords)
    existing_report = await evaluate_password_security_ml(existing_passwords)

    # Écriture du rapport dans un fichier
    with open("password_security_report.txt", "w", encoding="utf-8") as file:
        file.write("\n".join(generated_report + existing_report))

    print("Le rapport de sécurité des mots de passe a été généré dans le fichier password_security_report.txt.")

# Exécution de la fonction principale asynchrone
asyncio.run(main())
