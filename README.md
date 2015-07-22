STSPlatform Client
==================

This library allows developers to use the STS Platform (including the FREE version 'WoTKit').

# Dependencies

* Requests >= 2.2.1

# Installing the library

You can install using pip with:

```
pip install stsplatform
```

# Getting Started

Import the library:
```
import stsplatform.client as sts
```

Create an STS Platform client:
```
w = sts.Client()
```

Print a sensor hosted in the platform
```
s = sts.Sensors(w,'mike.yvr-arrive')
print s.get().data
```

Print some data (last data point)
```
d = sts.Data(s)
print d.get({'beforeE':1}).data
```
# Using the library

All methods rely on the Client Class. The parameter CONF is not required, but allows you to configure your client to specify your credentials and url of the STS Platform instance you want to access. By default the client will use the community edition of the STS Platform (WoTKit):

A common configuration object is:

```
CONF = {
  "url":"http://wotkit.sensetecnic.com/api",
  "auth":{"key_id":KEY_ID, "key_password":KEY_PASSWORD},  
}
```

You can then instantiate your client like this:

```
c = sts.Client(CONF)
```

To access resources you build them up hierarchically. A sensor lives in an STS Platform Server:
```
c = sts.Client(CONF)
s = sts.Sensors(c, 'SENSORNAME')
```

Sensor data lives in a Sensor:
```
c = sts.Client(CONF)
s = sts.Sensors(c, 'SENSORNAME')
d = sts.Data(s)
```

And so on. Each element that uses the Client class can access GET, POST, PUT and DELETE methods. These methods take parameters and return a STSPlatformResponse object containing "data" and "code". Data is the parsed response from the STS Platform server. Code is an integer response code from the STS Platform server:

```
c = sts.Client(CONF)
s = sts.Sensors(c, 'SENSORNAME')
d = sts.Data(s)
response = d.get({'parameter':'parametervalue'})

print response.code
print response.data
```

For more information on the API, support and examples visit [http://developers.sensetecnic.com](http://developers.sensetecnic.com)

# Supported Resources

To get started, import the library:
```
import stsplatform.client as sts
```

#### Configuring the client

You can configure the client to use a different STS Platform URL (in this case the free version 'WoTKit'). You can also configure it to use a username and password, or a valid key_id and key_password:
```
conf = {
  "url":"http://wotkit.sensetecnic.com/api",
  #"auth":{"username":USERNAME, "password":PASSWORD},
  #"auth":{"key_id":KEY_ID, "key_password":KEY_PASSWORD},  
}
client = sts.Client(conf)
```

#### Get Sensors

```
c = sts.Client(CONF)
s = sts.Sensors(c, SENSOR_NAME)
print s.get().data
```

#### Get Data:

```
c = sts.Client(CONF)
s = sts.Sensors(c, SENSOR_NAME)
d = sts.Data(s)
print d.get({'beforeE':1}).data
```

#### Publish Data

```
c = sts.Client(CONF)
s = sts.Sensors(c, SENSOR_NAME)
d = w.Data(s)
print d.post({"value":620}).code #print reponse code
print d.get({"beforeE":"1"}).data
```

#### Get Sensor Fields

```
c = sts.Client(CONF)
s = sts.Sensors(c, SENSOR_NAME)
fs = c.Fields(s)
print fs.get().data
f = c.Fields(s, "value")
print f.get().data
```

#### Organizations

```
c = sts.Client(CONF)
o = sts.Orgs(c, "sensetecnic")
print o.get().data
```

# Development

Clone the latest stable (Master) repository:

```
git clone https://github.com/SenseTecnic/stsplatform-lib-python
cd stsplatform-lib-python
```

Run the tests:

```
python setup.py test
```

Install in system for development (creates a link to your project)

```
python setup.py develop
```
