"""
 read code and set proper behaviour

"""

from arduino_serial.Consumers.CodeConsumer import CodeConsumersList
from arduino_serial.Senders.BasicSender import SenderList
import time
from logging import getLogger

logger=getLogger("core")


class CodeProcessorException(Exception):
    pass


class CodeProcessor(object):
    _consumers = None
    _senders = None
    _serial = None
    _cn = 0
    _read = True

    def __init__(self):
        self._consumers = None
        self._senders = None
        self._cn = 0
        self._serial = None
        self._read = True

    def set_serial(self, serial):
        self._serial = serial
        return self

    @property
    def senders(self) -> SenderList:
        if self._senders is None:
            self._senders = SenderList()
        return self._senders

    @property
    def consumers(self) -> CodeConsumersList:
        if self._consumers is None:
            self._consumers = CodeConsumersList()
        return self._consumers

    @property
    def latest_timer(self):
        return self._cn

    def handle(self, code, value):
        """
        go thought all registered parsers and try to handle serial port
        :param code: two letter code
        :param value: the code value
        """
        for consumer in self.consumers:
            try:
                handeled = consumer.handle(code, value)
                if handeled is True:
                    break
            except Exception as e:
                logger.warning("Could not parse `{code}`: `{value}`; message: {message}".format(code=code, value=value, message=str(e)))

    def read_data(self, shell_we_read = None):
        """
            Read data from Serial port until is not ended
        :param shell_we_read:  callback function with bool response
        """
        ser = self._serial
        if ser.isOpen():
            ser.close()
            time.sleep(0.1)

        ser.open()

        now_timer = 0
        old_timer = 0
        while self._read:
            x=ser.readline().decode("utf-8")
            x=x.strip()
            time.sleep(0.1)
            if x.strip() == "":
                continue
            try:
                code, val = x.split(" ")
            except ValueError as e:
                logger.warning("Invalid value loaded: {row}, message: {message}".format(row=str(x), message=str(e)))
                continue
            self.handle(code, val)

            now_timer = int(time.strftime("%S"))

            if now_timer < old_timer:
                try:
                    self.consumers.flush_buffer()
                except Exception as e:
                    logger.warning("Flush failed message: {message}".format(message=str(e)))

            old_timer = now_timer

            if shell_we_read is not None:
                self._read = shell_we_read()
