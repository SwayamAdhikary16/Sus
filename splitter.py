import pandas as pd

def save_to_excel(data_array, header_length, excel_file_name):
    # Splitting the data array based on the header length
    header = data_array[:header_length]
    rest_of_message = data_array[header_length:]
    
    # Creating a DataFrame to store the data
    df = pd.DataFrame({'Header': [header], 'Rest_of_Message': [rest_of_message]})
    
    # Writing the DataFrame to an Excel file
    df.to_excel(excel_file_name, index=False)
    print(f"Data saved to {excel_file_name}")

# Example usage:
data_array = ['1'] * 16 + ['Data', 'to', 'be', 'saved', 'in', 'Excel']
header_length = 16
excel_file_name = 'data.xlsx'

save_to_excel(data_array, header_length, excel_file_name)
