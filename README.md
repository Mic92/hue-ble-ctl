# Hue-Bluetooth-Bridge
Control your Phillips Hue light bulb over Bluetooth.

## Features

Took Mic92 work to create an API than can control Philips Hue light.
[Mic92 GitHub](https://github.com/Mic92/hue-ble-ctl)

## Requirements

- [gatt-python](https://github.com/getsenic/gatt-python)

## How to use

1. First, if your light is already paired with hue App, you need to reset it.
2. Then pair your device with bluetoothctl, **and note mac address for next step** :

```console
$ bluetootctl
[CHG] scan on
[CHG] connect CD:43:95:FE:CE:D6
```

3. Update Config.py to add your devices name and mac address :

```python
DEVICES_DEFINITION: List = [
  {
    "name": "MainLight",
    "mac_address": "AA:AA:AA:AA:AA:AA"
  },
  {
    "name": "SecondLight",
    "mac_address": "BB:BB:BB:BB:BB:BB"
  }
]
```

4. Launch API

```console
python3 Main.py
```

## Available routes :

**Toggle**
----
  Toggle the lightbulb

* **URL**
  /api/v1/toggle

* **Method:**

  `GET`

*  **URL Params**

   **Required:**

   `device_name=[string]`

**Set Brightness**
----
  Set lightbulb brightness to value in uri
  Must be between 0 and 254.

* **URL**
  /api/v1/brightness/<int:value>

* **Method:**

  `GET`

*  **URL Params**

   **Required:**

   `device_name=[string]`


**Vary Brightness**
----
  Increase or decrease brightness of the lightbulb.

* **URL**
  /api/v1/brightness/vary/<string:value>

* **Method:**

  `GET`

*  **URL Params**

   **Required:**

   `device_name=[string]`

**Get Brightness**
----
  Return lightbulb brigthness level.

* **URL**
  /api/v1/brightness

* **Method:**

  `GET`

*  **URL Params**

   **Required:**

   `device_name=[string]`

**Get Active State**
----
  Return True if a connection is established between the lightbulb and your server.

* **URL**
  /api/v1/active

* **Method:**

  `GET`

*  **URL Params**

   **Required:**

   `device_name=[string]`

**Schedule light on**
----
  Schedule light on at a given time

* **URL**
  /api/v1/light_on_at

* **Method:**

  `GET`

*  **URL Params**

   **Required:**

   `device_name=[string]`
   `hour=[int]`
   `minute=[int]`
   `second=[int]`

**Schedule light on every day at**
----
  Schedule light on every day at a given time

* **URL**
  /api/v1/light_on_every_day_at

* **Method:**

  `GET`

*  **URL Params**

   **Required:**

   `device_name=[string]`
   `hour=[int]`
   `minute=[int]`
   `second=[int]`

**Schedule light on every day at**
----
  Schedule toggle light every x seconds

* **URL**
  /api/v1/light_on_every_day_at

* **Method:**

  `GET`

*  **URL Params**

   **Required:**

   `device_name=[string]`
   `second=[int]`

**Get jobs**
----
  Return a list of all saved jobs

* **URL**
  /api/v1/jobs

* **Method:**

  `GET`

*  **URL Params**

   **Optional:**

   `device_name=[string]`


**Get jobs**
----
  Delete a job from ID

* **URL**
  /api/v1/jobs

* **Method:**

  `DELETE`

*  **URL Params**

   **Required:**

   `device_name=[string]`

## Note :
My device is this one : [LWA009](https://zigbee.blakadder.com/Philips_LWA009.html)
It has no color so i didn't implemented this.
I didn't tested with more than one device. Tell me if there is any problem.

## Todo :

- [ ] Handle errors with [http response code](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes)

- [ ] Add tests

- [ ] Add Swagger documentation

- [ ] Change Set routes to POST instead of GET
