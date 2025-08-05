"""
Generates a heatmap for a selected cell technology to indicate relationships between quantitative variables.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

cell_tech = {
    "1": "AlBSF",
    "2": "monoPERC",
    "3": "NPERT",
    "4": "SHJ",
    "5": "TOPCon"
}

cell_type = {
    "1":"full cell",
    "2":"TLM"
}

#similar to pairplot function, but more general
def user_choices(dict):
    for key, val in dict.items():
        print(f"Option {key}: {val}")
    user_input = input("\nMake a selection: ")
    if user_input in dict:
        return dict[user_input]
    print("Invalid input, please try again.")    

def make_heatmaps(file_path):
    try:
        base_electrical = pd.read_csv(file_path)

        #Step 1: filter by cell technology
        print("Please choose a cell technology from the following list:\n")
        tech = user_choices(cell_tech)
        
        specific_electrical = base_electrical[base_electrical["cell_technology"] == tech] #Options: AlBSF, monoPERC, NPERT, SHJ, TOPCon
        specific_electrical.drop(columns=["inventory", "area", "PL", "remark", "Suns_J02"], inplace=True) #drop unnecessary values (like constants)

        #step 1.5 (TOPCon only): drop steps 8 and 9 due to data collection issues
        if tech == "TOPCon":
           specific_electrical = specific_electrical[(specific_electrical['exposure_step'] != 8) & (specific_electrical['exposure_step'] != 9)]

        #Step 2: narrow down further by cell type
        print("Please choose a cell type from the following list:\n")
        full_or_TLM = user_choices(cell_type)

        
        specific_by_cell_type = specific_electrical[specific_electrical["cell_type"] == full_or_TLM] #"full cell" or "TLM"
        specific_by_cell_type.dropna(axis=1, thresh=100, inplace=True) #dropping rows w/ ALL missing

        #plot heatmap for quantitative variables
        specific_num = specific_by_cell_type.select_dtypes("number")
        plt.figure(figsize=(16,8)) #fixed cramped number issue
        sns.heatmap(specific_num.corr(), annot=True) #recommendation: set annotations to False for full cell
        plt.title(f"{tech} Heatmap for {full_or_TLM}", y=1.03) 
        plt.show()

    #exceptions for errors
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

#main function
if __name__ == '__main__':
    path = "Master_File_COE_SIPS_CWRU_Accelerated_Screening_updated.csv"
    make_heatmaps(path)
