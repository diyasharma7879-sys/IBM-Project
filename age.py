import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.io as pio


pio.renderers.default = "browser"

class AgeCalculatorProject:
    def __init__(self):
        print("--- University Project: Age Analytics & Calculator ---")
        print("Initializing Data Science Libraries...\n")

    def get_user_dob(self):
        """Gets valid date of birth from user."""
        while True:
            try:
                dob_str = input("Please enter your Date of Birth (YYYY-MM-DD): ")
            except EOFError:
                print("\n[System] Interactive input not available (EOF). Using default: 2000-01-01")
                return datetime.date(2000, 1, 1)

            try:
                dob = datetime.datetime.strptime(dob_str, "%Y-%m-%d").date()
                if dob > datetime.date.today():
                    print("Error: Date of birth cannot be in the future.")
                    continue
                return dob
            except ValueError:
                print("Invalid format. Please use YYYY-MM-DD (e.g., 2000-05-15).")

    def calculate_precise_age(self, dob):
        """Calculates precise age using datetime math."""
        today = datetime.date.today()
        years = today.year - dob.year
        months = today.month - dob.month
        days = today.day - dob.day

        if months < 0 or (months == 0 and days < 0):
            years -= 1
            months += 12

        if days < 0:

            prev_month = today.month - 1 if today.month > 1 else 12
            prev_year = today.year if today.month > 1 else today.year - 1
            days_in_prev_month = (datetime.date(today.year, today.month, 1) - datetime.timedelta(days=1)).day
            days += days_in_prev_month
            months -= 1

        return years, months, days

    def generate_population_data(self, n_samples=500):
        """
        Uses NUMPY to generate a random distribution of ages
        to simulate a university campus environment.
        """
        print(f"\n[NumPy] Generating synthetic dataset of {n_samples} individuals...")

        group1 = np.random.normal(loc=20, scale=2, size=int(n_samples * 0.7))

        group2 = np.random.normal(loc=35, scale=10, size=int(n_samples * 0.3))

        ages = np.concatenate([group1, group2])
        ages = np.abs(ages)
        ages = np.round(ages).astype(int)

        return ages

    def analyze_with_pandas(self, ages, user_age_years):
        """
        Uses PANDAS to create a DataFrame and categorize data.
        """
        print("[Pandas] Processing data frames...")
        df = pd.DataFrame(ages, columns=['Age'])

        def categorize(age):
            if age < 20: return 'Teen'
            elif 20 <= age < 30: return 'Young Adult'
            elif 30 <= age < 50: return 'Adult'
            else: return 'Senior'

        df['Category'] = df['Age'].apply(categorize)

        mean_age = df['Age'].mean()
        percentile = (df[df['Age'] < user_age_years].shape[0] / len(df)) * 100

        print(f"\n--- Statistics ---")
        print(f"Population Mean Age: {mean_age:.2f}")
        print(f"Your Age: {user_age_years}")
        print(f"You are older than {percentile:.1f}% of the simulated population.")

        return df

    def visualize_matplotlib_seaborn(self, df, user_age):
        """
        Uses SEABORN and MATPLOTLIB for statistical visualization.
        """
        print("[Seaborn/Matplotlib] Generating distribution plot...")
        plt.figure(figsize=(10, 6))
        sns.set_theme(style="whitegrid")

        sns.histplot(df['Age'], kde=True, color='skyblue', bins=20)

        plt.axvline(x=user_age, color='red', linestyle='--', linewidth=2, label=f'You ({user_age})')

        plt.title('Age Distribution Analysis (University Context)', fontsize=15)
        plt.xlabel('Age')
        plt.ylabel('Count')
        plt.legend()
        plt.show()

    def visualize_plotly(self, df):
        """
        Uses PLOTLY for an interactive pie chart.
        """
        print("[Plotly] Generating interactive pie chart...")

        counts = df['Category'].value_counts().reset_index()
        counts.columns = ['Category', 'Count']

        fig = px.pie(
            counts,
            values='Count',
            names='Category',
            title='Population Age Groups',
            color_discrete_sequence=px.colors.sequential.RdBu
        )

        fig.update_traces(textposition='inside', textinfo='percent+label')

        try:
            fig.show()
        except Exception as e:
            print(f"\n[System] Could not open browser for Plotly: {e}")
            print("[System] This is normal in online compilers. Saving to 'age_groups.html' instead.")
            try:
                fig.write_html("age_groups.html")
                print("[System] Plot saved successfully as 'age_groups.html'")
            except Exception as e2:
                print(f"[System] Could not save file: {e2}")

    def run(self):

        dob = self.get_user_dob()

        years, months, days = self.calculate_precise_age(dob)
        print(f"\n>>> RESULT: You are {years} years, {months} months, and {days} days old.")

        population_ages = self.generate_population_data()

        df = self.analyze_with_pandas(population_ages, years)

        print("Displaying static plot...")
        self.visualize_matplotlib_seaborn(df, years)

        self.visualize_plotly(df)

if __name__ == "__main__":
    app = AgeCalculatorProject()
    app.run()