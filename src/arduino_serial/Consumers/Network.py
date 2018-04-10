"""
 network data from serial port

"""
from arduino_serial.Consumers.CodeConsumer import CodeConsumer


class NetworkCodeConsumer(CodeConsumer):
    # c = {"IP": net_ip, "GW": net_gw, "IN": net_internet, "VN": net_vpn}
    codes = ['IP', 'GW', 'IN', 'VN']
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
                key = self.get_key(c)
                value = self._queue[c][-1]
                if c in ['IN', 'VN']:
                    if value in ['0', 'fail']:
                        value = 0
                    if value in ['1', 'ok']:
                        value = 1
                self.senders.send_data(key, value, c)
        # self.data_processor.flush()
        self._queue[c] = []
