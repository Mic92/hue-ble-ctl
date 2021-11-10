import time
from typing import List
from Tools import check_connection
from HueDevice import HueLight
from threading import Thread, Barrier
from flask import request
from flask_apscheduler import APScheduler
import flask

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
    def setBrightness(value):
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
    def varyBrightness(value):
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
    def getBrightness():
        device_name = request.args.get('device_name')
        if (device_name):
          device = devices.get(device_name)
          if (device != None):
            return str(device.getBrightness())
          else:
            return {
              "error": DEVICE_NOT_KNOWN
            }
        else:
          return {
            "error": NEED_TO_SPECIFY_DEVICE_NAME
          }

    @app.route(API_START_URI + 'active', methods=['GET'])
    def getActiveState():
        device_name = request.args.get('device_name')
        if (device_name):
          device = devices.get(device_name)
          if (device != None):
            return str(device.is_connected())
          else:
            return {
              "error": DEVICE_NOT_KNOWN
            }
        else:
          return {
            "error": NEED_TO_SPECIFY_DEVICE_NAME
          }

    def light_on_bulb_at(device: HueLight, hour: int , minute: int , seconde: int) -> bool:
      scheduler.add_job(id="blblbl", func=device.toggle_light, trigger="cron", args=[], hour=hour, minute=minute, second=seconde)

    @app.route(API_START_URI + 'light_on_at', methods=['GET'])
    def lightOnAt():
      device_name = request.args.get('device_name') and str(request.args.get('device_name'))
      hour = request.args.get('hour') and int(request.args.get('hour'))
      minute = request.args.get('minute') and int(request.args.get('minute'))
      seconde = request.args.get('seconde') and int(request.args.get('seconde'))
      if(device_name):
        if(hour
        and minute
        and seconde
        and hour >= 0
        and hour <= 23
        and minute >= 0
        and minute <= 59
        and seconde >= 0
        and seconde <= 59):
          device = devices.get(device_name)
          if (device != None):
            light_on_bulb_at(device.connection, hour, minute, seconde)
            return {
              "message": DEVICE_SCHEDULE_OK,
              "device_name": device_name,
              "hour": hour,
              "minute": minute,
              "seconde": seconde,
            }
          else:
            return {
              "error": DEVICE_NOT_KNOWN
            }
        else:
          return {
              "error": INVALID_HOUR
            }
      else:
        return {
          "error": NEED_TO_SPECIFY_DEVICE_NAME
        }