import os.path
from time import time

from testing.wav_file_io import read_wav, save_wav
from core.nodes import Nodes
from reverb.reverb_box import ReverbBox

if __name__ == "__main__":
    MIX = 0.55
    dst = os.path.join('temp', 'temp.wav')
    obj = read_wav(dst)
    data = obj["data"]
    CHUNK_SIZE = obj["chunks"]
    fs = obj["sample_rate"]

    # initiate the component here
    input_node = Nodes(chunks=CHUNK_SIZE)
    input_node.set_frame_exceed_chunk_length((1 - MIX) * data)

    # all_pass_component = AllPassFilter(delay=0.347, gain=0.7, fs=fs, chunks=chunk_size)
    # all_pass_component.insert_input_node(input_node)

    reverb_component = ReverbBox(delay=[
        347,
        113,
        37,
        1800,
        1610,
        2300,
        2400,
    ], gain=[
        0.7,
        0.7,
        0.7,
        0.75,
        0.8,
        0.71,
        0.698,
    ], fs=fs, chunks=CHUNK_SIZE, pre_delay=90)

    reverb_component.insert_input_node(input_node)

    component = reverb_component

    # Do Filter here
    N_ITER = len(data) // obj["chunks"]
    s = time()
    for i in range(N_ITER):
        component.filter()
        data[CHUNK_SIZE *
             i: CHUNK_SIZE *
             (i +
              1)] = (MIX *
                     data[CHUNK_SIZE *
                          i: CHUNK_SIZE *
                          (i +
                           1)] +
                     component.get_output_node().get_frame())

    # fir_filter = FIRFilter(fs=obj["sample_rate"], wc=8000, n_order=64)
    # data = fir_filter.filter(data)
    # data = np.int16(data / np.max(np.abs(data)) * 32767)
    # obj["data"] = data

    save_wav(dst=os.path.join('temp', 'result.wav'), **obj)

    e = time()
    print(f"Took {e - s} second")
