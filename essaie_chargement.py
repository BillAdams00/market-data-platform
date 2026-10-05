from instrument import PorteFeuille

portefeuille = PorteFeuille.charger("portefeuille.json")
print(portefeuille)
print(portefeuille.positions[0])
print(portefeuille.montant_investi_total())