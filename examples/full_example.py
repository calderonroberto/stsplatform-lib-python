#!/bin/python

# To run this example from the root directory: python -m examples/simple_example
import random
import stsplatform.client as sts

# You will need your credentials configured here. Read more here:
# http://wotkit.readthedocs.org/en/latest/api_v1/api_authentication.html#keys-and-basic-authentication

KEY_ID = ''
KEY_PASSWORD = ''
SENSOR_NAME = 'calderonroberto.demo' # A sensor that is publicly available

def main():
    conf = {
        "url":"http://wotkit.sensetecnic.com/api",
        "auth":{"username":KEY_ID, "password":KEY_PASSWORD}
        }

    #create an stsplatform client with custom configuration
    c = sts.Client(conf)

    # Print a sensor hosted in the sts platform
    s = sts.Sensors(c, SENSOR_NAME)
    print "\n\n>>>>>> Sensor %s has the current structure: \n" % SENSOR_NAME
    print s.get().data

    # Print some data (last event) that lives in this sensor according to:
    # http://wotkit.readthedocs.org/en/latest/api_v1/api_sensor_data.html#raw-data-retrieval
    d = sts.Data(s)
    print "\n\n>>>>>> Sensor %s's last data point is: \n" % SENSOR_NAME
    print d.get({'beforeE':1}).data

    # Add some data
    d = sts.Data(s)
    randomvalue = random.randint(0,42)
    print "\n\n>>>>>> Sending data returned code %s\n" % d.post({"value":randomvalue}).code
    print "\nAnd here is the last data point of that sensor: "
    print d.get({'beforeE':1}).data

    # Accessing the Fields resource
    f = sts.Fields(s)
    print "\n\n>>>>>> Sensor %s has the following fields:" % SENSOR_NAME
    print f.get().data
    print "\n\nSensor %s has the following info on field 'value':" % SENSOR_NAME
    fi = sts.Fields(s, "value")
    print fi.get().data

    # Accessing the Orgs resources
    o = sts.Orgs(c, "sensetecnic")
    print "\n>>>>>> The organization sensetecnic information contains: \n"
    print o.get().data



if __name__ == "__main__":
    main()
