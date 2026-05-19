"""
generate_dataset.py
Generates a CSV matching the schema of the Kaggle dataset:
'Global AI Tool Adoption Across Industries'
Run this once to produce ai_tool_adoption.csv
"""

import pandas as pd
import numpy as np

np.random.seed(42)

industries   = ["Healthcare", "Finance", "Retail", "Manufacturing",
                "Education", "Technology", "Legal", "Media"]
ai_tools     = ["ChatGPT", "GitHub Copilot", "Midjourney",
                "Gemini", "Claude", "Jasper"]
regions      = ["North America", "Europe", "Asia-Pacific",
                "Latin America", "Middle East & Africa"]
company_sizes= ["Small", "Medium", "Large", "Enterprise"]
years        = list(range(2019, 2025))

# Base adoption rates per industry (will be varied with noise)
base_rates = {
    "Technology": 72, "Finance": 65, "Healthcare": 55, "Media": 52,
    "Retail": 48, "Manufacturing": 44, "Education": 40, "Legal": 35,
}

rows = []
for year in years:
    year_multiplier = 1 + (year - 2019) * 0.10   # ~10% growth per year
    for industry in industries:
        for tool in ai_tools:
            for region in regions:
                for size in company_sizes:
                    size_boost = {"Small": 0, "Medium": 5, "Large": 10, "Enterprise": 18}[size]
                    region_boost = {
                        "North America": 10, "Europe": 5, "Asia-Pacific": 8,
                        "Latin America": -5, "Middle East & Africa": -8,
                    }[region]
                    base = base_rates[industry] * year_multiplier + size_boost + region_boost
                    adoption = min(98, max(5, base + np.random.normal(0, 4)))
                    users = max(0.1, (adoption / 100) * np.random.uniform(0.5, 5.0) * year_multiplier)

                    rows.append({
                        "Year": year,
                        "Industry": industry,
                        "AI_Tool": tool,
                        "Region": region,
                        "Company_Size": size,
                        "Adoption_Rate_%": round(adoption, 2),
                        "Number_of_Users_(Millions)": round(users, 3),
                    })

df = pd.DataFrame(rows)
df.to_csv("ai_tool_adoption.csv", index=False)
print(f"Dataset created: {len(df):,} rows × {len(df.columns)} columns")
print(df.head())
