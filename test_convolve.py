from filter.fir import FIRFilter
from core.Nodes import Nodes

from scipy.signal import fftconvolve

import numpy as np

if __name__ == "__main__":
  fs = 48000
  L = 1024
  length = 1024 * 5
  
  xn = np.cos(2 * np.pi * 1000/fs * np.linspace(0, length - 1, length))
  # xn = np.pad(xn, (0, chunks), mode="constant")
  fir_filter = FIRFilter(fs=fs, chunks=L, wc=4000, n_order=101)
  
  # n_iter = len(xn) // chunks
  # out = []
  
  # input_node = Nodes(chunks=1024)
  # input_node.set_frame_exceed_chunk_length(xn)
  
  # fir_filter.insert_input_node(input_node)
  
  # for i in range(n_iter):
  #   fir_filter.filter()
  #   out.append(fir_filter.get_output_node().get_frame())   
    
  # out = np.concatenate(out)
  # print(out)
  
  # out_full = fftconvolve(xn[:length], fir_filter._taps, mode="full")
  # print(out_full)
  
  # hn = [1, -1, 1]
  # xn = [3, -1, 0, 3, 2, 0, 1, 2, 1]
  # length = len(xn)
  
  # L = 3
  # M = len(hn)
  
  xn = np.pad(xn, (0, L), mode="constant")
  # fir_filter = FIRFilter(fs=48000, chunks=L, hn=hn)
  
  input_node = Nodes(chunks=L)
  input_node.set_frame_exceed_chunk_length(xn)
  
  fir_filter.insert_input_node(input_node)
  n_iter = len(xn) // L

  out = []
  for i in range(n_iter):
    fir_filter.filter()
    out.append(fir_filter.get_output_node().get_frame())
    
  print(np.concatenate(out)[:length + fir_filter._num_taps - 1])
  
  print(fftconvolve(xn[:length], fir_filter._taps, mode="full"))