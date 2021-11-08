#!/usr/bin/env python
import dbus
import gatt
from typing import Dict, List
from threading import Thread, Barrier
from Routes import configureRoutes
from Config import DEVICES_DEFINITION
from HueDevice import HueDevice
from flask_apscheduler import APScheduler
import flask

from HueLight import HueLight

# Import json file
import json
with open('./jobs.json') as f:
  jobs = json.load(f)

def job1(var_one, var_two):
      print(str(var_one) + " " + str(var_two))

def job2(var_one, var_two):
      print(str(var_one) + " " + str(var_two))

def jobJsonToObj(job):
  jobFunc = None
  if (job["func"] == "job1"):
    jobFunc = job1
  else:
    jobFunc = job2
  return {
    "id": job["id"],
    "func": jobFunc,
    "trigger": job["trigger"],
    "args": job["args"],
    "hour": job["hour"],
    "minute": job["minute"],
    "second": job["second"]
  }

if __name__ == '__main__':
  # Set configuration values
  class Config:
      SCHEDULER_API_ENABLED = True
      SCHEDULER_TIMEZONE = "Europe/Paris"
      JOBS = list(map(jobJsonToObj , jobs))


  devices = dict()
  # device = HueLight(mac_address="FD:4A:25:A6:62:80", manager=manager, barrier=b)

  for device_def in DEVICES_DEFINITION:
    device = HueDevice(device_def["name"], device_def["mac_address"])
    def run():
      device.open_connection()
      devices[device_def["name"]] = device
      device.connection.connect()
      device.manager.run()
    t = Thread(target=run, daemon=True)
    t.start()
    device.barrier.wait()


  app = flask.Flask(__name__)
  app.config.from_object(Config())
  # initialize scheduler
  scheduler = APScheduler()
  scheduler.init_app(app)
  scheduler.start()

  # scheduler.add_job(id="job1", func=job1, args=['one', 'two'], trigger="cron", hour=21, minute=26, second=1)
  configureRoutes(app, devices)

  app.run(
    debug=True,
    host='0.0.0.0',
    use_reloader=False
  )