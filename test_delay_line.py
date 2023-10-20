import os.path

from core.nodes import Nodes
from reverb.tapped_delay_line import TappedDelayLine
from testing.wav_file_io import save_wav, read_wav


if __name__ == "__main__":
    mix = 0.75
    dst = os.path.join('temp', 'temp.wav')
    obj = read_wav(dst)

    data = obj["data"]

    chunk_size = obj["chunks"]
    fs = obj["sample_rate"]

    # initiate the component here
    input_node = Nodes(chunks=chunk_size)
    input_node.set_frame_exceed_chunk_length((1 - mix) * data)

    delay_line = TappedDelayLine(
        delay=[10, 30, 40, 50, 75, 100, 125, 250, 500], 
        gain=[0.95, 0.85, 0.87, 0.7, 0.8, 0.82, 0.69, 0.69, 0.5],
        fs=fs,
        chunks=chunk_size
    )

    component = delay_line

    component.insert_input_node(input_node)
    n_iter = len(data) // obj["chunks"]

    for i in range(n_iter):
        component.filter()
        data[i * chunk_size : (i + 1) * chunk_size] = mix * data[i * chunk_size : (i + 1) * chunk_size] + \
            component.get_output_node().get_frame()
        
    save_wav(dst=os.path.join('temp', 'result.wav'), **obj)