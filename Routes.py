from Tools import check_connection
from HueLight import HueLight
from threading import Thread, Barrier
import flask

# Const
from Config import API_START_URI


def configureRoutes(app: flask.Flask, device: HueLight):
    @app.route(API_START_URI + 'toggle', methods=['GET'])
    def toggle():
        check_connection(device)
        device.toggle_light()
        return ""

    @app.route(API_START_URI + 'brightness/<int:value>', methods=['GET'])
    def setBrightness(value):
        check_connection(device)
        device.set_brightness(value)
        return ""

    @app.route(API_START_URI + 'brightness/vary/<string:value>', methods=['GET'])
    def varyBrightness(value):
        check_connection(device)
        def run():
            device.varyBrightness(int(value))
            t = Thread(target=run, daemon=True)
        t.start()
        return "ok"

    @app.route(API_START_URI + 'brightness', methods=['GET'])
    def getBrightness():
        return str(device.getBrightness())

    @app.route(API_START_URI + 'active', methods=['GET'])
    def getActiveState():
        return str(device.is_connected())