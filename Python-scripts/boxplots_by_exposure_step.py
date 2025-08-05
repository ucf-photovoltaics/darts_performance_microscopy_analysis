import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def create_box_plots(file_path):
   
    try:
        # Load the dataset from the specified CSV file
        data = pd.read_csv(file_path)

        # --- Filter data for type of cell cell ---
        # This arguement can be  changed depending on the type of cell 
        cell_data = data[data['cell_technology'] == 'monoPERC'].copy() 

        if cell_data.empty:
            print("No data found for this cell technology.")
            return

        # Get the unique exposure conditions for desired cell type
        exposure_conditions = cell_data['exposure_condition'].unique()

        # Define the specific conditions we want to plot
        conditions_to_plot = ['acetic acid', 'DI water']

        # Create a separate plot for each exposure condition 
        for condition in conditions_to_plot:
            if condition not in exposure_conditions:
                print(f"Warning: Exposure condition '{condition}' not found in the data for this cells.")
                continue

            # Filter the data for the current exposure condition
            condition_data = cell_data[cell_data['exposure_condition'] == condition]

            if condition_data.empty:
                print(f"No data available for condition: {condition}")
                continue

            # --- Create the Box Plot ---
            plt.style.use('seaborn-v0_8-whitegrid') 
            fig, ax = plt.subplots(figsize=(12, 8))

            # Create the boxplot using seaborn, setting x and y to desired metrics
            sns.boxplot(
                x='exposure_step',
                y='corrected_Eff',
                data=condition_data,
                ax=ax,
                palette='viridis' 
            )

            # --- Customize the Plot ---
            # Set the title and labels for cell type
            ax.set_title(
                f'Corrected Efficiency of monoPERC Cells under {condition} Exposure',
                fontsize=16,
                fontweight='bold'
            )
            ax.set_xlabel('Exposure Step', fontsize=12)
            ax.set_ylabel('Corrected Efficiency (%)', fontsize=12)

            # Improve readability of x-axis labels if they are long
            plt.xticks( ha='right')
            
            # Add a grid for better readability
            ax.yaxis.grid(True, linestyle='--', which='major', color='grey', alpha=.5)

            # Using a tight layout
            plt.tight_layout()

            # Display the plot
            plt.show()

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == '__main__':
    # --- Specify the path to your data file ---
    # Make sure this file is in the same directory as the script, or provide the full path.
    csv_file_path = 'Master_File_COE_SIPS_CWRU_Accelerated_Screening_updated.csv'
    create_box_plots(csv_file_path)
