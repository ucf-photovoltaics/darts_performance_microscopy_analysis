"""
Creates a pairplot based on a selected cell technology and a selected list of variables.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

cell_tech = { #numbers have to be strings because input() takes in strings
    "1": "AlBSF",
    "2": "monoPERC",
    "3": "NPERT",
    "4": "SHJ",
    "5": "TOPCon"
}

#function to choose cell tech, based on Daniel's code
def choose_tech(input_dict):
    for key, val in input_dict.items():
        print(f"Option {key}: {val}")
    user_input = input("\nSelect a cell technology: ")
    if user_input in input_dict:
        return input_dict[user_input]
    print("Invalid input, please try again.")

def pairplots_by_tech(file_path):
    #step 0: load in data as DataFrame
    main_data = pd.read_csv(file_path)

    #step 1: choose tech
    tech = choose_tech(cell_tech)
    filtered_data = main_data[main_data["cell_technology"] == tech]
    filtered_data.dropna(axis=1, thresh=100, inplace=True) #dropping rows w/ ALL missing
    filtered_data.drop(columns=["area"], inplace=True) #drop unnecessary values (like constants)
    #step 1.5 (TOPCon only): drop steps 8 and 9 due to data collection issues
    if tech == "TOPCon":
        filtered_data = filtered_data[(filtered_data['exposure_step'] != 8) & (filtered_data['exposure_step'] != 9)]

    #step 2: form a pairplot
    #START here
    """
    Recommended divisions of columns to prevent generating HUGE pairplots (though checking across catagories is also crucial): 
    
    FUTURE IMPROVEMENT: Make this a dictionary. No need to loop through elements of array; pairplot function handles that already.
    
    IV =  ['IV_Voc', 'IV_Isc',
       'corrected_Jsc', 'IV_Imp', 'IV_Vmp', 'IV_Pmp', 'IV_FF', 'corrected_Eff',
       'IV_Rs', 'IV_Rsh']
    
    TLM = ['TLM_RSH', 'TLM_Rcf', 'TLM_LT', 'TLM_?c']
    
    Suns = ['Suns_Voc',
       'Suns_FF', 'Suns_Eff', 'Suns_J01'] (examine Suns_VOC histograms and Suns_Voc vs. Suns_J01)
    """
    
    IV =  ['IV_Voc', 'IV_Isc', 'corrected_Jsc', 'IV_Imp', 'IV_Vmp', 'IV_Pmp', 'IV_FF', 'corrected_Eff', 'IV_Rs', 'IV_Rsh']
    sns.pairplot(data=filtered_data, vars = IV)
    plt.suptitle(f'Pairplot for IV Data of {tech} Cell Technology', y=1.03, fontsize = 16) #manually change data examined
    plt.show()

if __name__ == "__main__":
    path = "Master_File_COE_SIPS_CWRU_Accelerated_Screening_updated.csv"
    pairplots_by_tech(path)   
