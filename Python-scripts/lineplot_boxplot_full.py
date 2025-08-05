# -*- coding: utf-8 -*-

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sys

TECH_MAP = {
    "1": "AlBSF",
    "2": "monoPERC",
    "3": "NPERT",
    "4": "SHJ",
    "5": "TOPCon"
}

X_OPS = {
    "1": "exposure_condition",
    "2": "exposure_step"
}

Y_OPS = {
    "1":  "IV_Voc",
    "2":  "IV_Isc",
    "3":  "corrected_Jsc",
    "4":  "IV_Imp",
    "5":  "IV_Vmp",
    "6":  "IV_Pmp",
    "7":  "IV_FF",
    "8":  "corrected_Eff",
    "9":  "IV_Rs",
    "10": "IV_Rsh",
    "11": "Suns_Voc",
    "12": "Suns_FF",
    "13": "Suns_Eff",
    "14": "Suns_J01"
}

def choose_from_dict(d, prompt):
    """Utility to print options and read a valid key."""
    while True:
        print(prompt)
        for k, v in d.items():
            print(f"  {k}. {v}")
        choice = input("→ ").strip()
        if choice in d:
            return d[choice]
        print(f"Invalid choice: {choice!r}. Try again.\n")

def main():
    # 1) pick technology
    tech = choose_from_dict(
        TECH_MAP,
        "Select which cell‐technology you'd like to plot:"
    )
    # 2) pick x‐axis
    x_var = choose_from_dict(
        X_OPS,
        "\nSelect your x‑axis variable:"
    )
    # 3) pick y‐axis
    y_var = choose_from_dict(
        Y_OPS,
        "\nSelect your y‑axis variable:"
    )

    # 4) load data
    csv_path = "Master_File_COE_SIPS_CWRU_Accelerated_Screening_updated.csv"
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        print(f"ERROR: could not find {csv_path!r}")
        sys.exit(1)

    # filter by chosen technology
    sub = df[df["cell_technology"] == tech].copy()
    if sub.empty:
        print(f"No rows found for cell_technology == {tech!r}")
        sys.exit(1)

    # (TOPCon only) drop steps 8 and 9 due to data collection issues
    if tech == "TOPCon":
        sub = sub[(sub['exposure_step'] != 8) & (sub['exposure_step'] != 9)]
        if sub.empty:
            print(f"No data left for {tech}.")
            sys.exit(1)

    # drop rows where x or y is missing
    sub = sub.dropna(subset=[x_var, y_var])
    if sub.empty:
        print(f"No data left after dropping missing {x_var} or {y_var}.")
        sys.exit(1)

    sns.set(style="whitegrid")
    plt.figure(figsize=(10, 6))

    # choose plot type based on x_var
    if x_var == "exposure_condition":
        # categorical → boxplot
        sns.boxplot(
            data=sub,
            x=x_var,
            y=y_var,
            palette="muted"
        )
        plt.title(f"{y_var} distribution by {x_var} for {tech}")
        plt.xlabel("Exposure Condition")
        plt.ylabel(y_var)
    else:
        # numeric x → lineplot (mean ± sd)
        sns.lineplot(
            data=sub,
            x=x_var,
            y=y_var,
            estimator="mean",
            ci="sd",
            marker="o"
        )
        plt.title(f"{y_var} vs. {x_var} for {tech}")
        plt.xlabel(x_var)
        plt.ylabel(y_var)

    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
