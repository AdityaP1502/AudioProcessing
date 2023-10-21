import sys
import traceback

from threading import Thread
from time import sleep, time

class Test():
    def __init__(self, component, data, chunks, verbose=False):
        self._component = component
        self._n = len(data) // chunks
        self._i = 0
        self._t = Thread(target=self.run)
        self._exc = None
        self.chunk_size = chunks
        self.data = data
        self.verbose = verbose

    def start(self):
        self._t.start()
        if self.verbose:
            s = time()
            while self._t.is_alive():
                sys.stdout.write(f'\rProcessing.{" " * 20}frame {self._i}/{self._n}                      ')
                sleep(1)
                sys.stdout.write(f'\rProcessing..{" " * 19}frame {self._i}/{self._n}                     ')
                sleep(1)
                sys.stdout.write(f'\rProcessing...{" " * 18}frame {self._i}/{self._n}                    ')
                sleep(1)
            e = time()
            sys.stdout.write('\r                                                                    ')
            sys.stdout.write('\r')
            if not self._exc:
                print(f'Took {(e - s) * 1000} ms to complete')
                print(f'frame time {(e - s) * 1000 / self._n} ms')
        
    def join(self):
        self._t.join()
        if self._exc != None:
            traceback.print_exception(self._exc)
            raise self._exc
        
    def run(self):
        try:
            for i in range(self._n):
                self._component.filter()
                self.data[i * self.chunk_size : (i + 1) * self.chunk_size] = self.data[i * self.chunk_size : (i + 1) * self.chunk_size] + \
                self._component.get_output_node().get_frame()
                self._i += 1
        except Exception as e:
            self._exc = e
            return
            
            