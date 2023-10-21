import os.path
import traceback
import sys

from core.nodes import Nodes
from core.cascaded_box import CascadedBox

from box.arithmetic import Adder
from reverb.reverb_box import ReverbBox
from reverb.tapped_delay_line import TappedDelayLine

from testing.wav_file_io import save_wav, read_wav
from testing.test import Test

MIX = 0.75
CHUNK_SIZE=None
SAMPLE_RATE=None

if __name__ == "__main__":
    dst = os.path.join('temp', 'temp.wav')
    obj = read_wav(dst)

    data = obj["data"]
    
    CHUNK_SIZE = obj["chunks"]
    SAMPLE_RATE = obj["sample_rate"]
    
    # initiate the component here
    input_node = Nodes(chunks=CHUNK_SIZE)
    input_node.set_frame_exceed_chunk_length((1 - MIX) * data)
    
    delay_line = TappedDelayLine(
        delay=[10, 30, 40, 50, 75, 100, 125, 250, 500], 
        gain=[0.95, 0.85, 0.87, 0.7, 0.8, 0.82, 0.69, 0.69, 0.5],
        fs=SAMPLE_RATE,
        chunks=CHUNK_SIZE
    )
    
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
    ], fs=SAMPLE_RATE, chunks=CHUNK_SIZE)

    adder = Adder(fs=SAMPLE_RATE, chunks=CHUNK_SIZE)

    reverb_component.insert_input_node(delay_line.get_tap(-2))

    adder.insert_input_node(delay_line.get_output_node())
    adder.insert_input_node(reverb_component.get_output_node())

    component = CascadedBox.create_system_from_components((0, delay_line), (1, reverb_component), (2, adder))
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