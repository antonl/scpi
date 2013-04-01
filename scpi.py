import socket
import select

class SCPI(object):
    
    _socket = None
    _chunk = 128 # buf size
    _vocal = False
    _timeout = 0.150 # Float timeout in secs
    
    def __init__(self, host, port=5025, timeout=None, vocal=True):
        try:
            self.host = host
            self._vocal = vocal
            
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            #self._socket.setblocking(0)

            if timeout is not None: 
                self._socket.settimeout(timeout)
                self._timeout = timeout
            self._socket.connect((host, port))
        except socket.error as e:
            if self._vocal: print 'SCPI>> connect({:s}:{:d}) failed: {:s}'.format(host, port, e)
            else: raise e
            
    def _write(self, cmd):
        if self._socket is None: raise IOError('disconnected')
        
        for i in xrange(0, len(cmd), self._chunk):
            if (i+self._chunk) > len(cmd): idx = slice(i, len(cmd))
            else: idx = slice(i, i+self._chunk)
            self._socket.sendall(cmd[idx])

        return cmd
    
    def write(self, cmd):
        try:
            return self._write(cmd + b'\n')
        except IOError as e:
            if self._vocal: print 'SCPI>> write({:s}) failed: {:s}'.format(cmd.strip(), e)
            else: raise e
    
    def _read(self):
        if self._socket is None: raise IOError('disconnected')
        
        buf = bytearray()
        
        data = True
        while data:
            r,w,e = select.select([self._socket], [], [self._socket], self._timeout)

            if r: # socket readable
                data = self._socket.recv(self._chunk)
                if data: 
                    buf += data
                else: # Socket readable but there is no data, disconnected.
                    data = False
                    self.close()
            else: # no data in socket
                data = False
        return buf
        
    def ask(self, cmd):
        try:
            cmd = self._write(cmd + b'\n')
            ans = self._read()
            if self._vocal:
                print '>> {:s} \n<< {:s} \n'.format(cmd.strip(), ans.strip()),
                if ans == '':
                    cmd = self._write('SYST:ERR?\n')
                    err = self._read()
                    print '>> {:s} \n<< {:s} \n'.format(cmd.strip(), err.strip()),    
            return str(ans.strip())
        except IOError as e: 
            if self._vocal: 
                print 'SCPI>> ask({:s}) failed: {:s}'.format(cmd.strip(), e)
            else: 
                raise e
    
    def close(self):
        self.__del__()
        
    def __del__(self):    
        if self._socket is not None: self._socket.close()
        self._socket = None

