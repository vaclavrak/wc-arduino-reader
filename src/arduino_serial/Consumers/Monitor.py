"""
 monitoring data from serial port
    WD Watch Dog Counter
    WL Watch Dog Limit
    FS Fun Speed
    PS Power Switch
    PO Power TimeOut
    TI temperature in
    TO temperature out
"""

from arduino_serial.Consumers.CodeConsumer import CodeConsumer
import numpy


class MonitorCodeConsumer(CodeConsumer):
    codes = ['WD', 'FS', "PS", "PO", "TI", "TO", "WL", "RS", "ST", "HI", "OP", "RS"]
    _queue = {}

    def __init__(self):
        for c in self.codes:
            self._queue[c] = []

    def handle(self, code, value):
        if code in self.codes:
            sw = float(value)
            self._queue[code].append(sw)
            if code == 'WD':
                (r, cfg) = self.senders.get_by_name("Redis")
                r.send_data(self.get_key('WD'), sw, 'WD')
            return True

        return False

    def after_counter_reset(self):
        for c in self.codes:
            if len(self._queue[c]):
                value_list = self._queue[c]
                key = self.get_key(c)
                m = numpy.max(value_list)
                self.senders.send_data(key, m, c)
            # self.data_processor.flush()
            self._queue[c] = []
