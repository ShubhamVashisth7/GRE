import time
import random
import numpy as np
from scipy.stats import uniform
from matplotlib import pyplot as plt

np.random.seed(1866)

def time_taken(start, end):
    hours, rem = divmod(end - start, 3600)
    minutes, seconds = divmod(rem, 60)
    return "{:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds)

def plot_cdf(data_sorted, dataset: str):
    fontsize = 14
    y = np.arange(1, len(data_sorted) + 1) / len(data_sorted)
    plt.plot(data_sorted, y, color='cornflowerblue', linewidth=1.5)
    plt.yticks(np.arange(0.0, 1.1, 0.25), ['0%', '25%', '50%', '75%', '100%'], fontsize=fontsize)
    plt.xticks(fontsize=fontsize)
    plt.ylim(top=1)
    plt.xlim(left=0.0) 
    plt.title(dataset, fontsize=fontsize+4)
    plt.xlabel('Key domain', fontsize=fontsize)
    plt.savefig(f'data_profiler/out/{dataset}_{len(data_sorted)}_cdf.png', dpi=300)

def generate_linear_cdf_keys(num_keys):
    min_val = 0
    max_val = 2**64-1 # as per 3.2 in https://www.vldb.org/pvldb/vol15/p3004-wongkham.pdf, 8-byte unsigned integer key

    cdf = uniform(loc=min_val, scale=max_val - min_val) # linear CDF

    print(f'generating {num_keys} keys')
    random_values = cdf.rvs(size=num_keys+10000)

    keys = set(np.sort(random_values).astype(np.uint64))
    num_keys_to_remove = len(keys) - num_keys

    keys_to_delete = random.sample(list(keys), num_keys_to_remove)
    for item in keys_to_delete:
        keys.remove(item)

    keys = np.sort(np.array(list(keys))) 
    print(f"generated {len(set(keys))} unique keys.\n sample keys: ", keys[:5])
    plot_cdf(data_sorted=keys, dataset='synthetic')

    keys = np.insert(keys, 0, len(keys))
    with open(f'/data/learned-index/synthetic_{len(keys)-1}', 'wb') as file:
        file.write(keys)

if __name__ == "__main__":
    start = time.time() 
    num_keys = 2*10**9
    generate_linear_cdf_keys(num_keys)
    print('done in ', time_taken(start=start, end=time.time()))
