#!/bin/python

# To run this example from the root directory: python -m examples/simple_example

import stsplatform as sts

SENSOR_NAME = 'mike.yvr-arrive'

def main():
    conf = {
        "url":"http://wotkit.sensetecnic.com/api",
        }

    #create an stsplatform client with custom configuration
    w = sts.Client(conf)

    # Print a sensor hosted in the sts platform
    s = sts.Sensors(w, SENSOR_NAME)
    print "\n\nSensor %s has the current structure: \n" % SENSOR_NAME
    print s.get().data

    # Print some data (last event) that lives in this sensor according to:
    # http://wotkit.readthedocs.org/en/latest/api_v1/api_sensor_data.html#raw-data-retrieval
    d = sts.Data(s)
    print "\n\nSensor %s's last data point is: \n" % SENSOR_NAME
    print d.get({'beforeE':1}).data


if __name__ == "__main__":
    main()
