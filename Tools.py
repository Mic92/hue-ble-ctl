from HueLight import HueLight

def check_connection(device: HueLight) -> None:
  if (not device.is_connected()):
      print("Reconnecting")
      device.connect()
