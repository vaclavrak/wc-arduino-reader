"""
  serial code consumer

"""

from abc import ABCMeta, abstractmethod
from arduino_serial.Controller import Configurator
from arduino_serial.Senders.BasicSender import Sender, SenderList
import copy

class CodeConsumerException(Exception):
    pass


class CodeConsumer(object):
    __metaclass__ = ABCMeta
    _timer_callback = None
    _old_timer = 0
    _config = None
    _senders = None
    _k = {}

    def __init__(self):
        self._timer_callback = None
        self._old_timer = 0
        self._config = None
        self._senders = None
        self._k = {}

    def set_timer_reader(self, timer_callback):
        self._timer_callback = timer_callback
        self._config = None

    @property
    def senders(self) -> SenderList:
        if self._senders is None:
            self._senders = SenderList()
        return self._senders

    def register_sender(self, sender: Sender, kwargs):
        self.senders.append(sender.name, sender, kwargs)
        return self

    @property
    def get_now(self):
        if self._timer_callback is None:
            raise NotImplemented("timer_callback is not successfully initialized")

        return self._timer_callback()

    @abstractmethod
    def handle(self, code, value):
        raise NotImplementedError("handle")

    @abstractmethod
    def after_counter_reset(self):
        raise NotImplementedError("send_after_counter_reset")

    def set_config(self, cfg: Configurator):
        if not isinstance(cfg, Configurator):
            raise CodeConsumerException("Invalid config type")
        self._config = cfg
        return self

    @property
    def config(self) -> Configurator:
        return self._config

    def set_key_item(self, k):
        for k_item in k.keys():
            self._k[k_item] = k[k_item]

    def get_key(self, c):
        return copy.copy(self._k.get(c, {}))


class CodeConsumersList(object):
    _consumers = []

    def __init__(self):
        self._consumers = []

    def append(self, consumer_provider: CodeConsumer)-> object:
        for consumer in self._consumers:
            if type(consumer) == type(consumer_provider) :
                raise CodeConsumerException("Consumer {} already registered".format(consumer_provider))
        self._consumers.append(consumer_provider)
        return self

    def __iter__(self):
        for c in self._consumers:
            yield c

    def flush_buffer(self):
        for c in self._consumers:
            c.after_counter_reset()
            c.senders.flush()