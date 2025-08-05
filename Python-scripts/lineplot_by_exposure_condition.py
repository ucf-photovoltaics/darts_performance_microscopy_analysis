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
    "14": "Suns_J01",
    "15": "Suns_J02"
}

def choose_from_dict(d, prompt):
    while True:
        print(prompt)
        for k, v in d.items():
            print(f"  {k}. {v}")
        choice = input("→ ").strip()
        if choice in d:
            return d[choice]
        print(f"Invalid choice: {choice!r}. Try again.\n")

def main():
    # Step 1: Choose technology and Y-axis
    tech = choose_from_dict(TECH_MAP, "Select which cell technology to graph:")
    y_var = choose_from_dict(Y_OPS, "\nSelect the y-axis variable to plot (x-axis will be exposure_step):")

    # Step 2: Load data
    csv_path = "Master_File_COE_SIPS_CWRU_Accelerated_Screening_updated.csv"
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        print(f"ERROR: File '{csv_path}' not found.")
        sys.exit(1)

    # Step 3: Filter for selected tech and valid y-axis data
    df = df[df['cell_technology'] == tech].copy()
    df = df.dropna(subset=['exposure_step', y_var])

    if df.empty:
        print("No valid data available for selected filters.")
        sys.exit(1)

    # Step 4: Plot for each exposure condition
    for condition in ['acetic acid', 'DI water']:
        subset = df[df['exposure_condition'].str.lower() == condition.lower()]

        if subset.empty:
            print(f"Warning: No data found for '{condition}' under {tech}.")
            continue

        # Plotting
        sns.set(style="whitegrid")
        plt.figure(figsize=(10, 6))

        sns.lineplot(
            data=subset,
            x='exposure_step',
            y=y_var,
            estimator='mean',
            ci='sd',
            marker='o'
        )

        plt.title(f"{y_var} vs. Exposure Step ({condition}, {tech})")
        plt.xlabel("Exposure Step")
        plt.ylabel(y_var)
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    main()
