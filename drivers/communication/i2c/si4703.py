from machine import I2C, Pin
import utime

class SI4703:
    I2C_ADDR = 0x10

    # Register addresses
    REG_DEVICEID = 0x00
    REG_CHIPID = 0x01
    REG_POWERCFG = 0x02
    REG_CHANNEL = 0x03
    REG_SYSCONFIG1 = 0x04
    REG_SYSCONFIG2 = 0x05
    REG_STATUSRSSI = 0x0A
    REG_READCHAN = 0x0B

    def __init__(self, i2c, reset_pin):
        self.i2c = i2c
        self.reset_pin = Pin(reset_pin, Pin.OUT)
        self.reset()
        self.init_device()

    def reset(self):
        self.reset_pin.value(0)
        utime.sleep_ms(100)
        self.reset_pin.value(1)
        utime.sleep_ms(100)

    def init_device(self):
        # Power up the device
        self.write_reg(self.REG_POWERCFG, 0x4001)
        utime.sleep_ms(110)  # Wait for oscillator to stabilize

        # Configure for maximum performance
        self.write_reg(self.REG_SYSCONFIG2, 0x0100)

    def set_channel(self, freq):
        # Frequency in MHz, e.g. 95.8
        channel = int((freq - 87.5) / 0.1)
        self.write_reg(self.REG_CHANNEL, channel << 6)

    def get_channel(self):
        readchan = self.read_reg(self.REG_READCHAN)
        freq = (readchan & 0x03FF) * 0.1 + 87.5
        return freq

    def read_reg(self, reg):
        self.i2c.writeto(self.I2C_ADDR, bytes([reg]))
        data = self.i2c.readfrom(self.I2C_ADDR, 2)
        return (data[0] << 8) | data[1]

    def write_reg(self, reg, value):
        self.i2c.writeto(self.I2C_ADDR, bytes([reg, (value >> 8) & 0xFF, value & 0xFF]))

# Example usage:
# i2c = I2C(0, scl=Pin(22), sda=Pin(21))
# si4703 = SI4703(i2c, reset_pin=23)
# si4703.set_channel(95.8)  # Set to 95.8 MHz
# current_freq = si4703.get_channel()
# print(f"Current frequency: {current_freq} MHz")
