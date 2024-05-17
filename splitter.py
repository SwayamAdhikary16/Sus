import pandas as pd
import random

def generate_random_binary_string(length):
    return ''.join(random.choice(['0', '1']) for _ in range(length))


def sem_split(data_array, param_filename, output_filename):
    param_df = pd.read_excel(param_filename)
    params = param_df.to_dict(orient='list')
    
    params = {k: int(v[0]) for k, v in params.items()}
    
    data_dict = {}
    start_idx = 0
    for col_name, col_length in params.items():
        end_idx = start_idx + col_length
        data_dict[col_name] = ''.join(map(str, data_array[start_idx:end_idx]))
        start_idx = end_idx
    
    df = pd.DataFrame([data_dict])
    
    df.to_excel(output_filename, index=False)
    print(f"Data saved to {output_filename}")


data_array = ['1'] * 16 + [str(i) for i in generate_random_binary_string(54)] 
param_filename = 'sem.xlsx'  
output_filename = 'data.xlsx'

sem_split(data_array, param_filename, output_filename)
    
