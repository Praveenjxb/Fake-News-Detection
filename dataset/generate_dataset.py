"""
generate_dataset.py

Generates a small SYNTHETIC dataset (Fake.csv / True.csv) so the project
can be trained and demoed end-to-end without needing to download a large
external dataset.

NOTE FOR THE STUDENT:
For a real submission, it is strongly recommended to replace these files
with a genuine dataset (e.g. the commonly used Kaggle "Fake and Real News
Dataset" - search "Fake.csv True.csv Kaggle"). Just keep the same column
name ("text") and this script/training pipeline will work unchanged.
"""

import csv
import random

random.seed(42)

# --- Building blocks for FAKE-style (sensational / unverified) news ---
fake_subjects = [
    "Scientists", "Doctors", "A secret government report", "Local officials",
    "An anonymous whistleblower", "A viral video", "Experts", "A leaked memo",
    "A famous celebrity", "An unnamed source", "A shocking new study",
    "Internet users", "A popular blogger", "A conspiracy theorist",
]
fake_claims = [
    "reveal that drinking hot water cures cancer overnight",
    "confirm that the moon landing was completely faked",
    "warn that 5G towers are secretly controlling people's minds",
    "claim that a miracle pill melts fat in just three days",
    "expose a hidden plan to replace all money with a secret currency",
    "prove that vaccines contain microchips for tracking citizens",
    "announce that aliens have already taken over a major city",
    "insist that the earth is actually flat and NASA is hiding it",
    "reveal a secret cure that doctors don't want you to know about",
    "claim a celebrity faked their own death for publicity",
    "warn that eating this common fruit instantly boosts IQ by 50 points",
    "state that a new law will secretly ban all internet access next week",
    "allege that a politician is actually a robot controlled remotely",
    "claim breaking news that the stock market will collapse tomorrow at noon",
]
fake_tails = [
    "Share this before it gets deleted!",
    "Mainstream media refuses to report this.",
    "You won't believe what happens next.",
    "This is being hidden from the public.",
    "Wake up, people, before it's too late!",
    "No official confirmation exists, but sources insist it's true.",
    "The video has already been viewed millions of times.",
    "",
]

# --- Building blocks for REAL-style (measured / attributed / factual) news ---
real_subjects = [
    "The Reserve Bank of India", "The Ministry of Health", "Researchers at a state university",
    "The city municipal corporation", "The state government", "A parliamentary committee",
    "The World Health Organization", "The company's quarterly earnings report",
    "The election commission", "Local police", "The finance ministry",
    "The central government", "A peer-reviewed study published in a medical journal",
    "The state education department",
]
real_claims = [
    "announced a 0.25 percent increase in the benchmark interest rate on Wednesday",
    "released updated guidelines for seasonal vaccination campaigns",
    "published findings on regional rainfall patterns over the last decade",
    "approved a new budget allocation for infrastructure repair projects",
    "confirmed that voter turnout increased by four percent compared to the previous election",
    "reported a decline in quarterly profits due to rising raw material costs",
    "issued a statement clarifying new traffic regulations effective next month",
    "announced revised examination dates for the upcoming academic term",
    "conducted an investigation into a reported break-in near the city center",
    "signed a trade agreement aimed at boosting regional exports",
    "released a report outlining measures to improve urban water supply",
    "confirmed that construction of the new metro line is on schedule",
    "outlined new safety protocols for public transportation services",
    "presented data showing a gradual decrease in unemployment over the past year",
]
real_tails = [
    "Officials said further details will be shared in the coming weeks.",
    "The announcement was made during a press briefing on Wednesday.",
    "The full report is available on the department's official website.",
    "Authorities confirmed the figures are subject to final review.",
    "The decision follows months of consultation with stakeholders.",
    "A spokesperson said the changes will take effect from next quarter.",
    "The findings were published in the official gazette this week.",
    "",
]


def make_rows(subjects, claims, tails, n):
    rows = []
    for _ in range(n):
        text = f"{random.choice(subjects)} {random.choice(claims)}. {random.choice(tails)}".strip()
        rows.append(text)
    return rows


def main():
    fake_rows = make_rows(fake_subjects, fake_claims, fake_tails, 250)
    real_rows = make_rows(real_subjects, real_claims, real_tails, 250)

    with open("Fake.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["text"])
        for row in fake_rows:
            writer.writerow([row])

    with open("True.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["text"])
        for row in real_rows:
            writer.writerow([row])

    print(f"Wrote {len(fake_rows)} rows to Fake.csv")
    print(f"Wrote {len(real_rows)} rows to True.csv")


if __name__ == "__main__":
    main()
