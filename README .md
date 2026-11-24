# GTM Account List and Outreach Draft Automation

A small Python script that automates two repetitive go-to-market tasks:

1. **Build a ranked target account list.** It reads a CSV of companies, keeps the ones that match a target profile (industry and size) and scores them.
2. **Draft personalised outreach emails** for each target company.

All data in `sample_accounts.csv` is made up for demonstration.

## Run
    pip install pandas
    python gtm_automation.py sample_accounts.csv

Outputs: `target_accounts_ranked.csv` and `outreach_drafts.txt`.

## Settings
Change the target industries, minimum company size and scoring points at the top of `gtm_automation.py`.
