import random
import numpy as np
from collections import Counter
import pandas as pd
import argparse

object_dict = {
    
}

def sample_obj(cat, n_sample, sample_size=2):
    sampled_objs = []
    cat_obj = cat.copy()
    while n_sample > 0 and len(cat) > 0:
        if len(cat_obj) < 2:
            cat_obj = cat.copy()
            print('refill the cat_obj')
        sampled_obj = random.sample(cat_obj, 2)
        sampled_objs.extend([sampled_obj])
        cat_obj = [obj for obj in cat_obj if obj not in sampled_obj]
        n_sample -= 1

    return sampled_objs, cat

# Create a table with three columns
def format_dataframe(df, columns=5):
    rows = (len(df) + columns - 1) // columns
    formatted_data = []
    for row in range(rows):
        formatted_row = []
        for col in range(columns):
            index = row + col * rows
            if index < len(df):
                formatted_row.append(f' {df.iloc[index, 0]}: {df.iloc[index, 1]} times      ')
            else:
                formatted_row.append('')
        formatted_data.append(formatted_row)
    return pd.DataFrame(formatted_data)

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Split the objects')
    parser.add_argument('--num_sample', type=int, default=153, help='Number of samples')
    parser.add_argument('--sample_size', type=int, default=2, help='Number of objects in each sample')
    args = parser.parse_args()
    num_sample = args.num_sample
    sample_size = args.sample_size
    
    cat1 = list(range(1, 112))
    cat2 = list(range(112, 188))
    cat3 = list(range(188, 201))
    total_obj = len(cat1) + len(cat2) + len(cat3)

    ratio1 = len(cat1) / total_obj
    ratio2 = len(cat2) / total_obj
    ratio3 = len(cat3) / total_obj
    sample1 = int(num_sample * ratio1)
    sample2 = int(num_sample * ratio2)
    sample3 = num_sample - (sample1 + sample2)
    print('sample1:', sample1)
    print('sample2:', sample2)
    print('sample3:', sample3)

    sampled_objs1, cat1 = sample_obj(cat1, sample1, sample_size)
    sampled_objs2, cat2 = sample_obj(cat2, sample2, sample_size)
    sampled_objs3, cat3 = sample_obj(cat3, sample3, sample_size)

    sampled_objs = sampled_objs1 + sampled_objs2 + sampled_objs3
    print('sampled_objs shape:', np.array(sampled_objs).shape)
    # Count occurrences of each object in sampled_objs
    sampled_objs = np.array(sampled_objs).flatten()
    counter = Counter(sampled_objs)

    # Convert the counter to a pandas DataFrame for better visualization
    df = pd.DataFrame(counter.items(), columns=['Object', 'Sampled Times'])
    df = df.sort_values(by='Object')
    
    formatted_df = format_dataframe(df, columns=10)
    print(formatted_df.to_string(index=False, header=False))