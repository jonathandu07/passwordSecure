import re
import random
import string
import asyncio

regex = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-])[A-Za-z0-9#?!@$%^&*-]{8,}$"


valid_passwords = []

# Lecture des mots de passe existants
with open("passwords.txt", "r", encoding="utf-8") as file:
    existing_passwords = file.read().splitlines()

# Filtrage des mots de passe valides
for password in existing_passwords:
    if re.match(regex, password):
        valid_passwords.append(password)

# Génération de 10 millions de mots de passe
async def generate_passwords():
    generated_passwords = []
    while len(generated_passwords) < 10000000:
        password = ''.join(random.choices(string.ascii_letters + string.digits + "#?!@$%^&*-", k=8))
        if re.match(regex, password):
            generated_passwords.append(password)
    return generated_passwords

async def main():
    generated_passwords = await generate_passwords()

    # Stockage des mots de passe générés dans un fichier
    with open("generated_passwords.txt", "w", encoding="utf-8") as file:
        file.write("\n".join(generated_passwords))

    print("Les 10 millions de mots de passe générés ont été stockés dans generated_passwords.txt.")

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
