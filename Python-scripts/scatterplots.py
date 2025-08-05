"""
Generates scatterplots between two selected variables (or histograms if the same variable is chosen twice). 
Gives the option to graph a third variable (shown as a hue) to help determine extra influence.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import sys

cell_tech = { 
    "1": "AlBSF",
    "2": "monoPERC",
    "3": "NPERT",
    "4": "SHJ",
    "5": "TOPCon"
}

possible_vars = {
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
    "11": "TLM_RSH",
    "12": "TLM_Rcf",
    "13": "TLM_LT",
    "14": "TLM_?c",
    "15": "Suns_Voc",
    "16": "Suns_FF",
    "17": "Suns_Eff",
    "18": "Suns_J01"
}

hue_vars = {
    "0": None,
    "1": 'exposure_condition',
    "2": 'exposure_step',
    "3": 'measurement_step'
}


def user_choices(input_dict):
    for key, val in input_dict.items():
        print(f"Option {key}: {val}")
    user_input = input("\nMake a selection: ")
    if user_input in input_dict:
        return input_dict[user_input]
    print("Invalid input, please try again.")
    sys.exit(1)

def scatter_for_2_vars(file_path):
    #step 0: load in data as DataFrame
    main_data = pd.read_csv(file_path)
    main_data.drop(columns=["inventory", "area", "PL", "remark", "Suns_J02"], inplace=True) #drop unnecessary values (like constants)

    #step 1: choose tech
    tech = user_choices(cell_tech)
    filtered_data = main_data[main_data["cell_technology"] == tech]
    filtered_data.dropna(axis=1, thresh=100, inplace=True) #dropping rows w/ ALL missing

    #step 1.5 (TOPCon only): drop steps 8 and 9 due to data collection issues
    filtered_data = filtered_data[(filtered_data['exposure_step'] != 8) & (filtered_data['exposure_step'] != 9)]

    #step 2: choose axis variables AND verify if they're
    print("Please select a variable for the x-axis.\n")
    x_axis = user_choices(possible_vars)
    print("\nNow select a variable for the y-axis.\n")
    y_axis = user_choices(possible_vars)

    if not(x_axis in filtered_data.columns) or not(y_axis in filtered_data.columns):
        print(f"At least one of the selected columns is not currently present.")
        sys.exit(1)

    #step 3: set up relplots (histograms if same variable for x- and y-axis)
    if x_axis == y_axis: #histogram if same var chosen twice
        plt.hist(filtered_data[x_axis])
        plt.title(f"Histogram of {x_axis} Values for {tech} Technology", y = 1.02)
        plt.xlabel(f"{x_axis}")
        plt.ylabel("Value")
        plt.show()
    else:
        print("\nPlease select a 3rd variable (hue) to examine.\n")
        hue = user_choices(hue_vars)
        r2 = np.square(filtered_data[x_axis].corr(filtered_data[y_axis])) #calculates r^2 for linear regression
        
        sns.lmplot(x=x_axis, y=y_axis, data=filtered_data, ci=None, hue=hue) #hue is a 3rd CATEGORICAL variable, check  'exposure_condition' then 'exposure_step' then 'measurement_step'
        if hue is not None:
            plt.title(f"Scatterplot of {y_axis} vs. {x_axis} for {tech} Technology")
        else:
            plt.title(f"Scatterplot of {y_axis} vs. {x_axis} for {tech} Technology (r^2 = {r2})")
        plt.show()
        
            
if __name__ == "__main__":
    path = "Master_File_COE_SIPS_CWRU_Accelerated_Screening_updated.csv"
    scatter_for_2_vars(path)
