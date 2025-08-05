import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math

cell_tech = {
    "1": "AlBSF",
    "2": "monoPERC",
    "3": "NPERT",
    "4": "SHJ",
    "5": "TOPCon"
}

def choose_tech(input_dict):
    for key, val in input_dict.items():
        print(f"Option {key}: {val}")
    user_input = input("\nSelect a cell technology: ")
    if user_input in input_dict:
        return input_dict[user_input]
    print("Invalid input, please try again.")
    return choose_tech(input_dict)

def grid_plot_vs_exposure_step(file_path):
    main_data = pd.read_csv(file_path)
  
    tech = choose_tech(cell_tech)
    filtered_data = main_data[main_data["cell_technology"] == tech].copy()
    filtered_data.dropna(axis=1, thresh=100, inplace=True)
    filtered_data.drop(columns=["area"], errors='ignore', inplace=True)    
    if tech == "TOPCon":
        filtered_data = filtered_data[(filtered_data['exposure_step'] != 8) & (filtered_data['exposure_step'] != 9)]

  # Define IV variables
  IV_vars = ['IV_Voc', 'IV_Isc', 'corrected_Jsc', 'IV_Imp', 'IV_Vmp', 'IV_Pmp', 
             'IV_FF', 'corrected_Eff', 'IV_Rs', 'IV_Rsh']
  # Filter only existing columns
  IV_vars = [var for var in IV_vars if var in filtered_data.columns]

  # Create a subplot grid
  n_cols = 3
  n_rows = math.ceil(len(IV_vars) / n_cols)

  sns.set(style="whitegrid")
  fig, axes = plt.subplots(n_rows, n_cols, figsize=(n_cols * 6, n_rows * 4), sharex=True)
  axes = axes.flatten()

   for i, var in enumerate(IV_vars):
        ax = axes[i]
        data = filtered_data[['exposure_step', var]].dropna()
        if data.empty:
            ax.set_visible(False)
            continue
        sns.lineplot(
            data=data,
            x='exposure_step',
            y=var,
            estimator='mean',
            ci='sd',
            marker='o',
            ax=ax
        )
        ax.set_title(f"{var} vs Exposure Step")
        ax.set_xlabel("Exposure Step")
        ax.set_ylabel(var)
        ax.tick_params(axis='x', rotation=45)
  # Hide any unused subplots
  for j in range(len(IV_vars), len(axes)):
        axes[j].set_visible(False)

  plt.suptitle(f"IV Metrics vs Exposure Step for {tech}", fontsize=16, y=1.02)
  plt.tight_layout()
  plt.show()

if __name__ == "__main__":
    path = "Master_File_COE_SIPS_CWRU_Accelerated_Screening_updated.csv"
    grid_plot_vs_exposure_step(path)
