"""

  Reset Arduino Watch Dog, prevention against freeze RPi
"""

from django.core.management.base import BaseCommand
from logging import getLogger
from arduino_serial.Controller import  Configurator
import redis
from socket import gethostname
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
        _host = config.get_kv("targets/redis/host", "localhost")
        _port = config.get_kv("targets/redis/port", 6379)
        _db = config.get_kv("targets/redis/database", 0)

        _redis = redis.StrictRedis(host=_host, port=_port, db=_db)
        wd_value = _redis.get("{}:watchdog:counter".format(gethostname()))
        wd_limit = _redis.get("{}:watchdog:limit".format(gethostname()))
        m = "The latest reported WD value is {}/{}".format(wd_value, wd_limit)
        logger.info(m)
        self.stdout.write(self.style.SUCCESS(m))

