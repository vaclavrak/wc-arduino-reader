from django.test import TransactionTestCase, mock
from wes_serial.CodeProvider import CodeProcessor
from wes_serial.Consumers.Dust import DustCodeConsumer
from wes_serial.Consumers.Monitor import MonitorCodeConsumer
from wes_serial.Consumers.Power import PowerCodeConsumer
from wes_serial.Consumers.Rain import RainCodeConsumer

class SerialTestCase(TransactionTestCase):

    def test_dust_sensor(self):
        class ser(object):
            read_stop = False
            _i = 0
            _lines = [
                "RA 0",
                "CN 35",
                "FS 333.3",
                "WD 0.333",
                "CN 41",
                "DI 111.1",
                "BO 11",
                "AI 6340",
                "RA 1",
                "CN 45",
                "DD 123.3",
                "RW 0.22",
                "VT 6340",
                "VT 0.055",
                "DV 123.55",
                "CN 0",
                "RA 1",
                "FS 333.3",
                "WD 0.444",
                "CN 41",
                "DI 222.2",
                "BO 12",
                "AI 6340",
                "CN 25",
                "DD 123.3",
                "RA 0",
                "RW 0.22",
                "VT 6340",
                "VT 0.055",
                "DV 123.55",
                "DV 1aaa",
                "CN 0"
            ]
            def isOpen(self):
                return False

            def open(self):
                return self

            def readline(self):
                ln = self._lines[self._i]
                if (self._i + 1) >= len(self._lines):
                    self._i = 0
                    self.read_stop = True
                else:
                    self._i += 1
                return ln

            def read_continue(self):
                return not ser.read_stop

        ser = ser()
        dcc = DustCodeConsumer()
        mcc = MonitorCodeConsumer()
        # pcc = PowerCodeConsumer()
        # rcc = RainCodeConsumer()

        cp = CodeProcessor(ser)
        cp.register(dcc)
        cp.register(mcc)
        # cp.register(pcc)
        # cp.register(rcc)

        with mock.patch('webcam.signals.dust_ventilator_speed.send', autospec=True) as mocked_handler:
            cp.read_data(ser.read_continue)
        self.assertEquals(mocked_handler.call_count, 2)  # standard django
