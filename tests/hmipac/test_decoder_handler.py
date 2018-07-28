import conftest
import asa_hmi_data_agent.hmipac as hd

b = b'1234567\n'
b += b'-------'
b += hd.decoder._CONST_HEADER_GET_AR
b += b'\x00'
b += b'\x00\x04'
b += b'\x01\x02\x03\x04'
b += bytes([sum(b'\x00\x04') + sum(b'\x01\x02\x03\x04')])

print('ssss')
de  = hd.Decoder()
de.set_text(b)
print('-----------------------------------------------------------------------')
res = de.get()
print(res)
print(de.get_text())

print('-----------------------------------------------------------------------')
res = de.get()
print(res)
print(de.get_text())

print('-----------------------------------------------------------------------')
res = de.get()
print(res)
print(de.get_text())


print('-----------------------------------------------------------------------')
b  = hd.decoder._CONST_HEADER_GET_AR
de.add_text(b)
res = de.get()
print(res)
print(de.get_text())

print('-----------------------------------------------------------------------')
b = b'\x00'
de.add_text(b)
res = de.get()
print(res)
print(de.get_text())

print('-----------------------------------------------------------------------')
b = b'\x00\x04'
de.add_text(b)
res = de.get()
print(res)
print(de.get_text())

print('-----------------------------------------------------------------------')
b = b'\x01\x02\x03\x04'
de.add_text(b)
res = de.get()
print(res)
print(de.get_text())

print('-----------------------------------------------------------------------')
b = bytes([sum(b'\x00\x04') + sum(b'\x01\x02\x03\x04')])
de.add_text(b)
res = de.get()
print(res)
print(de.get_text())
