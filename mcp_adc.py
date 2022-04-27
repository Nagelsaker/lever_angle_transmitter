import numpy as np
import logging
log_format = "%(levelname)s | %(asctime)-15s | %(message)s"
logging.basicConfig(format=log_format, level=logging.DEBUG)
import RPi.GPIO as GPIO
import time
import socket
import spidev

def transmit(value, sock, ip, port, freq):
    '''
    Transmit value over UDP
    '''
    message = bytes(f"{value}", "utf-8")
    try:
        sock.sendto(message, (ip,port))
    except:
        pass
    time.sleep(1/freq)

def main():
    # Setup UDP connection
    DST_IP = "10.42.0.1"
    DST_PORT = 20000
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    freq = 10 # Hz
    
    # SPI
    min_angle = -96
    max_angle = 98
    min_val = 14 #50
    max_val = 114 #450
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
            b1 = int(bin(out[0] << 2),2)
            b2 = int(bin(out[1])[:4],2)
            val = int(bin(b1 | b2),2)
            
            angle = np.deg2rad((val - min_val)/ (max_val-min_val) * (max_angle-min_angle) + min_angle)
            transmit(angle, sock, DST_IP, DST_PORT, freq)
            print(f"bits:\t{bin(b1 | b2)}\tval:\t{val}\t\tangle:\t{np.rad2deg(angle)}")
    except KeyboardInterrupt:        
        spi.close()
        sock.close()

if __name__ == "__main__":
    main()