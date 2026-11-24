"""Account list builder and outreach draft generator.

Reads a CSV of companies, filters them to a target profile, gives each a
simple score, and writes a ranked target list plus a personalised outreach
email draft for each company. Uses only pandas.

Usage:
    python gtm_automation.py sample_accounts.csv
"""
import sys
import pandas as pd

# ---- Settings you can change ----
TARGET_INDUSTRIES = {"Automotive", "Aerospace", "Machinery", "Chemicals"}
MIN_EMPLOYEES = 1000
SCORE_RULES = {            # points per rule
    "industry_match": 40,
    "large_company": 30,   # employees >= MIN_EMPLOYEES
    "has_pain_point": 20,
    "senior_contact": 10,
}
SENIOR_WORDS = ("head", "lead", "cfo", "director", "manager")
KEYWORDS = ("csrd", "cbam", "scope 3", "carbon", "emissions")


def score_row(row):
    s = 0
    if row["industry"] in TARGET_INDUSTRIES:
        s += SCORE_RULES["industry_match"]
    if row["employees"] >= MIN_EMPLOYEES:
        s += SCORE_RULES["large_company"]
    pain = str(row["pain_point"]).lower()
    if pain != "none listed" and any(k in pain for k in KEYWORDS):
        s += SCORE_RULES["has_pain_point"]
    if any(w in str(row["contact_role"]).lower() for w in SENIOR_WORDS):
        s += SCORE_RULES["senior_contact"]
    return s


def draft_email(row):
    first = str(row["contact_name"]).split()[0]
    return (
        f"Subject: {row['pain_point'].capitalize()} at {row['company']}\n\n"
        f"Hello {first},\n\n"
        f"I noticed that {row['company']} works in {row['industry'].lower()}, "
        f"where {row['pain_point']} is becoming a priority. "
        f"We help companies in your sector turn supplier and product data into "
        f"decisions on cost, compliance and carbon.\n\n"
        f"Would a 20-minute call next week be useful?\n\n"
        f"Best regards,\n[Your name]\n"
    )


def main(path):
    df = pd.read_csv(path)
    df["score"] = df.apply(score_row, axis=1)
    targets = df[(df["industry"].isin(TARGET_INDUSTRIES)) &
                 (df["employees"] >= MIN_EMPLOYEES)].sort_values(["score", "employees"], ascending=False)
    targets.to_csv("target_accounts_ranked.csv", index=False)
    with open("outreach_drafts.txt", "w", encoding="utf-8") as f:
        for _, row in targets.iterrows():
            f.write(f"=== {row['company']} (score {row['score']}) ===\n")
            f.write(draft_email(row) + "\n")
    print(f"{len(df)} companies read, {len(targets)} kept as targets.")
    print(targets[["company", "country", "score"]].to_string(index=False))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "sample_accounts.csv")
