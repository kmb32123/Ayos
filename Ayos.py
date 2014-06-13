import RPi.GPIO as GPIO
import ephem
import time

from simpledaemon import Daemon
from RelayController import Relay
from datetime import datetime,tzinfo,timedelta
from threading import Timer

class AyosDaemon(Daemon):
    default_conf = '/etc/ayosdaemon.conf'
    section = 'ayos'
    


    Platteville = ephem.Observer()
    Sun = ephem.Sun()


    
    def run(self):
        relay = Relay(args.port)
        Platteville.lat=args.latitude
        Platteville.lon=args.longitude
        next_sunrise_date = Platteville.next_rising(Sun).datetime()
        next_sunset_date = Platteville.next_setting(Sun).datetime()
        
        if next_sunrise_date < next_sunset_date: #It is night time
            relay.turnOff()
            time.sleep(next_sunrise_date - datetime.utcnow())

        while True:
            relay.turnOn()
            
            next_sunset_date = Platteville.next_setting(Sun).datetime()

            time.sleep(next_sunset_date - datetime.utcnow())
            
            relay.turnOff()
            
            next_sunrise_date = Platteville.next_rising(Sun).datetime()

            time.sleep(next_sunrise_date - datetime.utcnow())
            
    def add_arguments(self):
        super(AyosDaemon, self).add_arguments()
        self.parser.add_argument('--lat', dest='latitude', required='True'
                            action='store', help='Lattitude of location' type=float)
        self.parser.add_argument('--long', dest='longitude', required='True'
                            action='store', help='Longitude of location' type=float)
        self.parser.add_argument('--port', dest='port', required='True'
                            action='store', help='GPIO port to control', type=int)                    
        self.parser.description = 'Run Ayos light controller for a specified location'

if __name__ == '__main__':
    AyosDaemon().main()
