from marketdata import Instrument,Position,PorteFeuille


if __name__ == "__main__":
    nvidia = Instrument("nvda", "Nvidia", "Technologie")
    microsoft = Instrument("msft", "Microsoft", "Technologie")

    portefeuille = PorteFeuille("PEA Adams")
    portefeuille.ajouter(Position(nvidia, 12, 158.40))
    portefeuille.ajouter(Position(microsoft, 5, 214.75))

    print(portefeuille)
    print("Taille du portefeuille :",len(portefeuille))
    print("Le montant investi toatl est de: ",portefeuille.montant_investi_total())

    # renforcement : 8 Nvidia de plus, a 175,00
    portefeuille.ajouter(Position(nvidia, 8, 175.00))
    print(portefeuille)
    print(portefeuille.positions[0])
    print(portefeuille.montant_investi_total())

    cours = {"NVDA": 171.20, "MSFT": 198.30}
    print(portefeuille.valeur_totale(cours))
    print(portefeuille.plus_value_totale(cours))

    try:
        portefeuille.supprimer("aapl")
    except ValueError as erreur:
        print("Refusé :", erreur)

    try:
        portefeuille.valeur_totale({"NVDA": 171.20})
    except ValueError as erreur:
        print("Refusé :", erreur)
    
    # le JSON produit
    print(json.dumps(portefeuille.to_dict(), indent=2, ensure_ascii=False))

    # aller-retour complet
    copie = PorteFeuille.from_dict(portefeuille.to_dict())
    print(copie)
    print(copie.positions[0])
    print(copie.montant_investi_total())
    
    portefeuille.sauvegarder("portefeuille.json")
    print("Sauvegardé.")

    recharge = PorteFeuille.charger("portefeuille.json")
    print(recharge)
    print(recharge.positions[0])
    print(recharge.montant_investi_total())

    try:
        PorteFeuille.charger("inexistant.json")
    except FileNotFoundError as erreur:
        print("Refusé :", erreur)