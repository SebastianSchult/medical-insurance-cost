import csv
from sklearn.linear_model import LinearRegression
import numpy as np

ages = []
sexes = []
bmis = []
children = []
smokers = []
regions = []
charges = []

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

class InsuranceAnalyzer:
    def __init__(self, ages, sexes, bmis, children, smokers, regions, charges):
        self.ages = ages
        self.sexes = sexes
        self.bmis = bmis
        self.children = children
        self.smokers = smokers
        self.regions = regions
        self.charges = charges

        # Modell vorbereiten
        self.model = self._train_model()

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

    def _train_model(self):
        # Eingabedaten vorbereiten (Alter, BMI, Raucherstatus)
        X = []
        for age, bmi, smoker in zip(self.ages, self.bmis, self.smokers):
            smoker_numeric = 1 if smoker == "yes" else 0
            X.append([age, bmi, smoker_numeric])
        X = np.array(X)
        y = np.array(self.charges)

        model = LinearRegression()
        model.fit(X, y)
        return model

    def predict_charge(self, age, bmi, smoker_status):
        smoker_num = 1 if smoker_status.lower() == "yes" else 0
        input_data = np.array([[age, bmi, smoker_num]])
        return self.model.predict(input_data)[0]

# Objekt erstellen
analyzer = InsuranceAnalyzer(ages, sexes, bmis, children, smokers, regions, charges)

# Analyse ausgeben
print("💰 Gesamtdurchschnitt Versicherungskosten:", round(analyzer.average_cost(), 2))
print("🚬 Durchschnittskosten (Raucher):", round(analyzer.average_cost_by_smoker("yes"), 2))
print("🚭 Durchschnittskosten (Nichtraucher):", round(analyzer.average_cost_by_smoker("no"), 2))
print("👶 Durchschnittsalter mit Kindern:", round(analyzer.average_age_with_children(), 2))
print("🌍 Regionale Verteilung:", analyzer.region_distribution())
print("🚻 Geschlechterverteilung:", analyzer.gender_distribution())

# Vorhersagebeispiele
print("🔮 Prognose für 35 Jahre, BMI 28.5, Raucher:", round(analyzer.predict_charge(35, 28.5, "yes"), 2))
print("🔮 Prognose für 35 Jahre, BMI 28.5, Nichtraucher:", round(analyzer.predict_charge(35, 28.5, "no"), 2))