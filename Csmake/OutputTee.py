
import subprocess
import sys
import tempfile
import threading

class OutputTee:
    def __init__(self):
        self.tempdir = tempfile.mkdtemp(prefix='csmake-temp')
        self.executing = True
        self.lock = threading.Lock()
        self.resultIds = {}
        self.writers = []
        self.threadsOpen = {}
        self.threads = []
        self._locals = threading.local()
        self.actual = sys.stdout

    def subsumeStream(self, stream):
        self.actual = stream

    def _consumerThread(self, myfd):
        while self.threadsOpen[myfd] and self.executing:
            buf = myfd.read(2048)
            self.actual.write(buf)
            self.actual.flush()
        try:
            myfd.close()
        except:
            pass

    def _init_thread_local(self):
        self._locals.filename = "{}/{}".format(self.tempdir, threading.currentThread().getName())
        self._locals.filebuf = open(self._locals.filename, 'wb',0)
        self._locals.readbuf = open(self._locals.filename, 'r+b')
        self._locals.currentResult = None
        self._locals.readerThread = threading.Thread(
            target=self._consumerThread,
            args=(self._locals.readbuf, ))
        with self.lock:
            self.threadsOpen[self._locals.readbuf] = True
            self.threads.append(self._locals.readerThread)
        #self._locals.readerThread.daemon = True
        self._locals.readerThread.start()

    def startResult(self, result, repeat=True):
        try:
            cr = self._locals.currentResult
            pos = self._locals.filebuf.tell()
            with self.lock:
                if cr is not None:
                    self.resultIds[cr].append(pos)
                self.resultIds[result] = [self._locals.filename, pos]
        except AttributeError:
            if not repeat:
                raise
            self._init_thread_local()
            self.startResult(result, False)

    def endResult(self, result):
        try:
            self.flush()
            with self.lock:
                self.resultIds[result].append(self._locals.filebuf.tell())
        except:
            pass

    def endAll(self):
        self.executing = False
        for f in self.writers:
            try:
                f.close()
            except:
                pass
        try:
            subprocess.call(['rm', '-rf', self.tempdir])
        except:
            pass
        for t in self.threads:
            try:
                t.join()
            except:
                pass

    def close(self):
        try:
            self.actual.flush()
        except:
            pass
        try:
            self.threadsOpen[self._locals.readbuf] = False
            self._locals.filebuf.close()
            self._locals.readbuf.close()
            with self.lock:
                f.remove(self._locals.filebuf)
        except:
            pass

    def flush(self):
        try:
            self._locals.filebuf.flush()
        except AttributeError:
            self._init_thread_local()

    def write(self, out, retry=True):
        try:
            return self._locals.filebuf.write(out)
        except AttributeError:
            if retry:
                self._init_thread_local()
                self.write(out, False)

    def fileno(self):
        return self._locals.filebuf.fileno()

    def getResult(self, result):
        with self.lock:
            location = self.resultIds[result]
            if len(location) >= 3:
                f = location[0]
                start = location[1]
                stop = location[-1]
            else:
                f, start = location
                stop = 9999999
        with open(f, 'r+b') as fp:
            fp.seek(start)
            #TODO: Ensure all is read
            return fp.read(stop-start)

    def __del__(self):
        self.endAll()

OutputTee = OutputTee()

