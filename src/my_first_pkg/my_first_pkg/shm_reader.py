# shm_reader.py
import time
import struct
from multiprocessing import shared_memory

def read_float64(buf, offset):
    return struct.unpack('d', buf[offset:offset+8])[0]

def main():
    shm = shared_memory.SharedMemory(name='vehicle_data')

    try:
        while True:
            speed = read_float64(shm.buf, 0)
            soc = read_float64(shm.buf, 8)
            posx = read_float64(shm.buf, 16)
            posy = read_float64(shm.buf, 24)

            print(f"Speed: {speed:.2f}, SOC: {soc:.2f}, X: {posx:.2f}, Y: {posy:.2f}")
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        shm.close()

if __name__ == '__main__':
    main()