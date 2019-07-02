import conftest
import numpy as np
from asa_hmi_data_agent.hmipac.encoder import *
import asa_hmi_data_agent.hmipac as hd

data_ar = np.array(([1, 2, 3, 4, 5]), np.int8)

data_mt = np.array(([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]), np.int8).reshape(2, 5)

data_st = np.array(
    (
        [1, 2],
        [1, 2]
    ),
    dtype=[
        ('f0', np.uint8, (2,)),
        ('f1', np.uint16, (2,))
    ]
)


packet_ar = encodeArToPac(data_ar)
print("packet_ar is {}".format(packet_ar))

packet_mt = encodeMtToPac(data_mt)
print("packet_mt is {}".format(packet_mt))

packet_st = encodeStToPac(data_st)
print("packet_st is {}".format(packet_st))

pd = hd.Decoder()

for ch in packet_ar:
    pd.put(ch)
    if pd.state is hd.DecoderState.DONE:
        print(pd.get())

for ch in packet_mt:
    pd.put(ch)
    if pd.state is hd.DecoderState.DONE:
        print(pd.get())

for ch in packet_st:
    pd.put(ch)
    if pd.state is hd.DecoderState.DONE:
        print(pd.get())
