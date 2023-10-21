import os.path
import traceback
import sys

from core.nodes import Nodes
from reverb.tapped_delay_line import TappedDelayLine
from testing.wav_file_io import save_wav, read_wav
from testing.test import Test

MIX = 0.75
CHUNK_SIZE = None
SAMPLE_RATE = None

if __name__ == "__main__":
    dst = os.path.join('temp', 'temp.wav')
    obj = read_wav(dst)

    data = obj["data"]
    CHUNK_SIZE = obj["chunks"]
    SAMPLE_RATE = obj["sample_rate"]

    input_node = Nodes(chunks=CHUNK_SIZE)
    input_node.set_frame_exceed_chunk_length((1 - MIX) * data)

    # initiate the component here
    ##############################
    
    ## Changes delay and gain parameter here, make sure they
    ## are the same length
    
    delay_line = TappedDelayLine(
        delay=[10, 30, 40, 50, 75, 100, 125, 250, 500],
        gain=[0.95, 0.85, 0.87, 0.7, 0.8, 0.82, 0.69, 0.69, 0.5],
        fs=SAMPLE_RATE,
        chunks=CHUNK_SIZE
    )
    ############################
    
    component = delay_line
    component.insert_input_node(input_node)
    
    test = Test(
        component=component,
        data=MIX * data,
        chunks=CHUNK_SIZE,
        verbose=True
    )

    try:
        test.start()
        test.join()
    except Exception as e:
        traceback.print_exception(e)
        print("Terminate testing without saving data")
        sys.exit(1)
    
    obj["data"] = test.data
    print('Saving data into ./temp/result.wav')
    save_wav(dst=os.path.join('temp', 'result.wav'), **obj)
    print('Done.')