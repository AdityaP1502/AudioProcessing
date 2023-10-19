import matplotlib.pyplot as plt

import os.path
from time import time

from testing.wav_file_io import read_wav, save_wav
from core.nodes import Nodes
from compressor.compressor import Compressor

if __name__ == "__main__":
    dst = os.path.join('temp', 'temp.wav')
    obj = read_wav(dst)

    data = obj["data"]
    
    
    # plt.plot(data)
    # plt.show()
    
    chunk_size = obj["chunks"]
    fs = obj["sample_rate"]

    
    # initiate the component here
    input_node = Nodes(chunks=chunk_size)
    input_node.set_frame_exceed_chunk_length(data)
    
    compressor_component = Compressor(
        attack_time=10,
        release_time=1000,
        compressor_threshold=0.5,
        compressor_ratio=10,
        fs=fs,
        chunks=chunk_size
    )
    
    compressor_component.insert_input_node(input_node)
    
    component = compressor_component
    n_iter = len(data) // obj["chunks"]
    
    s = time()
    for i in range(n_iter):
        component.filter()
        data[i * chunk_size : (i + 1) * chunk_size] = component.get_output_node().get_frame()
        
    e = time()
    
    plt.plot(data)
    plt.show()
    
    save_wav(dst=os.path.join('temp', 'result.wav'), **obj)

    print(f"Took {e - s} second with average of {(e - s) / n_iter} seconds")