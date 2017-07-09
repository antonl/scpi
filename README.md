scpi
====

A python sockets implementation of SCPI. The api follows pyvisa, but I couldn't get VISA to run 
on a mac.

## Usage

```python
import scpi; SCPI = scpi.SCPI;

host = '192.168.1.3'

a = SCPI(host, timeout=0.5)
a.ask('SYST:ERR?');
a.write('*RST'); a.write('*CLS');

a.close()
```

The output looks like

```
>> SYST:ERR? 
<< +0,"No error" 
```

There is a more complete example for an Agilent 33521B Waveform Generator in the python notebook.

## Notes

This is code is not currently used by me and probably doesn't work on Python 3,
but is probably portable. Pull requests welcome!


## License

Copyright (c) 2013, Anton Loukianov, BSD 3-clause

Thank you to the contributors:

2017-06-05 Christian Liebhardt: check for newline termination instead of waiting for
timeout when parsing responses

