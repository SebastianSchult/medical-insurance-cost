import csv
from sklearn.linear_model import LinearRegression
import numpy as np
import tkinter as tk
from tkinter import messagebox

# Read data from CSV
ages, sexes, bmis, children, smokers, regions, charges = [], [], [], [], [], [], []

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
    """
    A class for analyzing and predicting medical insurance costs
    based on a given dataset.
    """

    def __init__(self, ages, sexes, bmis, children, smokers, regions, charges):
        """
        Initialize the InsuranceAnalyzer with dataset features and
        train the linear regression model.

        Args:
            ages (list): List of ages.
            sexes (list): List of genders.
            bmis (list): List of BMI values.
            children (list): List of number of children.
            smokers (list): List of smoker status.
            regions (list): List of regions.
            charges (list): List of insurance charges.
        """
        self.ages = ages
        self.sexes = sexes
        self.bmis = bmis
        self.children = children
        self.smokers = smokers
        self.regions = regions
        self.charges = charges
        self.model = self._train_model()

    def average_cost(self):
        """
        Calculate the average insurance cost in the dataset.

        Returns:
            float: Average cost.
        """
        return sum(self.charges) / len(self.charges)

    def average_cost_by_smoker(self, status="yes"):
        """
        Calculate the average insurance cost for smokers or non-smokers.

        Args:
            status (str): "yes" for smokers, "no" for non-smokers.

        Returns:
            float: Average cost for the given smoker status.
        """
        costs = [c for c, s in zip(self.charges, self.smokers) if s == status]
        return sum(costs) / len(costs) if costs else 0

    def average_age_with_children(self):
        """
        Calculate the average age of individuals with at least one child.

        Returns:
            float: Average age.
        """
        relevant_ages = [a for a, c in zip(self.ages, self.children) if c > 0]
        return sum(relevant_ages) / len(relevant_ages) if relevant_ages else 0

    def region_distribution(self):
        """
        Count the number of individuals in each region.

        Returns:
            dict: Region name as key and count as value.
        """
        result = {}
        for region in self.regions:
            result[region] = result.get(region, 0) + 1
        return result

    def gender_distribution(self):
        """
        Count the number of individuals by gender.

        Returns:
            dict: Gender as key and count as value.
        """
        result = {}
        for sex in self.sexes:
            result[sex] = result.get(sex, 0) + 1
        return result

    def _train_model(self):
        """
        Train a linear regression model using age, BMI, and smoker status.

        Returns:
            LinearRegression: Trained model.
        """
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
        """
        Predict insurance cost for a given person.

        Args:
            age (int): Age of the person.
            bmi (float): BMI of the person.
            smoker_status (str): "yes" or "no".

        Returns:
            float: Predicted insurance charge.
        """
        smoker_num = 1 if smoker_status.lower() == "yes" else 0
        input_data = np.array([[age, bmi, smoker_num]])
        return self.model.predict(input_data)[0]


def show_prediction_gui(analyzer):
    """
    Start a graphical interface (GUI) for predicting insurance costs.

    Allows the user to input age, BMI, number of children, smoker status,
    and region. Results are displayed and saved to a text file.
    """
    def on_predict():
        """
        Perform the prediction and show the result in the GUI.
        Save the result to a text file.
        """
        try:
            age = int(age_entry.get())
            bmi = float(bmi_entry.get())
            smoker = smoker_var.get()
            region = region_var.get()
            num_children = int(children_entry.get())

            prediction = analyzer.predict_charge(age, bmi, smoker)
            result_label.config(
                text=f"🔮 Predicted Cost: {round(prediction, 2)} $\n"
                     f"Region: {region}, Children: {num_children}"
            )

            with open("prediction_results.txt", "a") as f:
                f.write(f"Age: {age}, BMI: {bmi}, Smoker: {smoker}, Region: {region}, "
                        f"Children: {num_children}, Prediction: {round(prediction, 2)} $\n")

        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for age, BMI, and children.")

    # GUI Layout
    window = tk.Tk()
    window.title("Insurance Cost Prediction")
    window.geometry("400x350")

    tk.Label(window, text="Age:").pack()
    age_entry = tk.Entry(window)
    age_entry.pack()

    tk.Label(window, text="BMI:").pack()
    bmi_entry = tk.Entry(window)
    bmi_entry.pack()

    tk.Label(window, text="Number of Children:").pack()
    children_entry = tk.Entry(window)
    children_entry.pack()

    tk.Label(window, text="Smoker:").pack()
    smoker_var = tk.StringVar(window)
    smoker_var.set("no")
    tk.OptionMenu(window, smoker_var, "yes", "no").pack()

    tk.Label(window, text="Region:").pack()
    region_var = tk.StringVar(window)
    region_var.set("southeast")
    tk.OptionMenu(window, region_var, "southeast", "southwest", "northeast", "northwest").pack()

    tk.Button(window, text="Predict Cost", command=on_predict).pack(pady=10)

    result_label = tk.Label(window, text="", font=("Arial", 12, "bold"))
    result_label.pack()

    window.mainloop()


# Instantiate analyzer and display results
analyzer = InsuranceAnalyzer(ages, sexes, bmis, children, smokers, regions, charges)

print("💰 Average Insurance Cost:", round(analyzer.average_cost(), 2))
print("🚬 Average Cost (Smokers):", round(analyzer.average_cost_by_smoker("yes"), 2))
print("🚭 Average Cost (Non-Smokers):", round(analyzer.average_cost_by_smoker("no"), 2))
print("👶 Average Age with Children:", round(analyzer.average_age_with_children(), 2))
print("🌍 Region Distribution:", analyzer.region_distribution())
print("🚻 Gender Distribution:", analyzer.gender_distribution())
print("🔮 Prediction for 35 y/o, BMI 28.5, Smoker:", round(analyzer.predict_charge(35, 28.5, "yes"), 2))
print("🔮 Prediction for 35 y/o, BMI 28.5, Non-Smoker:", round(analyzer.predict_charge(35, 28.5, "no"), 2))

# Launch GUI
show_prediction_gui(analyzer)