import sys
import gatt
import struct
from threading import Barrier

LIGHT_CHARACTERISTIC = "932c32bd-0002-47a2-835a-a8d455b859dd"
BRIGHTNESS_CHARACTERISTIC = "932c32bd-0003-47a2-835a-a8d455b859dd"
COLOR_CHARACTERISTIC = "932c32bd-0004-47a2-835a-a8d455b859dd"
PUBLIC_NAME = "97fe6561-0003-4f62-86e9-b71ee2da3d22"
ZIGBEE_MODELS = "00002a24-0000-1000-8000-00805f9b34fb"
FIRMWARE_VERSION = "00002a28-0000-1000-8000-00805f9b34fb"

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

    ###
    # Method that print all light characteristics
    # (Color, Brightness level ... etc)
    ###
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
                if (c.uuid == LIGHT_CHARACTERISTIC):
                  c.uuid = "LIGHT_CHARACTERISTIC"
                elif (c.uuid == BRIGHTNESS_CHARACTERISTIC):
                  c.uuid = "BRIGHTNESS_CHARACTERISTIC"
                elif (c.uuid == COLOR_CHARACTERISTIC):
                  c.uuid = "COLOR_CHARACTERISTIC"
                elif (c.uuid == PUBLIC_NAME):
                  c.uuid = "PUBLIC_NAME"
                elif (c.uuid == ZIGBEE_MODELS):
                  c.uuid = "ZIGBEE_MODELS"
                elif (c.uuid == FIRMWARE_VERSION):
                  c.uuid = "FIRMWARE_VERSION"
                print(f"  characteristic: {c.uuid}: {val}")

    ###
    # Change color properties
    ###
    def set_color(self) -> None:
        foo = self.color.write_value(struct.pack("i", 1000))

    ###
    # Change brightness properties by replacing it
    ###
    def set_brightness(self, val: int) -> None:
        self.brightness.write_value(struct.pack("B", val))

    ###
    # Change brightness properties by incrementing it
    ###
    def varyBrightness(self, val: int) -> None:
        next_brightness = self.getBrightness() + val
        if (next_brightness > 254) : next_brightness = 254
        elif (next_brightness < 1) : next_brightness = 1
        self.brightness.write_value(struct.pack("B", next_brightness ))

    ###
    # Toggle the lightbulb
    # ON if OFF, OFF if ON
    ###
    def toggle_light(self) -> None:
      if (hasattr(self, "light_state")):
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

    ###
    # Light on the lightbulb
    ###
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

    ###
    # Light off the lightbulb
    ###
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

    ###
    # Method called after connection is established
    ###
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

    ###
    # Return lightbulb brightness
    # 0 <= brightness <= 254
    ###
    def getBrightness(self) -> int:
        return int(self.brightness.read_value()[0])

    ###
    # Change the device mac address
    ###
    def set_mac_address(self, mac_address) -> None:
        self.mac_address = mac_address
