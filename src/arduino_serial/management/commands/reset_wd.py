"""

  Reset Arduino Watch Dog, prevention against freeze RPi
"""

from django.core.management.base import BaseCommand
from serial import Serial
from logging import getLogger
from arduino_serial.Controller import  Configurator
import time

logger=getLogger("arduino_serial")


class Command(BaseCommand):
    help = 'Set arduino WD to 0 via command `1/1/`'

    _stop = False

    def __init__(self):
        super(Command, self).__init__()
        self._serial = None

    def exit_callback(self):
        self._stop = True
        logger.info("Going to stop")

    def add_arguments(self, parser):
        parser.add_argument('--cnf', '-c', dest='config',  default="/etc/webcam/serial-arduino.yml",
                            help='config file default is /etc/webcam/serial-arduino.yml')

    def handle(self, *args, **options):
        conf = options['config']
        config = Configurator().read(conf)

        serial_com = config.get_kv("serial/device")
        serial_speed = config.get_kv("serial/speed", 9600)

        ser = Serial(serial_com, serial_speed)

        ser.write('1/1/')
        ser.flush()
        time.sleep(1)
        ser.close()
