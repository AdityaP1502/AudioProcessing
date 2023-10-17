import os.path

from testing.wav_file_io import *
from core.Nodes import Nodes
from Reverb.AllPassFilter import AllPassFilter
from Reverb.ReverbBox import ReverbBox
from filter.fir import FIRFilter

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
    0., 
    0.35, 
    0.045,
    0.025,  
  ], fs=fs, chunks=chunk_size)
  

  reverb_component.insert_input_node(input_node)
  
  component = reverb_component
  
  # Do Filter here
  n_iter = len(data) // obj["chunks"]
  for i in range(n_iter):
    component.filter()
    data[chunk_size * i : chunk_size * (i + 1)] = 0.5 * (mix * data[chunk_size * i : chunk_size * (i + 1)] + component.get_output_node().get_frame())
  
  # fir_filter = FIRFilter(fs=obj["sample_rate"], wc=8000, n_order=64)
  # data = fir_filter.filter(data)
  # data = np.int16(data / np.max(np.abs(data)) * 32767)
  # obj["data"] = data
  
  save_wav(dst=os.path.join('temp', 'result.wav'), **obj)  
  
  
  