import conftest
import asa_hmi_data_agent.packet_handler as hd


b  = hd._CONST_HEADER_GET_AR
b += b'\x00'
b += b'\x00\x04'
b += b'\x01\x02\x03\x04'
b += bytes([sum(b'\x00\x04') + sum(b'\x01\x02\x03\x04')])

print('ssss')
de  = hd.DecoderHandler()
de.set_text(b)
res = de.get()
print(res)
print(de.get_text())


b  = hd._CONST_HEADER_GET_AR
de.add_text(b)
res = de.get()
print(res)
print(de.get_text())

b = b'\x00'
de.add_text(b)
res = de.get()
print(res)
print(de.get_text())

b = b'\x00\x04'
de.add_text(b)
res = de.get()
print(res)
print(de.get_text())

b = b'\x01\x02\x03\x04'
de.add_text(b)
res = de.get()
print(res)
print(de.get_text())

b = bytes([sum(b'\x00\x04') + sum(b'\x01\x02\x03\x04')])
de.add_text(b)
res = de.get()
print(res)
print(de.get_text())
