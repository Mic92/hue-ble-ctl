import sys
import dbus
import gatt
import struct
from threading import Barrier

LIGHT_CHARACTERISTIC = "932c32bd-0002-47a2-835a-a8d455b859dd"
BRIGHTNESS_CHARACTERISTIC = "932c32bd-0003-47a2-835a-a8d455b859dd"
COLOR_CHARACTERISTIC = "932c32bd-0004-47a2-835a-a8d455b859dd"

class HueLight(gatt.Device):
    def __init__(
        self,
        mac_address: str,
        manager: gatt.DeviceManager,
        barrier: Barrier
    ) -> None:
        self.barrier = barrier
        self.mac_address = mac_address
        print(f"connect to {mac_address}...")
        super(HueLight, self).__init__(mac_address=self.mac_address, manager=manager)

    error = False;

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

    def set_color(self) -> None:
        foo = self.color.write_value(struct.pack("i", 1000))

    def set_brightness(self, val: int) -> None:
        self.brightness.write_value(struct.pack("B", val))

    def varyBrightness(self, val: int) -> None:
        next_brightness = self.getBrightness() + val
        if (next_brightness > 254) : next_brightness = 254
        elif (next_brightness < 1) : next_brightness = 1
        
        self.brightness.write_value(struct.pack("B", next_brightness ))



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

    def light_on(self) -> None:
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
        self.light_state.write_value(b"\x01")

    def light_off(self) -> None:
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
        self.light_state.write_value(b"\x00")

    def services_resolved(self) -> None:
        super().services_resolved()
        for s in self.services:
            for char in s.characteristics:
                val = char.read_value()
                if char.uuid == LIGHT_CHARACTERISTIC:
                    print("found light characteristics")
                    self.light_state = char
                elif char.uuid == BRIGHTNESS_CHARACTERISTIC:
                    print("found brightness characteristics : " + str(int(val[0])))
                    self.brightness = char
                elif char.uuid == COLOR_CHARACTERISTIC:
                    print("found color characteristics")
                    self.color = char
        self.barrier.wait()

    def getBrightness(self) -> int:
        return int(self.brightness.read_value()[0])

    def set_mac_address(self, mac_address) -> None:
        self.mac_address = mac_address

    def set_action(self, action) -> None:
        self.action = action
