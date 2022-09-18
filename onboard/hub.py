from pybricks.hubs import TechnicHub
from pybricks.tools import wait

hub = TechnicHub

while True:
    voltage = hub.battery.voltage()
    current = hub.battery.current()
    print('{} {}'.format(voltage / 1000, current / 1000))
    wait(1000)


