import conftest
import numpy as np
import asa_hmi_data_agent.packet_handler as hd

h      = hd._CONST_HEADER_GET_ST
fs     = b'ui8x5'
sbyte  = len(fs)
data   = b'\x01\x02\x03\x04\x05'
dbyte  = sbyte + len(data)+1
sbyte  = bytes([len(fs)])
dbyte  = bytes([dbyte>>8, dbyte&0xFF])
chkSum = bytes([sum(dbyte + sbyte + fs + data)&0xFF])

packet = h + dbyte + sbyte + fs + data + chkSum
print(packet)

de = hd.DecoderHandler()
de.set_text(packet)
print('-----------------------------------------------------------------------')
res = de.get()
print(res)
print(de.get_text())
print('-----------------------------------------------------------------------')
res = de.get()
print(res)
print(de.get_text())

dt = np.int8
# dt = dt.newbyteorder('>')
res = np.frombuffer(data, dtype=dt)
print(res)
print(type(res))
