import gatt
import struct
from threading import Barrier
from HueLight import HueLight

class HueDevice():
  def __init__(
        self,
        name,
        mac_address: str
    ) -> None:
        self.name = name
        self.mac_address = mac_address
        self.connection = None
        self.barrier = Barrier(2)
        self.manager = gatt.DeviceManager(adapter_name="hci0")

  def open_connection(self) -> None:
    self.connection = HueLight(mac_address=self.mac_address, manager=self.manager, barrier=self.barrier)