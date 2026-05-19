"""
Increasing Usage of AI — Exploratory Data Analysis
Dataset: Global AI Tool Adoption Across Industries (Kaggle)
Author: Osman Zaheeruddin Qazi
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

# ── Global style ──────────────────────────────────────────────────────────────
sns.set_theme(style="whitegrid", palette="Blues_d")
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.titlesize": 14,
    "axes.titleweight": "bold",
    "axes.titlepad": 12,
    "axes.labelsize": 11,
    "figure.dpi": 150,
})
NAVY   = "#1F3864"
TEAL   = "#2196A6"
CORAL  = "#E05A4E"
GOLD   = "#F0A500"
COLORS = [NAVY, TEAL, CORAL, GOLD, "#6BAF92", "#9B59B6", "#E67E22", "#27AE60"]

# ── Load data ─────────────────────────────────────────────────────────────────
df = pd.read_csv("ai_tool_adoption.csv")
print("Dataset shape:", df.shape)
print(df.head())
print(df.dtypes)

# ── Data cleaning ─────────────────────────────────────────────────────────────
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
df.dropna(inplace=True)
print("\nCleaned shape:", df.shape)

# =============================================================================
# Q1. Which industries have the highest AI adoption rates?
# =============================================================================
q1 = (df.groupby("industry")["adoption_rate_%"]
        .mean()
        .sort_values(ascending=False)
        .reset_index())

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.barh(q1["industry"], q1["adoption_rate_%"],
               color=[NAVY if i == 0 else TEAL for i in range(len(q1))])
ax.set_xlabel("Average AI Adoption Rate (%)")
ax.set_title("Q1: Which Industries Have the Highest AI Adoption Rates?")
ax.xaxis.set_major_formatter(mtick.PercentFormatter())
for bar, val in zip(bars, q1["adoption_rate_%"]):
    ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2,
            f"{val:.1f}%", va="center", fontsize=9)
plt.tight_layout()
plt.savefig("charts/q1_adoption_by_industry.png")
plt.close()
print("Saved: charts/q1_adoption_by_industry.png")

# =============================================================================
# Q2. How has global AI tool usage grown year-over-year?
# =============================================================================
q2 = (df.groupby("year")["number_of_users_(millions)"]
        .sum()
        .reset_index()
        .rename(columns={"number_of_users_(millions)": "total_users_m"}))

q2["yoy_growth_%"] = q2["total_users_m"].pct_change() * 100

fig, ax1 = plt.subplots(figsize=(10, 5))
ax2 = ax1.twinx()
ax1.bar(q2["year"], q2["total_users_m"], color=TEAL, alpha=0.7, label="Total Users (M)")
ax2.plot(q2["year"].iloc[1:], q2["yoy_growth_%"].iloc[1:],
         color=CORAL, marker="o", linewidth=2, label="YoY Growth %")
ax1.set_xlabel("Year")
ax1.set_ylabel("Total Users (Millions)", color=TEAL)
ax2.set_ylabel("YoY Growth (%)", color=CORAL)
ax1.set_title("Q2: How Has Global AI Tool Usage Grown Year-Over-Year?")
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")
plt.tight_layout()
plt.savefig("charts/q2_yoy_growth.png")
plt.close()
print("Saved: charts/q2_yoy_growth.png")

# =============================================================================
# Q3. Which AI tools are most widely adopted, and in which industries?
# =============================================================================
q3 = df.pivot_table(index="industry", columns="ai_tool",
                    values="adoption_rate_%", aggfunc="mean")
q3 = q3.fillna(0)

fig, ax = plt.subplots(figsize=(12, 7))
sns.heatmap(q3, annot=True, fmt=".1f", cmap="Blues", linewidths=0.5,
            linecolor="white", ax=ax, cbar_kws={"label": "Adoption Rate (%)"})
ax.set_title("Q3: AI Tool Adoption Rate by Industry (%)")
ax.set_xlabel("AI Tool")
ax.set_ylabel("Industry")
plt.xticks(rotation=30, ha="right")
plt.tight_layout()
plt.savefig("charts/q3_tool_by_industry_heatmap.png")
plt.close()
print("Saved: charts/q3_tool_by_industry_heatmap.png")

# =============================================================================
# Q4. What is the relationship between company size and AI adoption rate?
# =============================================================================
size_order = ["Small", "Medium", "Large", "Enterprise"]
q4 = (df.groupby("company_size")["adoption_rate_%"]
        .mean()
        .reindex(size_order)
        .reset_index())

fig, ax = plt.subplots(figsize=(8, 5))
palette = sns.color_palette([NAVY, TEAL, CORAL, GOLD])
sns.barplot(data=q4, x="company_size", y="adoption_rate_%",
            palette=palette, ax=ax, order=size_order)
ax.yaxis.set_major_formatter(mtick.PercentFormatter())
ax.set_xlabel("Company Size")
ax.set_ylabel("Average Adoption Rate (%)")
ax.set_title("Q4: Does Company Size Correlate With AI Adoption Rate?")
for p in ax.patches:
    ax.annotate(f"{p.get_height():.1f}%",
                (p.get_x() + p.get_width() / 2, p.get_height() + 0.4),
                ha="center", fontsize=10)
plt.tight_layout()
plt.savefig("charts/q4_adoption_by_company_size.png")
plt.close()
print("Saved: charts/q4_adoption_by_company_size.png")

# =============================================================================
# Q5. Which regions are leading in AI adoption?
# =============================================================================
q5 = (df.groupby("region")["adoption_rate_%"]
        .mean()
        .sort_values(ascending=False)
        .reset_index())

fig, ax = plt.subplots(figsize=(9, 5))
colors_q5 = [NAVY if i < 2 else TEAL for i in range(len(q5))]
ax.bar(q5["region"], q5["adoption_rate_%"], color=colors_q5)
ax.yaxis.set_major_formatter(mtick.PercentFormatter())
ax.set_xlabel("Region")
ax.set_ylabel("Average Adoption Rate (%)")
ax.set_title("Q5: Which Regions Are Leading in AI Adoption?")
for i, (_, row) in enumerate(q5.iterrows()):
    ax.text(i, row["adoption_rate_%"] + 0.3, f"{row['adoption_rate_%']:.1f}%",
            ha="center", fontsize=9)
plt.xticks(rotation=20, ha="right")
plt.tight_layout()
plt.savefig("charts/q5_adoption_by_region.png")
plt.close()
print("Saved: charts/q5_adoption_by_region.png")

print("\n✅ All 5 analysis charts saved to /charts/")
