import numpy as np
import logging
log_format = "%(levelname)s | %(asctime)-15s | %(message)s"
logging.basicConfig(format=log_format, level=logging.DEBUG)
import RPi.GPIO as GPIO
import time
import spidev

def transmit(value):
    '''
    Transmit value over UDP
    '''
    pass

def main():
    # SPI
    min_angle = -90
    max_angle = 90
    min_val = 0
    max_val = 499
    bus = 0
    device = 0
    n = 10
    spi = spidev.SpiDev()
    spi.open(bus, device)
    
    # SPI settings
    spi.max_speed_hz = int(2.8e6)
    spi.mode = 0b11
    vref = 5.0
    
    try:
        while True:
            out = spi.readbytes(2)
            b1 = int(bin(out[0] << 4),2)
            b2 = int(bin(out[1])[:4],2)
            val = int(bin(b1 | b2),2)
            
            angle = np.deg2rad(val / max_val * (max_angle-min_angle) + min_angle)
            transmit(angle)
            print(f"val:\t{val}\t\tangle:\t{angle}")
    except KeyboardInterrupt:        
        spi.close()

if __name__ == "__main__":
    main()