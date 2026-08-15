import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

india_data = pd.read_csv("Unemployment in India.csv")
rate_data = pd.read_csv("Unemployment_Rate_upto_11_2020.csv")

india_data.columns = india_data.columns.str.strip()
rate_data.columns = rate_data.columns.str.strip()


rename_map = {
    "Estimated Unemployment Rate (%)": "UnemploymentRate",
    "Estimated Employed": "Employed",
    "Estimated Labour Participation Rate (%)": "LabourParticipation"
}
india_data = india_data.rename(columns=rename_map)
rate_data = rate_data.rename(columns=rename_map)


india_data["Date"] = pd.to_datetime(india_data["Date"], errors="coerce", dayfirst=True)
rate_data["Date"] = pd.to_datetime(rate_data["Date"], errors="coerce", dayfirst=True)



india_data = india_data[["Region", "Date", "UnemploymentRate", "Employed", "LabourParticipation"]]
rate_data = rate_data[["Region", "Date", "UnemploymentRate", "Employed", "LabourParticipation"]]



data = pd.concat([india_data, rate_data], ignore_index=True)
data = data.drop_duplicates()

data = data.loc[:, ~data.columns.duplicated()]

print("Columns:", data.columns.tolist())
print(data.info())
print(data.describe())



region_avg = data.groupby("Region")["UnemploymentRate"].mean().sort_values(ascending=False)
print("\nAverage Unemployment Rate by Region:\n", region_avg)



plt.figure(figsize=(12,6))
sns.lineplot(data=data, x="Date", y="UnemploymentRate", hue="Region")
plt.title("Unemployment Trends by Region")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


covid_period = data[(data["Date"] >= "2020-04-01") & (data["Date"] <= "2020-06-30")]
plt.figure(figsize=(10,5))
sns.barplot(data=covid_period, x="Region", y="UnemploymentRate")
plt.title("COVID-19 Impact on Unemployment (Apr–Jun 2020)")
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

data["Month"] = data["Date"].dt.month
monthly_avg = data.groupby("Month")["UnemploymentRate"].mean()
plt.figure(figsize=(8,5))
sns.lineplot(x=monthly_avg.index, y=monthly_avg.values, marker="o")
plt.title("Average Monthly Unemployment Trend")
plt.xlabel("Month")
plt.ylabel("Unemployment Rate (%)")
plt.tight_layout()
plt.show()

