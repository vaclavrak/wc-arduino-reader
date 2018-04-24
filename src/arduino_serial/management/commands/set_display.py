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
    help = 'set up display parameters'

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
        parser.add_argument('type', nargs='?')
        parser.add_argument('value', nargs='?')


    def handle(self, *args, **options):
        conf = options['config']
        config = Configurator().set_watch(False).read(conf)

        serial_com = config.get_kv("serial/device")
        serial_speed = config.get_kv("serial/speed", 9600)
        if options['type'] not in ['ip', 'gw', 'internet', 'vpn']:
            self.stdout.write(self.style.ERROR("Invalid option `type`, valid are `ip`"))
            return -1
        # self.stdout.write(self.style.SUCCESS("`type`: {}".format(options['type'])))

        ser = Serial(serial_com, serial_speed)
        if options['type'] == 'ip':
            ser.write(bytes('1/17/{}'.format(options['value']), 'utf-8'))
        if options['type'] == 'gw':
            ser.write(bytes('1/18/{}'.format(options['value']), 'utf-8'))
        if options['type'] == 'internet':
            ser.write(bytes('1/19/{}'.format(options['value']), 'utf-8'))
        if options['type'] == 'vpn':
            ser.write(bytes('1/20/{}'.format(options['value']), 'utf-8'))

        self.stdout.write(self.style.SUCCESS("`type`: {}, `value` {}".format(options['type'], options['value'])))
        ser.flush()
        time.sleep(1)
        ser.close()
