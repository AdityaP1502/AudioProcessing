
import os.path
import traceback
import sys

# insert any dependencies here
###############################
# import numpy as np
# import matplotlib.pyplot as plt
###############################

from core.nodes import Nodes
from testing.wav_file_io import save_wav, read_wav
from testing.test import Test

# Import your component class implementation here
#####################################################
# from comp_package.comp_module import comp_class
#####################################################

# Change these parameter if needed
MIX = 0.75
CHUNK_SIZE = None # you can set it here or inside the scripts
SAMPLE_RATE = None 

if __name__ == "__main__":
    # Initiate your data here
    ###########################
    ###########################
    
    # insert your frame length into input nodes
        ## use input_node.set_frame_exceed_chunk_length if your data length
        ## is greater than the chunk size, else use set_frame
        
    ################################
    # input_node = Nodes(chunks=CHUNK_SIZE)
    # input_node.set_frame_exceed_chunk_length((1 - MIX) * data)
    ################################

    # initiate the component here
    ##############################
    # some_comp = comp_class(*arg, **kwargs)
    ##############################
    
    # assigned your component instance to component variable
    # component = some_comp
    # component.insert_input_node(input_node)
    
    # Create a test class and leave all the argument as is
    # test = Test(
    #     component=component,
    #     data=MIX * data,
    #     chunks=CHUNK_SIZE,
    #     verbose=True
    # )

    # Uncomment this
    try:
        test.start()
        test.join()
    except Exception as e:
        traceback.print_exception(e)
        print("Terminate testing without saving data")
        sys.exit(1)
    
    # Do something here with your filtered data
