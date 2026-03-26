"""
Nonprofit Fundraising - Exploratory Data Analysis
Author: Oguz Tuncel
GitHub: linkedin.com/in/oguztuncel
Description: End-to-end EDA of fundraising data including
             donor segmentation, campaign performance,
             channel analysis, and trend visualisation.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

# ── Style ──────────────────────────────────────────────────────
plt.rcParams.update({
    "font.family": "sans-serif",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.titlesize": 13,
    "axes.titleweight": "bold",
    "figure.dpi": 120
})
PURPLE = "#534AB7"
TEAL   = "#1D9E75"
COLORS = [PURPLE, TEAL, "#EF9F27", "#E24B4A", "#3B8BD4", "#D4537E", "#888780", "#9FE1CB"]

# ── Load Data ──────────────────────────────────────────────────
donors    = pd.read_csv("data/donors.csv", parse_dates=["acquisition_date"])
donations = pd.read_csv("data/donations.csv", parse_dates=["donation_date"])

# Keep only completed donations
completed = donations[donations["status"] == "Completed"].copy()

print("=" * 55)
print("  NONPROFIT FUNDRAISING — EDA SUMMARY")
print("=" * 55)
print(f"  Total Donors        : {len(donors):,}")
print(f"  Total Donations     : {len(completed):,}")
print(f"  Total Raised        : ${completed['amount'].sum():,.0f}")
print(f"  Average Gift        : ${completed['amount'].mean():,.2f}")
print(f"  Median Gift         : ${completed['amount'].median():,.2f}")
print(f"  Recurring Rate      : {completed['is_recurring'].mean()*100:.1f}%")
print("=" * 55)

# ── 1. CAMPAIGN PERFORMANCE ────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle("Campaign Performance", fontsize=15, fontweight="bold", color=PURPLE)

camp = (completed.groupby("campaign")["amount"]
        .agg(["sum", "count", "mean"])
        .rename(columns={"sum": "total", "count": "donations", "mean": "avg"})
        .sort_values("total", ascending=True))

axes[0].barh(camp.index, camp["total"] / 1e3, color=TEAL, edgecolor="white")
axes[0].set_xlabel("Total Raised ($000s)")
axes[0].set_title("Revenue by Campaign")
for i, v in enumerate(camp["total"] / 1e3):
    axes[0].text(v + 10, i, f"${v:,.0f}k", va="center", fontsize=9)

axes[1].barh(camp.index, camp["avg"], color=PURPLE, edgecolor="white")
axes[1].set_xlabel("Average Donation ($)")
axes[1].set_title("Average Gift by Campaign")
for i, v in enumerate(camp["avg"]):
    axes[1].text(v + 5, i, f"${v:,.0f}", va="center", fontsize=9)

plt.tight_layout()
plt.savefig("outputs/01_campaign_performance.png", bbox_inches="tight")
plt.close()
print("✓ Chart 1 saved: Campaign Performance")

# ── 2. MONTHLY TREND ──────────────────────────────────────────
monthly = (completed.groupby(completed["donation_date"].dt.to_period("M"))["amount"]
           .sum().reset_index())
monthly["donation_date"] = monthly["donation_date"].dt.to_timestamp()

fig, ax = plt.subplots(figsize=(14, 5))
ax.fill_between(monthly["donation_date"], monthly["amount"] / 1e3,
                alpha=0.3, color=TEAL)
ax.plot(monthly["donation_date"], monthly["amount"] / 1e3,
        color=TEAL, linewidth=2.5)
ax.set_title("Monthly Fundraising Trend (2022–2024)",
             fontsize=13, fontweight="bold", color=PURPLE)
ax.set_ylabel("Total Raised ($000s)")
ax.set_xlabel("")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}k"))
plt.tight_layout()
plt.savefig("outputs/02_monthly_trend.png", bbox_inches="tight")
plt.close()
print("✓ Chart 2 saved: Monthly Trend")

# ── 3. DONOR TYPE BREAKDOWN ───────────────────────────────────
merged = completed.merge(donors[["donor_id", "donor_type"]], on="donor_id")
dtype_rev = merged.groupby("donor_type")["amount"].sum().sort_values(ascending=False)

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
fig.suptitle("Donor Type Analysis", fontsize=15, fontweight="bold", color=PURPLE)

axes[0].pie(dtype_rev, labels=dtype_rev.index, autopct="%1.1f%%",
            colors=COLORS[:len(dtype_rev)], startangle=90,
            wedgeprops={"edgecolor": "white", "linewidth": 2})
axes[0].set_title("Revenue Share by Donor Type")

dtype_count = merged.groupby("donor_type")["donor_id"].nunique().sort_values(ascending=False)
axes[1].bar(dtype_count.index, dtype_count.values,
            color=COLORS[:len(dtype_count)], edgecolor="white")
axes[1].set_title("Number of Donors by Type")
axes[1].set_ylabel("Count")
for i, v in enumerate(dtype_count.values):
    axes[1].text(i, v + 2, str(v), ha="center", fontweight="bold")

plt.tight_layout()
plt.savefig("outputs/03_donor_type.png", bbox_inches="tight")
plt.close()
print("✓ Chart 3 saved: Donor Type")

# ── 4. CHANNEL ANALYSIS ───────────────────────────────────────
channel = (completed.groupby("channel")["amount"]
           .agg(["sum", "count"])
           .rename(columns={"sum": "total", "count": "donations"})
           .sort_values("total", ascending=False))

fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.bar(channel.index, channel["total"] / 1e3,
              color=COLORS[:len(channel)], edgecolor="white")
ax.set_title("Revenue by Acquisition Channel",
             fontsize=13, fontweight="bold", color=PURPLE)
ax.set_ylabel("Total Raised ($000s)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}k"))
for bar in bars:
    h = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2, h + 5,
            f"${h:,.0f}k", ha="center", fontsize=9, fontweight="bold")
plt.tight_layout()
plt.savefig("outputs/04_channel_analysis.png", bbox_inches="tight")
plt.close()
print("✓ Chart 4 saved: Channel Analysis")

# ── 5. GEOGRAPHIC ANALYSIS ────────────────────────────────────
geo = (merged.groupby(donors.set_index("donor_id").reindex(merged["donor_id"])["state"].values)
       ["amount"].sum().sort_values(ascending=False))
geo.index.name = "state"

fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.bar(geo.index, geo.values / 1e3,
              color=PURPLE, edgecolor="white", alpha=0.85)
ax.set_title("Revenue by State",
             fontsize=13, fontweight="bold", color=PURPLE)
ax.set_ylabel("Total Raised ($000s)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}k"))
for bar in bars:
    h = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2, h + 5,
            f"${h:,.0f}k", ha="center", fontsize=9)
plt.tight_layout()
plt.savefig("outputs/05_geographic.png", bbox_inches="tight")
plt.close()
print("✓ Chart 5 saved: Geographic")

# ── 6. YEAR-OVER-YEAR COMPARISON ─────────────────────────────
yoy = (completed.groupby(["year", "campaign"])["amount"]
       .sum().reset_index())

fig, ax = plt.subplots(figsize=(14, 6))
campaigns_list = yoy["campaign"].unique()
x = np.arange(len(campaigns_list))
width = 0.25
years = sorted(yoy["year"].unique())

for i, yr in enumerate(years):
    vals = [yoy[(yoy["year"] == yr) & (yoy["campaign"] == c)]["amount"].sum()
            for c in campaigns_list]
    bars = ax.bar(x + i * width, [v / 1e3 for v in vals],
                  width, label=str(yr),
                  color=COLORS[i], edgecolor="white")

ax.set_title("Year-over-Year Campaign Revenue",
             fontsize=13, fontweight="bold", color=PURPLE)
ax.set_xticks(x + width)
ax.set_xticklabels(campaigns_list, rotation=25, ha="right")
ax.set_ylabel("Total Raised ($000s)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}k"))
ax.legend(title="Year")
plt.tight_layout()
plt.savefig("outputs/06_yoy_campaign.png", bbox_inches="tight")
plt.close()
print("✓ Chart 6 saved: Year-over-Year")

# ── 7. DONOR RETENTION ───────────────────────────────────────
donor_years = (completed.groupby(["donor_id", "year"])
               .size().reset_index(name="donations"))
donor_years = donor_years.sort_values(["donor_id", "year"])
donor_years["prev_year"] = donor_years.groupby("donor_id")["year"].shift(1)
donor_years["retained"] = (donor_years["year"] - donor_years["prev_year"]) == 1

retention = donor_years.groupby("year").agg(
    new_donors=("prev_year", lambda x: x.isna().sum()),
    retained_donors=("retained", "sum")
).reset_index()

fig, ax = plt.subplots(figsize=(8, 5))
x = np.arange(len(retention))
ax.bar(x - 0.2, retention["new_donors"], 0.4,
       label="New Donors", color=TEAL, edgecolor="white")
ax.bar(x + 0.2, retention["retained_donors"], 0.4,
       label="Retained Donors", color=PURPLE, edgecolor="white")
ax.set_xticks(x)
ax.set_xticklabels(retention["year"])
ax.set_title("Donor Retention — New vs Returning",
             fontsize=13, fontweight="bold", color=PURPLE)
ax.set_ylabel("Number of Donors")
ax.legend()
plt.tight_layout()
plt.savefig("outputs/07_retention.png", bbox_inches="tight")
plt.close()
print("✓ Chart 7 saved: Donor Retention")

print("\n✅ All charts saved to outputs/ folder")
print("=" * 55)
