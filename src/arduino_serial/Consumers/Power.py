"""
 power data from serial port
    DI	DC Current [A]
    BO  DC Battery out [V]
    U1	DC 24V
    U2	DC 15V
    U3	DC 5V
    RP  RPi power state
    CP  Camera power
    CV  camera voltage
"""
from arduino_serial.Consumers.CodeConsumer import CodeConsumer
import numpy


class PowerCodeConsumer(CodeConsumer):

    codes = ['DI', 'BO', 'AI', 'U1', 'U2', 'U3', "RP", "CP", "CV"]
    _queue = {}
    _min_bv4p = None
    _min4poweroff = None

    def __init__(self):
        self._min_bv4p = None
        self._min4poweroff = None
        for c in self.codes:
            self._queue[c] = []

    def handle(self, code, value):
        if code in self.codes:
            sw = float(value)
            self._queue[code].append(sw)
            return True
        return False

    @property
    def minimum_voltage_for_poweroff(self) -> float:
        if self._min4poweroff is None:
            self._min4poweroff = float(self.config.get_kv("consumers/Power/voltage/min4poweroff"))
        return self._min4poweroff

    @property
    def minimum_voltage_for_picture(self) -> float:
        if self._min_bv4p is None:
            self._min_bv4p = float(self.config.get_kv("consumers/Power/voltage/min4picture"))
        return self._min_bv4p

    def after_counter_reset(self):
        for c in self.codes:
            if len(self._queue[c]):
                key = self.get_key(c)
                if c == 'DI': # DC Current [A]
                    self.senders.send_data(key, numpy.mean(self._queue[c]), c)
                if c == "BO": # DC Battery out [V]
                    m = numpy.mean(self._queue[c])
                    self.senders.send_data(key, m, c)
                    key[-1] = 'power_on_ok'
                    if m > self.minimum_voltage_for_poweroff:
                        self.senders.send_data(key, 1, c)
                    else:
                        self.senders.send_data(key, 0, c)
                if c == "AI": # AC in [mA]
                    mean = numpy.mean(self._queue[c])
                    self.senders.send_data(key, mean, c)

                if c == "U1": # DC 24V
                    mean = numpy.mean(self._queue[c])
                    self.senders.send_data(key, mean, c)
                    # no external power supply
                    if mean < 5:
                        key[-1] = 'power_state'
                        self.senders.send_data(key, 0, c)
                    else:
                        self.senders.send_data(key, 1, c)

                if c == "U2": # DC 15V
                    mean = numpy.mean(self._queue[c])
                    self.senders.send_data(key, mean, c)
                    # no external power supply
                    key[-1] = 'make_picture_ok'
                    if mean > self.minimum_voltage_for_picture:
                        self.senders.send_data(key, 1, c)
                    else:
                        self.senders.send_data(key, 0, c)

                if c == "U3": # DC 5V
                    mean = numpy.mean(self._queue[c])
                    self.senders.send_data(key, mean, c)

                if c == "RP": # power RPi state
                    mean = numpy.mean(self._queue[c])
                    self.senders.send_data(key, mean, c)
                    changes = 0
                    state = self._queue[c][0]
                    for v in self._queue[c]:
                        if v != state:
                            changes = changes +1
                            state = v
                    key[-1] = 'state_rpi_changed'
                    self.senders.send_data(key, changes, c)

                if c == "CP": # Camera power state
                    mean = numpy.mean(self._queue[c])
                    self.senders.send_data(key, mean, c)
                    changes = 0
                    state = self._queue[c][0]
                    for v in self._queue[c]:
                        if v != state:
                            changes = changes +1
                            state = v
                    key[-1] = 'state_camera_changed'
                    self.senders.send_data(key, changes, c)

                if c == "CV": # Camera power state
                    mean = numpy.mean(self._queue[c])
                    self.senders.send_data(key, mean, c)

        # self.senders.flush()
        self._queue[c] = []
