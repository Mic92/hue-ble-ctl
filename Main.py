#!/usr/bin/env python
from typing import Dict, List
from Routes import configureRoutes
import Tools
from flask_apscheduler import APScheduler
import flask

from HueLight import HueLight

#Config Timezone
class Config:
  SCHEDULER_API_ENABLED = False
  SCHEDULER_TIMEZONE = "Europe/Paris"

if __name__ == '__main__':

  # Initialize bluetooth connection with saved devices
  devices = Tools.get_initialized_devices()

  # Create App
  app = flask.Flask(__name__)

  #Configure App with Config class
  app.config.from_object(Config())

  # initialize scheduler
  scheduler = Tools.initialize_scheduler(app)

  # Add saved jobs
  jobs = Tools.get_jobs()
  for job in jobs:
    Tools.jobJsonToJob(job, scheduler, devices)

  # Configure routes
  configureRoutes(app, devices, scheduler)

  # Run app
  app.run(
    debug=True,
    use_reloader=True,
    host='0.0.0.0'
  )