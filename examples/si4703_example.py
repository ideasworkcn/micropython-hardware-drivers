from machine import I2C, Pin
from drivers.communication.i2c.si4703 import SI4703

# Initialize I2C
i2c = I2C(0, scl=Pin(22), sda=Pin(21))

# Initialize SI4703
si4703 = SI4703(i2c, reset_pin=23)

# Set to 95.8 MHz
si4703.set_channel(95.8)

# Get current frequency
current_freq = si4703.get_channel()
print(f"Current frequency: {current_freq} MHz")

# You can add more functionality here, like scanning for stations
