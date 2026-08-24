
def main() -> None: 
    chaine = "nb_drones: 5"
    try:
        partie1, partie2 = chaine.split(":")
        partie1 = partie1.strip()
        partie2 = partie2.strip()
    except ValueError as e:
        raise e
    print(partie1)
    print(partie2)

if __name__ == "__main__":
    try:
        main()
    except ValueError as e:
        print(e)