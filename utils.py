# -*- coding: utf-8 -*-

import subprocess
import threading
import hashlib
import queue
import datetime
import time


def uniqify(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]



def hash_string(w):
    return hashlib.md5(w).hexdigest()


class AsynchronousFileReader(threading.Thread):
    '''
    Helper class to implement asynchronous reading of a file
    in a separate thread. Pushes read lines on a queue to
    be consumed in another thread.
    '''

    def __init__(self, fd, queue):
        threading.Thread.__init__(self)
        self._fd = fd
        self._queue = queue

    def run(self):
        '''The body of the tread: read lines and put them on the queue.'''
        for line in iter(self._fd.readline, ''):
            self._queue.put(line)

    def eof(self):
        '''Check whether there is no more content to expect.'''
        return not self.is_alive() and self._queue.empty()

def startsubprocess(command, process_events, sleep_time=0.1, debug=False):
    '''
    Example of how to consume standard output and standard error of
    a subprocess asynchronously without risk on deadlocking.
    '''
    # Launch the command as subprocess.
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Launch the asynchronous readers of the process' stdout and stderr.
    stdout_queue = queue.Queue()
    stdout_reader = AsynchronousFileReader(process.stdout, stdout_queue)
    stdout_reader.start()
    stderr_queue = queue.Queue()
    stderr_reader = AsynchronousFileReader(process.stderr, stderr_queue)
    stderr_reader.start()

    while not stdout_reader.eof() or not stderr_reader.eof():
        now = datetime.datetime.now()

        # STDERR
        def get_error_line():
            line = stderr_queue.get().decode('utf-8')
            if debug:
                print("STDERR: {}: {}".format(now,line[:-1]))
            return line
       
        while not stderr_queue.empty():
            get_error_line()

        # STDOUT
        def get_line():
            line = stdout_queue.get().decode('utf-8')
            if debug:
                print("STDOUT: {}: {}".format(now,line[:-1]))
            return line
       
        events = []
        while not stdout_queue.empty():
            line = get_line()
            events.append(line)
           
        if events:
            process_events(events)
        # Sleep a bit before asking the readers again.
        time.sleep(sleep_time)
    # Close down
    stdout_reader.join()
    stderr_reader.join()
    process.stdout.close()
    process.stderr.close()
