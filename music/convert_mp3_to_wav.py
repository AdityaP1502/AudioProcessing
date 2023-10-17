import sys
import os.path
from pydub import AudioSegment

if __name__ == "__main__":
  if len(sys.argv) == 1:
    sys.exit(1)
    
  music_name = sys.argv[1]  
  
  src = os.path.join("music", music_name)
  dst = os.path.join("temp", "temp.wav")
  
  if not (os.path.isdir("temp")):
    os.mkdir("temp")
    
  
  sound = AudioSegment.from_mp3(src)
  sound.set_channels(1)
  sound = sound[10 * 1000:60 * 1000]
  sound.export(dst, format="wav")