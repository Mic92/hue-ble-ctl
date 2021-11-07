from typing import List
from Tools import check_connection
from HueDevice import HueDevice
from threading import Thread, Barrier
from flask import request
import flask

# Const
from Config import API_START_URI

DEVICE_NOT_KNOWN = "Device name not known"
NEED_TO_SPECIFY_DEVICE_NAME = "You need to specify device name : ?device_name=..."


def configureRoutes(app: flask.Flask, devices: dict):
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