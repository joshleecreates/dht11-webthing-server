from __future__ import division, print_function
from webthing import (Action, Event, SingleThing, Property, Thing, Value,
                      WebThingServer)
import logging
import random
import time
import tornado.ioloop
import uuid
import dhtadapter


class TemperatureHumiditySensor(Thing):
    """A DHT11 Temperature & Humidity Sensor Adapter."""

    def __init__(self):
        Thing.__init__(
            self,
            'urn:dev:ops:dht11-temp',
            'DHT11 Temperature Sensor',
            ['TemperatureSensor', 'MultiLevelSensor'],
            'A temperature sensor'
        )
        self.temperature = Value(0)
        self.add_property(
            Property(self,
                     'temperature',
                     self.temperature,
                     metadata={
                         '@type': 'TemperatureProperty',
                         'title': 'Temperature',
                         'type': 'integer',
                         'description': 'The temperature in celsius',
                         'readOnly': True,
                     }))
        self.humidity = Value(0)
        self.add_property(
            Property(self,
                     'humidity',
                     self.humidity,
                     metadata={
                         '@type': 'LevelProperty',
                         'title': 'Humidity',
                         'type': 'integer',
                         'description': 'The current humidity in %',
                         'minimum': 0,
                         'maximum': 100,
                         'unit': 'percent',
                         'readOnly': True,
                     }))

        logging.debug('starting the sensor update looping task')
        self.timer = tornado.ioloop.PeriodicCallback(
            self.update_level,
            3000
        )
        self.timer.start()

    def update_level(self):
        results = dhtadapter.get_results()
        logging.debug('setting new humidity level: %s', results.humidity)
        logging.debug('setting new temperature: %s', results.temperature)
        self.humidity.notify_of_external_update(results.humidity)
        self.temperature.notify_of_external_update(results.temperature)

    def cancel_update_level_task(self):
        self.timer.stop()

def run_server():

    # Create a thing that represents a humidity sensor
    sensor = TemperatureHumiditySensor()

    # If adding more than one thing, use MultipleThings() with a name.
    # In the single thing case, the thing's name will be broadcast.
    server = WebThingServer(SingleThing(sensor), port=8888)
    try:
        logging.info('starting the server')
        server.start()
    except KeyboardInterrupt:
        logging.debug('canceling the sensor update looping task')
        sensor.cancel_update_level_task()
        logging.info('stopping the server')
        server.stop()
        logging.info('done')


if __name__ == '__main__':
    logging.basicConfig(
        level=10,
        format="%(asctime)s %(filename)s:%(lineno)s %(levelname)s %(message)s"
    )
    run_server()

