"""
 light sensor data from serial port
 codes
    LS Light Sensor
    UV Ultra Violent spectrum
"""
from arduino_serial.Consumers.CodeConsumer import CodeConsumer
import numpy


class LightCodeConsumer(CodeConsumer):
    codes = ['LS', 'UV']
    _queue = {}

    def __init__(self):
        for c in self.codes:
            self._queue[c] = []

    def handle(self, code, value):
        if code in self.codes:
            sw = float(value)
            self._queue[code].append(sw)
            return True
        return False

    def after_counter_reset(self):
        for c in self.codes:
            if len(self._queue[c]):
                key = self.get_key(c)

                if c == 'UV':
                    m = numpy.mean(self._queue[c])
                    self.senders.send_data(key, m, c)
                if c == 'LS':
                    m = numpy.mean(self._queue[c])
                    m_min = numpy.min(self._queue[c])
                    m_max = numpy.max(self._queue[c])
                    self.senders.send_data(key, m, c)
                    key[-1] = 'max'
                    self.senders.send_data(key, m_max, c)
                    key[-1] = 'min'
                    self.senders.send_data(key, m_min, c)
            # self.senders.flush()
            self._queue[c] = []
