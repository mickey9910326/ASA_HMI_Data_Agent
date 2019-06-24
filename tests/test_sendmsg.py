import serial

def run():
    s1 = serial.Serial(port='COM2') # COM1 <---> COM2
    s2 = serial.Serial(port='COM4') # COM3 <---> COM4

    for i in range(10):
        s1.write(b's1-123\n')
        s2.write(b's2-456\n')

if __name__ == "__main__":
    run()
