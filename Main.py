#!/usr/bin/env python
import dbus
import gatt
from typing import List
from threading import Thread, Barrier
from Routes import configureRoutes

from HueLight import HueLight

# API imports
import flask  

manager = gatt.DeviceManager(adapter_name="hci0")
b = Barrier(2)
device = HueLight(mac_address="FD:4A:25:A6:62:80", manager=manager, barrier=b)
def run():
  device.connect()
  manager.run()
t = Thread(target=run, daemon=True)
t.start()
b.wait()

app = flask.Flask(__name__)
app.config["DEBUG"] = True

configureRoutes(app, device)

app.run(host='0.0.0.0')


# def main(param):
#     if len(sys.argv) < 3:
#         print(f"USAGE: {sys.argv[0]} toggle|switch_on|switch_off|brightness|introspect macaddress args...", file=sys.stderr)
#         sys.exit(1)

#     mac_address = sys.argv[2]
#     # FIXME adapter_name should be configurable
#     manager = gatt.DeviceManager(adapter_name="hci0")
#     # this is a bit of a hack. gatt blocks indefinitely
#     b = Barrier(2)
#     device = HueLight(sys.argv[1], sys.argv[3:], mac_address=mac_address, manager=manager, barrier=b)
#     def run():
#         device.connect()
#         manager.run()
#     t = Thread(target=run, daemon=True)
#     t.start()
#     b.wait()




# if __name__ == "__main__":
#     main()
