import time
import numpy as np
from tqdm import tqdm
from matplotlib import pyplot as plt

np.random.seed(1866)

def time_taken(start, end):
    hours, rem = divmod(end - start, 3600)
    minutes, seconds = divmod(rem, 60)
    return "{:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds)

def plot_cdf(data_sorted, dataset: str, keys: int):
    fontsize = 14
    y = np.arange(1, len(data_sorted) + 1) / len(data_sorted)
    plt.plot(data_sorted, y, color='cornflowerblue', linewidth=1.5)
    plt.yticks(np.arange(0.0, 1.1, 0.25), ['0%', '25%', '50%', '75%', '100%'], fontsize=fontsize)
    plt.xticks(fontsize=fontsize)
    plt.ylim(top=1)
    plt.xlim(left=0.0) 
    plt.title(dataset, fontsize=fontsize+4)
    plt.xlabel('Key domain', fontsize=fontsize)
    plt.savefig(f'data_profiler/out/{dataset}_{keys}_cdf.png', dpi=300)

def generate(dataset: str, desired_key_num: int):
    with open(f'datasets/{dataset}', 'rb') as f:
        keys = np.sort(np.fromfile(f, dtype=np.uint64)[1:])

    keys_num = len(keys)
    print(f'# keys in {dataset}: {keys_num}\nsample keys: ', keys[:5])
    
    keys_to_add = desired_key_num - keys_num 
    print(f'adding additional {keys_to_add} keys')
    
    original_data_min = keys.min()
    original_data_max = keys.max()

    keys = set(keys)
    augmented_keys = set()
    with tqdm(total=keys_to_add, desc='Augmenting keys', unit='key', leave=False) as pbar:
        while len(augmented_keys) < keys_to_add:
            new_key = np.random.randint(low=original_data_min, high=original_data_max, dtype=np.uint64)
            if new_key not in keys and new_key not in augmented_keys:
                augmented_keys.add(new_key)
                pbar.update(1)
    
    print('done.')
    combined_keys = np.sort(np.array(list(keys)+list(augmented_keys)))
    print('# keys post augmentation: ', len(set(combined_keys)), '\nsample keys post augmentation: ', list(combined_keys)[:5])

    plot_cdf(data_sorted=combined_keys, dataset='big_' + dataset, keys=desired_key_num)

    combined_keys = np.insert(combined_keys, 0, len(combined_keys))
    with open(f'/data/learned-index/big_{dataset}_{desired_key_num}', 'wb') as file:
        file.write(combined_keys)

if __name__ == '__main__':
    start = time.time()
    generate(dataset ='libio', desired_key_num=800*10**6)
    print(f'done. in {time_taken(start=start, end=time.time())}')
