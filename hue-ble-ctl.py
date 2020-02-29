#!/usr/bin/env python
import math
import sys
import time

import dbus
import gatt

LIGHT_CHARACTERISTIC = "932c32bd-0002-47a2-835a-a8d455b859dd"
BRIGHTNESS_CHARACTERISTIC = "932c32bd-0003-47a2-835a-a8d455b859dd"
COLOR_CHARACTERISTIC = "932c32bd-0005-47a2-835a-a8d455b859dd"


class HueLight(gatt.Device):
    def __init__(
        self, action: str, mac_address: str, manager: gatt.DeviceManager
    ) -> None:
        self.action = action

        print(f"connect to {mac_address}...")
        super(HueLight, self).__init__(mac_address=mac_address, manager=manager)

    def introspect(self) -> None:
        for s in self.services:
            print(f"service: {s.uuid}")
            for c in s.characteristics:
                val = c.read_value()
                if val is not None:
                    ary = bytearray()
                    for i in range(len(val)):
                        ary.append(int(val[i]))
                    try:
                        val = ary.decode("utf-8")
                    except UnicodeDecodeError:
                        val = ary
                print(f"  characteristic: {c.uuid}: {val}")

    def toggle_light(self) -> None:
        val = self.light_state.read_value()
        if val is None:
            msg = (
                "Could not read characteristic. If that is your first pairing"
                "you may need to perform a firmware reset using the mobile phillips hue app and try connect again: "
                "https://www.reddit.com/r/Hue/comments/eq0y3y/philips_hue_bluetooth_developer_documentation/"
            )
            print(msg, file=sys.stderr)
            sys.exit(1)
        on = val[0] == 1
        self.light_state.write_value(b"\x00" if on else b"\x01")

    def services_resolved(self) -> None:
        super().services_resolved()
        for s in self.services:
            for char in s.characteristics:
                if char.uuid == LIGHT_CHARACTERISTIC:
                    print("found light characteristics")
                    self.light_state = char
                elif char.uuid == BRIGHTNESS_CHARACTERISTIC:
                    print("found brightness characteristics")
                    self.brightness = char
                elif char.uuid == COLOR_CHARACTERISTIC:
                    print("found color characteristics")
                    self.color = char
        if self.action == "toggle":
            self.toggle_light()
        elif self.action == "introspect":
            self.introspect()
        else:
            print(f"unknown action {self.action}")
            sys.exit(1)
        sys.exit(0)


# shannans_lamp = "cd:43:95:fe:ce:d6"
# joergs_lamp = "d4:bb:d8:6c:07:86"


def main():
    if len(sys.argv) < 3:
        print(f"USAGE: {sys.argv[0]} toggle|introspect macaddress", file=sys.stderr)
        sys.exit(1)

    mac_address = sys.argv[2]
    # FIXME adapter_name should be configurable
    manager = gatt.DeviceManager(adapter_name="hci0")
    device = HueLight(sys.argv[1], mac_address=mac_address, manager=manager)
    device.connect()

    manager.run()


if __name__ == "__main__":
    main()
