import conftest
import numpy as np
import asa_hmi_data_agent.hmipac as hd

packet_ar = b'\xac\xac\xac\x00\n\x01\x00\x05\x00\x05\x01\x02\x03\x04\x05\x1A'
packet_mt = b'\xac\xac\xac\x00\x10\x02\x00\x02\x02\x00\x04\x01\x02\x03\x04\x14'
packet_st = b'\xac\xac\xac\x00\x0E\x03\x05ui8_5\x00\x05\x01\x02\x03\x04\x05\xC6'

pd = hd.Decoder()

for ch in packet_ar:
    pd.put(ch)
    print(pd.state)
    if pd.state is hd.DecoderState.DONE:
        print(pd.get())

for ch in packet_st:
    pd.put(ch)
    print(pd.state)
    if pd.state is hd.DecoderState.DONE:
        print(pd.get())

for ch in packet_mt:
    pd.put(ch)
    print(pd.state)
    if pd.state is hd.DecoderState.DONE:
        print(pd.get())
