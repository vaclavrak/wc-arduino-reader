"""
 monitoring data from serial port

"""

from arduino_serial.Consumers.CodeConsumer import CodeConsumer
import numpy


class AirconCodeConsumer(CodeConsumer):
    codes = ['VP', 'HP', "AC", "MV", "NV", "MH", "NH"]
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
                value_list = self._queue[c]
                key = self.get_key(c)
                if c in ['NV', 'NH']:
                    m = numpy.min(value_list)
                else:
                    m = numpy.max(value_list)

                self.senders.send_data(key, m, c)

            # self.senders.flush()
            self._queue[c] = []
