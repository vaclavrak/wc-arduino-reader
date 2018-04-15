"""
 read data from Serial and process it

 Settings objects
    WES_SERIAL_COM: string Serial  device, usual is /dev/ttyAMA0
    WES_SERIAL_SPEED: int Serial device read speed, usual is 9600

"""

import sys
from django.core.management.base import BaseCommand
from serial import Serial
from logging import getLogger
from arduino_serial.CodeProvider import CodeProcessor
from arduino_serial.Controller import  Configurator

logger=getLogger("arduino_serial")


class Command(BaseCommand):
    help = 'read data from Serial port and send it to to processor, press Ctrl+C to end it'

    _stop = False

    def __init__(self):
        super(Command, self).__init__()
        self._serial = None

    def exit_callback(self):
        self._stop = True
        logger.info("Going to stop")

    def add_arguments(self, parser):
        parser.add_argument('--cnf', '-c', dest='config',  default="/etc/webcam/serial-arduino.yml.example",
                            help='config file default is /etc/webcam/serial-arduino.yml.example')

    def handle(self, *args, **options):
        conf = options['config']
        config = Configurator().read(conf)

        serial_com = config.get_kv("serial/device")
        serial_speed = config.get_kv("serial/speed", 9600)

        ser = Serial(serial_com, serial_speed)

        cp = CodeProcessor()
        cp.set_serial(ser)

        for sender in config.get_kvs('targets'):
            sndr = sender.capitalize()
            __import__("arduino_serial.Senders.{cls}".format(cls=sndr))
            src_module = sys.modules["arduino_serial.Senders.{cls}".format(cls=sndr)]
            src_class = getattr(src_module, "{cls}Sender".format(cls=sndr))
            sender_cls = src_class().set_config(config).setup()
            cp.senders.append(sender_cls.name, sender_cls)

        for csm in config.get_kvs('consumers'):
            __import__("arduino_serial.Consumers.{cls}".format(cls=csm))
            src_module = sys.modules["arduino_serial.Consumers.{cls}".format(cls=csm)]
            src_class = getattr(src_module, "{cls}CodeConsumer".format(cls=csm))
            consumer_cls = src_class().set_config(config)
            for key_item in config.get_kvs("consumers/{}/keys".format(csm)):
                consumer_cls.set_key_item(key_item)
            for target_item in config.get_kvs("consumers/{}/targets".format(csm)):
                kwargs = {}
                for conf in config.get_kvs("consumers/{}/targets/{}".format(csm, target_item)):
                    value = config.get_kv("consumers/{}/targets/{}/{}".format(csm, target_item, conf))
                    kwargs[conf] = value
                (s, cnf) = cp.senders.get_by_name(target_item.capitalize())
                consumer_cls.register_sender(s, kwargs)
            cp.consumers.append(consumer_cls)

        cp.read_data()
