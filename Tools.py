from typing import List
from HueLight import HueLight
from HueDevice import HueDevice
import datetime
import json
from random import random
from Config import DEVICES_DEFINITION
from threading import Thread
from HueDevice import HueDevice
from flask_apscheduler import APScheduler

#### Bluetooth methods

###
# Check connection, and try to reconnect if disconnected
###
def check_connection(device: HueLight) -> None:
  if (not device.is_connected()):
      print("Reconnecting")
      device.connect()

def get_initialized_devices():
  devices = dict()
  for device_def in DEVICES_DEFINITION:
    device = HueDevice(device_def["name"], device_def["mac_address"])
    def run():
      device.open_connection()
      devices[device_def["name"]] = device
      device.connection.connect()
      device.manager.run()
    t = Thread(target=run, daemon=True)
    t.start()
    # device.barrier.wait()
  return devices

#### JSON Methods

###
# Get all jobs from jobs.json
###
def get_jobs():
  with open('./jobs.json') as f:
    return json.load(f)

###
# Replace all jobs from jobs.json
###
def overwrite_jobs(jobs):
  with open('./jobs.json', 'w') as outfile:
    json.dump(jobs, outfile)

###
# Delete one job from jobs.json
###
def delete_job(job_id):
  overwrite_jobs(
    list(
      filter(
        lambda job: job["id"] != job_id,
        get_jobs()
      )
    )
  )

###
# Find one job from jobs.json
###
def find_job(id: str):
  find_id = filter(lambda job: job.get("id") == id, get_jobs())
  try:
    return next(find_id)
  except:
    return None

###
# Add one job to jobs.json
###
def save_job(id: str, func: str, trigger: str, **kwargs):
  to_save = get_jobs()
  find_id = find_job(id)
  if (find_id is None):
    to_append = {
      "id": id,
      "func": func,
      "trigger": trigger,
    }
    print(kwargs)
    for key, value in kwargs.items():
      to_append[key] = value
    to_save.append(to_append)
    overwrite_jobs(to_save)

###
# Read jobs from jobs.json, and add them to schedule list
###
def jobJsonToJob(job, scheduler, devices):
  device_name = job.get("device_name")
  second = job.get("second")
  if (device_name and second):
    jobFunc = None
    # Get device
    device = devices.get(device_name)
    if (device):
      # Get function
      if (job["func"] == "light_on_every"):
        toggle_light_every(device, scheduler, job["second"])
      elif (job["func"] == "light_on_every_day_at"):
        light_on_bulb_every_day_at(device.connection, scheduler, job["hour"], job["minute"], job["second"])
  return None


#### Schedule methods

def initialize_scheduler(app):
  scheduler = APScheduler()
  scheduler.init_app(app)
  scheduler.start()
  return scheduler

###
# Schedule light on at a given time
###
def light_on_bulb_at(device: HueLight, scheduler: APScheduler, hour: int , minute: int , second: int) -> bool:
  scheduler.add_job(
    id=str(random()),
    func=device.toggle_light,
    trigger="cron",
    hour=hour,
    minute=minute,
    second=second
  )

###
# Schedule light on every day at a given time
###
def light_on_bulb_every_day_at(device: HueLight, scheduler: APScheduler, hour: int , minute: int , second: int) -> bool:
  scheduler.add_job(
    id=str(random()),
    func=device.light_on,
    trigger="cron",
    hour=hour,
    minute=minute,
    second=second,
  )

###
# Schedule light on every x second
###
def toggle_light_every(device: HueDevice, scheduler: APScheduler, second: int) -> bool:
  scheduler.add_job(
    id=str(random()),
    func=device.connection.toggle_light,
    trigger="interval",
    seconds=second
  )

#### Time methods

###
# Return true if the given time is valid
###
def valide_time(hour: int, minute: int, second: int):
  try:
    datetime.time(hour, minute, second)
    return True
  except:
    return False
