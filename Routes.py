from typing import List
from Tools import check_connection
from threading import Thread
from flask import request
from flask_apscheduler import APScheduler
import flask
from Tools import light_on_bulb_at, light_on_bulb_every_day_at, valide_time, toggle_light_every, save_job


# Const
from Config import API_START_URI

DEVICE_NOT_KNOWN = "Device name not known"
NEED_TO_SPECIFY_DEVICE_NAME = "You need to specify device name : ?device_name=..."
INVALID_HOUR = "Provided time is invalid"
DEVICE_SCHEDULE_OK = "Device schedule was setup"

def configureRoutes(app: flask.Flask, devices: dict, scheduler: APScheduler):
    @app.route(API_START_URI + 'toggle', methods=['GET'])
    def toggle():
        device_name = request.args.get('device_name')
        if (device_name):
          device = devices.get(device_name)
          if (device != None):
            check_connection(device.connection)
            device.connection.toggle_light()
            return {
              "message": "ok"
            }
          else:
            return {
              "error": DEVICE_NOT_KNOWN
            }
        else:
          return {
            "error": NEED_TO_SPECIFY_DEVICE_NAME
          }

    @app.route(API_START_URI + 'brightness/<int:value>', methods=['GET'])
    def set_brightness(value):
        device_name = request.args.get('device_name')
        if (device_name):
          device = devices.get(device_name)
          if (device != None):
            check_connection(device.connection)
            def run():
                device.connection.set_brightness(value)
            t = Thread(target=run, daemon=True)
            t.start()
            print(value)
            return "ok"
          else:
            return {
              "error": DEVICE_NOT_KNOWN
            }
        else:
          return {
            "error": NEED_TO_SPECIFY_DEVICE_NAME
          }

    @app.route(API_START_URI + 'brightness/vary/<string:value>', methods=['GET'])
    def vary_brightness(value):
        device_name = request.args.get('device_name')
        if (device_name):
          device = devices.get(device_name)
          if (device != None):
            check_connection(device.connection)
            def run():
                device.connection.varyBrightness(int(value))
            t = Thread(target=run, daemon=True)
            t.start()
            return "ok"
          else:
            return {
              "error": DEVICE_NOT_KNOWN
            }
        else:
          return {
            "error": NEED_TO_SPECIFY_DEVICE_NAME
          }

    @app.route(API_START_URI + 'brightness', methods=['GET'])
    def get_brightness():
        device_name = request.args.get('device_name')
        if (device_name):
          device = devices.get(device_name)
          if (device != None):
            return {
              "message": str(device.connection.getBrightness())
            }
          else:
            return {
              "error": DEVICE_NOT_KNOWN
            }
        else:
          return {
            "error": NEED_TO_SPECIFY_DEVICE_NAME
          }

    @app.route(API_START_URI + 'active', methods=['GET'])
    def get_active_state():
      device_name = request.args.get('device_name')
      if (device_name):
        device = devices.get(device_name)
        if (device != None):
          return str(device.connection.is_connected())
        else:
          return {
            "error": DEVICE_NOT_KNOWN
          }
      else:
        return {
          "error": NEED_TO_SPECIFY_DEVICE_NAME
        }

    @app.route(API_START_URI + 'light_on_at', methods=['GET'])
    def light_on_at():
      device_name = request.args.get('device_name') and str(request.args.get('device_name'))
      hour = request.args.get('hour') and int(request.args.get('hour'))
      minute = request.args.get('minute') and int(request.args.get('minute'))
      second = request.args.get('second') and int(request.args.get('second'))
      if(device_name):
        if(valide_time(hour, minute, second)):
          device = devices.get(device_name)
          if (device != None):
            light_on_bulb_at(device.connection, scheduler, hour, minute, second)
            return {
              "message": DEVICE_SCHEDULE_OK,
              "device_name": device_name,
              "hour": hour,
              "minute": minute,
              "second": second,
            }
          else:
            return {
              "error": DEVICE_NOT_KNOWN
            }
        else:
          return {
              "error": INVALID_HOUR,
              "hour": hour,
              "minute": minute,
              "second": second,
            }
      else:
        return {
          "error": NEED_TO_SPECIFY_DEVICE_NAME
        }

    @app.route(API_START_URI + 'light_on_every_day_at', methods=['GET'])
    def light_on_every_day_at():
      device_name = request.args.get('device_name') and str(request.args.get('device_name'))
      hour = request.args.get('hour') and int(request.args.get('hour'))
      minute = request.args.get('minute') and int(request.args.get('minute'))
      second = request.args.get('second') and int(request.args.get('second'))
      if(device_name):
        if(valide_time(hour, minute, second)):
          device = devices.get(device_name)
          if (device != None):
            light_on_bulb_every_day_at(device.connection, scheduler, hour, minute, second)
            return {
              "message": DEVICE_SCHEDULE_OK,
              "device_name": device_name,
              "hour": hour,
              "minute": minute,
              "second": second,
            }
          else:
            return {
              "error": DEVICE_NOT_KNOWN
            }
        else:
          return {
              "error": INVALID_HOUR,
              "hour": hour,
              "minute": minute,
              "second": second
            }
      else:
        return {
          "error": NEED_TO_SPECIFY_DEVICE_NAME
        }

    @app.route(API_START_URI + 'light_on_every', methods=['GET'])
    def light_on_every():
      device_name = request.args.get('device_name') and str(request.args.get('device_name'))
      second = request.args.get('second') and int(request.args.get('second'))
      if(device_name):
        device = devices.get(device_name)
        if (device != None):
          toggle_light_every(device, scheduler, second)
          save_job(id=f"light_on_every_{second}_seconds", func="light_on_every", trigger="interval", device_name=device.name, second=1)
          return {
            "message": DEVICE_SCHEDULE_OK,
            "device_name": device_name,
            "second": second,
          }
        else:
          return {
            "error": DEVICE_NOT_KNOWN
          }
      else:
        return {
          "error": NEED_TO_SPECIFY_DEVICE_NAME
        }