"""
 Rain sensor switch from serial port

"""

from arduino_serial.Consumers.CodeConsumer import CodeConsumer


class RainCodeConsumer(CodeConsumer):

    codes = ['RA']
    _queue = {}
    _type = None

    def __init__(self):
        self._queue = {"RA": []}
        self._type = None

    def handle(self, code, value):
        if code in self.codes:
            sw = float(value)
            self._queue[code].append(sw)
            return True
        return False

    def after_counter_reset(self):
        for c in self.codes:
            if len(self._queue[c]):
                max_number = max(self._queue[c])
                key = self.get_key(c)

                if self.rain_type == 'collector_i2c':
                    self.senders.send_data(key, max_number, c)
                    key[-1] = 'precipitation'
                    self.senders.send_data(key, max_number*0.2794, c)
                if self.rain_type == 'collector_i2c':
                    self.senders.send_data(key, max_number, c)
            # self.senders.flush()
            self._queue[c] = []



    @property
    def rain_type(self):
        if self._type is None:
            self._type = self.config.get_kv("consumers/Rain/type")
        return self._type