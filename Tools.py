from typing import List
from HueLight import HueLight
from HueDevice import HueDevice
import datetime
import json
from random import random
from flask_apscheduler import APScheduler

# Bluetooth methods
def check_connection(device: HueLight) -> None:
  if (not device.is_connected()):
      print("Reconnecting")
      device.connect()

# JSON Methods
def get_jobs():
      with open('./jobs.json') as f:
        return json.load(f)

def save_job(id: str, func: str, trigger: str, **kwargs):
  to_save = get_jobs()
  to_append = {
    "id": id,
    "func": func,
    "trigger": trigger,
  }
  if kwargs.get("args"): to_append["args"] = kwargs.get("args")
  if kwargs.get("hour"): to_append["hour"] = kwargs.get("hour")
  if kwargs.get("minute"): to_append["minute"] = kwargs.get("minute")
  if kwargs.get("start_date"): to_append["start_date"] = kwargs.get("start_date")
  if kwargs.get("second"): to_append["second"] = kwargs.get("second")
  if kwargs.get("device_name"): to_append["device_name"] = kwargs.get("device_name")
  to_save.append(to_append)
  with open('./jobs.json', 'w') as outfile:
    json.dump(to_save, outfile)

def jobJsonToObj(job, scheduler, devices):
  device_name = job.get("device_name")
  second = job.get("second")
  if (device_name and second):
    jobFunc = None
    # Get function
    if (job["func"] == "light_on_every"):
      jobFunc = toggle_light_every
    # Get device
    device = devices.get(device_name)
    if (device):
      return {
        "id": job["id"],
        "func": jobFunc,
        "trigger": job["trigger"],
        "device": device,
        "scheduler": scheduler,
        "second": second
      }
  return None


# Schedule methods
def light_on_bulb_at(device: HueLight, scheduler: APScheduler, hour: int , minute: int , second: int) -> bool:
  scheduler.add_job(
    id=str(random()),
    func=device.toggle_light,
    trigger="cron",
    hour=hour,
    minute=minute,
    second=second
  )

def light_on_bulb_every_day_at(device: HueLight, scheduler: APScheduler, hour: int , minute: int , second: int) -> bool:
  datetime_object1 = datetime.datetime.now()
  datetime_object2 = datetime.time(hour, minute, second)
  datetime_object = datetime.datetime.combine(datetime_object1.date(), datetime_object2)
  scheduler.add_job(
    id=str(random()),
    func=device.toggle_light,
    trigger="cron",
    hour=hour,
    minute=minute,
    second=second,
    start_date=datetime_object
  )

def toggle_light_every(device: HueDevice, scheduler: APScheduler, second: int) -> bool:
  scheduler.add_job(
    id=str(random()),
    func=device.connection.toggle_light,
    trigger="interval",
    seconds=second
  )

# Time methods
def valide_time(hour: int, minute: int, second: int):
  try:
    datetime.time(hour, minute, second)
    return True
  except:
    return False
