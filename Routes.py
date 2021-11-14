from typing import List
from Tools import check_connection
from threading import Thread
from flask import request
from flask_apscheduler import APScheduler
import flask
import Tools
import FR as LANG


# Const
from Config import API_START_URI



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
            "error": LANG.DEVICE_NOT_KNOWN
          }
      else:
        return {
          "error": LANG.NEED_TO_SPECIFY_DEVICE_NAME
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
            "error": LANG.DEVICE_NOT_KNOWN
          }
      else:
        return {
          "error": LANG.NEED_TO_SPECIFY_DEVICE_NAME
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
            "error": LANG.DEVICE_NOT_KNOWN
          }
      else:
        return {
          "error": LANG.NEED_TO_SPECIFY_DEVICE_NAME
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
            "error": LANG.DEVICE_NOT_KNOWN
          }
      else:
        return {
          "error": LANG.NEED_TO_SPECIFY_DEVICE_NAME
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
          "error": LANG.DEVICE_NOT_KNOWN
        }
    else:
      return {
        "error": LANG.NEED_TO_SPECIFY_DEVICE_NAME
      }

  @app.route(API_START_URI + 'light_on_at', methods=['GET'])
  def light_on_at():
    device_name = request.args.get('device_name') and str(request.args.get('device_name'))
    hour = request.args.get('hour') is not None and int(request.args.get('hour'))
    minute = request.args.get('minute') is not None and int(request.args.get('minute'))
    second = request.args.get('second') is not None and int(request.args.get('second'))
    if(device_name):
      if(Tools.valide_time(hour, minute, second)):
        device = devices.get(device_name)
        if (device != None):
          Tools.light_on_bulb_at(device.connection, scheduler, hour, minute, second)
          return {
            "message": LANG.DEVICE_SCHEDULE_OK,
            "device_name": device_name,
            "hour": hour,
            "minute": minute,
            "second": second,
          }
        else:
          return {
            "error": LANG.DEVICE_NOT_KNOWN
          }
      else:
        return {
            "error": LANG.INVALID_HOUR,
            "hour": hour,
            "minute": minute,
            "second": second,
          }
    else:
      return {
        "error": LANG.NEED_TO_SPECIFY_DEVICE_NAME
      }

  @app.route(API_START_URI + 'light_on_every_day_at', methods=['GET'])
  def light_on_every_day_at():
    device_name = request.args.get('device_name') and str(request.args.get('device_name'))
    hour = request.args.get('hour') is not None and int(request.args.get('hour'))
    minute = request.args.get('minute') is not None and int(request.args.get('minute'))
    second = request.args.get('second') is not None and int(request.args.get('second'))
    if(device_name):
      if(Tools.valide_time(hour, minute, second)):
        device = devices.get(device_name)
        if (device != None):
          job_id = f"light_on_bulb_every_day_at_{hour}:{minute}:{second}_on_device_{device_name}"
          Tools.save_job(
            id=job_id,
            func="light_on_every_day_at",
            trigger="cron",
            device_name=device.name,
            hour=hour,
            minute=minute,
            second=second
          )
          Tools.light_on_bulb_every_day_at(device.connection, scheduler, hour, minute, second)
          return {
            "message": LANG.DEVICE_SCHEDULE_OK,
            "device_name": device_name,
            "hour": hour,
            "minute": minute,
            "second": second,
          }
        else:
          return {
            "error": LANG.DEVICE_NOT_KNOWN
          }
      else:
        return {
            "error": LANG.INVALID_HOUR,
            "hour": hour,
            "minute": minute,
            "second": second
          }
    else:
      return {
        "error": LANG.NEED_TO_SPECIFY_DEVICE_NAME
      }

  @app.route(API_START_URI + 'light_on_every', methods=['GET'])
  def light_on_every():
    device_name = request.args.get('device_name') and str(request.args.get('device_name'))
    second = request.args.get('second') and int(request.args.get('second'))
    if(device_name):
      device = devices.get(device_name)
      if (device != None):
        Tools.toggle_light_every(device, scheduler, second)
        Tools.save_job(id=f"light_on_every_{second}_seconds", func="light_on_every", trigger="interval", device_name=device.name, second=1)
        return {
          "message": LANG.DEVICE_SCHEDULE_OK,
          "device_name": device_name,
          "second": second,
        }
      else:
        return {
          "error": LANG.DEVICE_NOT_KNOWN
        }
    else:
      return {
        "error": LANG.NEED_TO_SPECIFY_DEVICE_NAME
      }

  @app.route(API_START_URI + 'jobs', methods=['GET'])
  def get_jobs():
    device_name = request.args.get('device_name') and str(request.args.get('device_name'))
    tempResult = dict()
    if (device_name):
      for index, job in enumerate(Tools.get_jobs()):
        if (job.get("device_name") == device_name) : tempResult[index] = job
      return tempResult
    else:
      for index, job in enumerate(Tools.get_jobs()):
        tempResult[index] = job
      return tempResult

  @app.route(API_START_URI + 'jobs', methods=['DELETE'])
  def delete_job():
    job_id = request.args.get('job_id') and str(request.args.get('job_id'))
    if (job_id):
      Tools.delete_job(job_id)
      return {
        "message": LANG.DELETE_SCHEDULE_OK
      }
    else:
      return {
        "error": LANG.NEED_TO_SPECIFY_JOB_ID
      }