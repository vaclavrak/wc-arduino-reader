"""
 Date time data about RTC and arduino restart data from serial port

"""
from arduino_serial.Consumers.CodeConsumer import CodeConsumer


class DateTimeCodeConsumer(CodeConsumer):
    codes = ['DT', 'TM', 'RT', 'RD']
    _queue = {}

    def __init__(self):
        for c in self.codes:
            self._queue[c] = []

    def handle(self, code, value):
        if code in self.codes:
            self._queue[code] = [value, ]
            return True
        return False

    def after_counter_reset(self):
        for c in self.codes:
            if len(self._queue[c]):
                m = self._queue[c][-1]
                key = self.get_key(c)
                self.senders.send_data(key, m, c)
        # self.data_processor.flush()
        self._queue[c] = []
