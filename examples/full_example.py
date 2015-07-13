#!/bin/python

# To run this example from the root directory: python -m examples/simple_example

import stsplatform as sts

# You will need your credentials
KEY_ID = ''
KEY_PASSWORD = ''
SENSOR_NAME = 'mike.yvr-arrive'

def main():
    conf = {
        "url":"http://wotkit.sensetecnic.com/api",
        #"auth":{"username":KEY_ID, "password":KEY_PASSWORD}
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

    return

    print " Data >>>>>>>>>>>"
    data = w.Data(sensor)
    print data.post({"value":"620"})
    print data.get({"beforeE":"1"})
    print " "

    print " Fields >>>>>>>>>>>"
    fields = w.Fields(sensor)
    print fields.get()
    print " "
    field = w.Fields(sensor, "value")
    print field.get()
    print " "

    print "Tags >>>>>>>>>>>"
    tags = w.Tags(wotkit)
    print tags.get({"text":"weather"})
    print " "

    print "Orgs >>>>>>>>>>>"
    orgs = w.Orgs(wotkit, "sensetecnic")
    print orgs.get()
    print " "

    print "News >>>>>>>>>>>"
    news = w.News(wotkit)
    print news.get()
    print " "

    print "Stats >>>>>>>>>>>"
    stats = w.Stats(wotkit)
    print stats.get()
    print " "


if __name__ == "__main__":
    main()
