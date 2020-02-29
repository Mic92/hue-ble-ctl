# hue-ble-ctl
Control your Phillips Hue light bulb over Bluetooth.

## Features

(Just quickly hacked together in a few hours, more comes later)

- toggle light
- introspect GATT services and characteristics (for debugging)

## Requirements

- [gatt-python](https://github.com/getsenic/gatt-python)

## How to use

First connect to your hue light using blues `bluetoothctl`.
In this example the device mac address is `CD:43:95:FE:CE:D6`

```console
$ bluetootctl
[CHG] scan on 
[CHG] connect CD:43:95:FE:CE:D6
```

Then try to dump all bluetooth gatt attributes:

```console
$ python huectl.py introspect cd:43:95:fe:ce:d6
connect to cd:43:95:fe:ce:d6...
found brightness characteristics
found light characteristics
service: 9da2ddf1-0000-44d0-909c-3f3d3cb34a7b
  characteristic: 9da2ddf1-0001-44d0-909c-3f3d3cb34a7b: None
service: b8843add-0000-4aa1-8794-c3f462030bda
  characteristic: b8843add-0004-4aa1-8794-c3f462030bda:
  characteristic: b8843add-0003-4aa1-8794-c3f462030bda: None
  characteristic: b8843add-0002-4aa1-8794-c3f462030bda: None
  characteristic: b8843add-0001-4aa1-8794-c3f462030bda: bytearray(b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00')
service: 932c32bd-0000-47a2-835a-a8d455b859dd
  characteristic: 932c32bd-1005-47a2-835a-a8d455b859dd: bytearray(b'\x01\x01\x01\x02\x01\xfe')
  characteristic: 932c32bd-0007-47a2-835a-a8d455b859dd: bytearray(b'\x01\x01\x00\x02\x01\xfe')
  characteristic: 932c32bd-0006-47a2-835a-a8d455b859dd: None
  characteristic: 932c32bd-0003-47a2-835a-a8d455b859dd: bytearray(b'\xfe')
  characteristic: 932c32bd-0002-47a2-835a-a8d455b859dd:
  characteristic: 932c32bd-0001-47a2-835a-a8d455b859dd:
service: 0000fe0f-0000-1000-8000-00805f9b34fb
  characteristic: 97fe6561-a001-4f62-86e9-b71ee2da3d22: None
  characteristic: 97fe6561-2004-4f62-86e9-b71ee2da3d22: None
  characteristic: 97fe6561-2002-4f62-86e9-b71ee2da3d22: None
  characteristic: 97fe6561-2001-4f62-86e9-b71ee2da3d22:
  characteristic: 97fe6561-1001-4f62-86e9-b71ee2da3d22:
  characteristic: 97fe6561-0008-4f62-86e9-b71ee2da3d22: None
  characteristic: 97fe6561-0004-4f62-86e9-b71ee2da3d22: None
  characteristic: 97fe6561-0003-4f62-86e9-b71ee2da3d22: Shannan's bedroom
  characteristic: 97fe6561-0001-4f62-86e9-b71ee2da3d22: bytearray(b'\x01\x82\xe2\x06\x01\x88\x17\x00')
service: 0000180a-0000-1000-8000-00805f9b34fb
  characteristic: 00002a28-0000-1000-8000-00805f9b34fb: 1.65.9_hB3217DF4
  characteristic: 00002a24-0000-1000-8000-00805f9b34fb: LWA001
  characteristic: 00002a29-0000-1000-8000-00805f9b34fb: Philips
service: 00001801-0000-1000-8000-00805f9b34fb
  characteristic: 00002b29-0000-1000-8000-00805f9b34fb:
  characteristic: 00002b2a-0000-1000-8000-00805f9b34fb: bytearray(b'a\x10;o5\xdc\xcd\xb0{$\xa1\xc6\xd8\x04\xb3\xb1')
  characteristic: 00002a05-0000-1000-8000-00805f9b34fb: None
```

If all attributes show `None`, you might need to use the Phillips Hue App to
perform a firmware reset and reconnect first with your laptop instead of the
app.

If everything works as show here you can toggle the light as the following:

```console
$ python huectl.py toggle cd:43:95:fe:ce:d6
```
