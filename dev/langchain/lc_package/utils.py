import pickle
import gzip

def save_memory(path, memory):
    with gzip.open(path + '/memory.pickle', 'wb') as f:
        pickle.dump(memory, f)

def load_memory(path):
    with gzip.open(path + '/memory.pickle', 'rb') as f:
        data = pickle.load(f)
    return data