import csv

# 1. Leere Listen vorbereiten
ages = []
sexes = []
bmis = []
children = []
smokers = []
regions = []
charges = []

# 2. insurance.csv einlesen und Daten speichern
with open("insurance.csv", newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        ages.append(int(row["age"]))
        sexes.append(row["sex"])
        bmis.append(float(row["bmi"]))
        children.append(int(row["children"]))
        smokers.append(row["smoker"])
        regions.append(row["region"])
        charges.append(float(row["charges"]))

# 3. Klasse zur Analyse definieren
class InsuranceAnalyzer:
    def __init__(self, ages, sexes, bmis, children, smokers, regions, charges):
        self.ages = ages
        self.sexes = sexes
        self.bmis = bmis
        self.children = children
        self.smokers = smokers
        self.regions = regions
        self.charges = charges

    def average_cost(self):
        return sum(self.charges) / len(self.charges)

    def average_cost_by_smoker(self, status="yes"):
        costs = [c for c, s in zip(self.charges, self.smokers) if s == status]
        return sum(costs) / len(costs) if costs else 0

    def average_age_with_children(self):
        relevant_ages = [a for a, c in zip(self.ages, self.children) if c > 0]
        return sum(relevant_ages) / len(relevant_ages) if relevant_ages else 0

    def region_distribution(self):
        result = {}
        for region in self.regions:
            result[region] = result.get(region, 0) + 1
        return result

    def gender_distribution(self):
        result = {}
        for sex in self.sexes:
            result[sex] = result.get(sex, 0) + 1
        return result

# 4. Analyseobjekt erstellen
analyzer = InsuranceAnalyzer(ages, sexes, bmis, children, smokers, regions, charges)

# 5. Analysen durchführen
print("💰 Gesamtdurchschnitt Versicherungskosten:", round(analyzer.average_cost(), 2))
print("🚬 Durchschnittskosten (Raucher):", round(analyzer.average_cost_by_smoker("yes"), 2))
print("🚭 Durchschnittskosten (Nichtraucher):", round(analyzer.average_cost_by_smoker("no"), 2))
print("👶 Durchschnittsalter mit Kindern:", round(analyzer.average_age_with_children(), 2))
print("🌍 Regionale Verteilung:", analyzer.region_distribution())
print("🚻 Geschlechterverteilung:", analyzer.gender_distribution())