import unittest
from machine import I2C, Pin
from drivers.communication.i2c.si4703 import SI4703

class TestSI4703(unittest.TestCase):
    def setUp(self):
        self.i2c = I2C(0, scl=Pin(22), sda=Pin(21))
        self.si4703 = SI4703(self.i2c, reset_pin=23)

    def test_set_get_channel(self):
        test_freq = 95.8
        self.si4703.set_channel(test_freq)
        current_freq = self.si4703.get_channel()
        self.assertAlmostEqual(test_freq, current_freq, places=1)

if __name__ == '__main__':
    unittest.main()
