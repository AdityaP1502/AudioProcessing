import wave
import numpy as np

def read_wav(dst):
  chunk_size = 1024
  
  # Open the wave file
  with wave.open(dst, 'rb') as wav_file:
    # Get the number of frames and the sample width
    n_channels = wav_file.getnchannels()
    num_frames = wav_file.getnframes()
    sample_width = wav_file.getsampwidth()
    frame_rate = wav_file.getframerate()

    # Read the frames in chunks of 1024 samples
    data = []
    for i in range(0, num_frames, chunk_size):
        frames = wav_file.readframes(chunk_size)
        chunk = np.frombuffer(frames, dtype=np.int16)
        data.append(chunk)

  # Convert the data list into a NumPy array
  data = np.concatenate(data, axis=0)
  original_length = len(data)
  padding = np.zeros(len(data) % 1024)
  data = np.concatenate((data, padding), axis=0)
  
  return {"data": data, "n_channels" : n_channels, 
          "num_frames" : num_frames, "sample_width" : sample_width, 
          "sample_rate" : frame_rate, 
          "original_length" : original_length, "chunks" : chunk_size}
  
def save_wav(dst, **kwargs):
  # scaled = np.int16(kwargs["data"][:kwargs["original_length"]])
  scaled = np.int16(kwargs["data"][:kwargs["original_length"]] / np.max(np.abs(kwargs["data"][:kwargs["original_length"]])) * 32767)
  with wave.open(dst, 'w') as wav_file:
    wav_file.setnchannels(kwargs["n_channels"])
    wav_file.setsampwidth(kwargs["sample_width"])
    wav_file.setframerate(kwargs["sample_rate"])
    wav_file.setnframes(len(scaled))
    wav_file.writeframes(scaled.tobytes())