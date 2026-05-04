import hashlib

# propose à l'utilisateur de hacher un texte et récupere le input
def hacher_texte():
    texte = input("Entrez le texte à hacher : ")

    # si l'utilisateur écris rien et juste appuis sur entrer ce gros débil bah ca affiche un msg d'erreur
    if texte.strip() == "":
        print("Erreur : le texte ne peut pas être vide.")
        return

    # le hash
    hash_sha256 = hashlib.sha256(texte.encode("utf-8")).hexdigest()

    print("\nSHA-256 :", hash_sha256)
    proposer_sauvegarde("Texte saisi", texte, hash_sha256)


# propose à l'utilisateur de hacher un fichier et récupere le input
def hacher_fichier():
    chemin = input("Entrez le chemin du fichier à hacher : ")

    # au cas ou le mec donne pas le chemin d'accès
    if chemin.strip() == "":
        print("Erreur : le chemin du fichier ne peut pas être vide.")
        return

    # récupere le chemin d'accès, le lit et affiche le hash
    try:
        with open(chemin, "rb") as fichier:
            contenu = fichier.read()
            hash_sha256 = hashlib.sha256(contenu).hexdigest()

        print("\nSHA-256 :", hash_sha256)
        proposer_sauvegarde("Fichier", chemin, hash_sha256)

    # gestions des erreurs
    except FileNotFoundError:
        print("Erreur : fichier introuvable.")
    except PermissionError:
        print("Erreur : permission refusée pour lire ce fichier.")
    except Exception as e:
        print("Une erreur est survenue :", e)


# propose à l'utilisateur de sauvegarder le hash
def proposer_sauvegarde(type_input, input_utilisateur, hash_resultat):
    choix = input("\nVoulez-vous sauvegarder le hash dans hash_output.txt ? (o/n) : ")

    # si oui :
    if choix.lower() == "o":
        try:
            with open("hash_output.txt", "w", encoding="utf-8") as fichier:
                fichier.write(type_input + " : " + input_utilisateur + "\n")
                fichier.write("SHA-256 : " + hash_resultat + "\n")

            print("Le hash a été sauvegardé dans hash_output.txt.")

        except Exception as e:
            print("Erreur lors de la sauvegarde :", e)

# le script qui va faire fonctionner tout le code qu'on a fait au dessus
def main():
    print("Choisissez une option :")
    print()
    print("[1] Hacher un texte")
    print("[2] Hacher un fichier")
    print()

    choix = input("Votre choix : ")

    if choix == "1":
        hacher_texte()
    elif choix == "2":
        hacher_fichier()
    else:
        print("Erreur : choix invalide.")


if __name__ == "__main__":
    main()