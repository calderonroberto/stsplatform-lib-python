#!/bin/python

import requests
import re
import json
import time

class RequestHandler (object):
    """
    Main handler of the library. Defines successors in the chain of responsibility
    and in our case handles the REST requests to the STS Platform.
    """
    def __init__(self, successor=None, id=""):
        self.__successor = successor # private, yo
        self.resource = "/"+ self.__class__.__name__.lower() +"/"+str(id)
        #defaults:
        self.url = "http://wotkit.sensetecnic.com/api"
        self.auth = None

    def set_handler(self,handler):
        self.__successor = handler

    def set_config(self,config):
        """
        Override the default configuration of the client.
        Used to set a different STS Platform url and authentication key and password.
        """
        if 'url' in config:
            if re.match("http://",config["url"]) is None:
                raise STSPlatformError('Malformed URL string')
            else:
                self.url = config['url']

        if 'auth' in config:
            #key_id, key_password, access_token #TODO access token
            if 'username' not in config['auth'] and 'key_id' not in config['auth']:
                raise STSPlatformError('Malformed Auth dictionary')

            if 'username' in config['auth'] and 'password' in config['auth']:
                self.auth = {
                    'key_id': config['auth']['username'],
                    'key_password': config['auth']['password']
                    }
            if 'key_id' in config['auth'] and 'key_password' in config ['auth']:
                    self.auth = config['auth']

    def get(self, params=None, resource=""):
        """
        Makes a GET request
        Attributes:
            params -- the parameters as a dictionary: {'key':'value'}
        """
        if self.__successor != None:
            return self.__successor.get(params,  self.resource +  resource)
        else:
            params = self.__handle_params(params)
            auth = self.__handle_authentication()
            r = requests.get(self.url+resource,auth=auth,params=params)
            return (self.__handle_response(r))

    def post(self, payload=None, resource=""):
        """
        Makes a POST request
        Attributes:
            payload -- the payload as a dictionary: {'key':'value'}
        """
        if self.__successor != None:
            return self.__successor.post(payload, self.resource + resource)
        else:
            data = self.__handle_payload(payload)
            auth = self.__handle_authentication()
            headers = {'content-type': 'application/json'}
            r = requests.post(self.url+resource,auth=auth,headers=headers,data=data)
            return (self.__handle_response(r))

    def put(self, payload=None, resource=""):
        """
        Makes a PUT request
        Attributes:
            payload -- the payload as a dictionary: {'key':'value'}
        """
        if self.__successor != None:
            return self.__successor.put(payload, self.resource + resource)
        else:
            data = self.__handle_payload(payload)
            auth = self.__handle_authentication()
            headers = {'content-type': 'application/json'}
            r = requests.put(self.url+resource,auth=auth,headers=headers,data=data)
            return (self.__handle_response(r))

    def delete(self, params=None, resource=""):
        """
        Makes a DELETE request
        Attributes:
            params -- the parameters as a dictionary: {'key':'value'}
        """
        if self.__successor != None:
            return self.__successor.delete(params, self.resource + resource)
        else:
            params = self.__handle_params(params)
            auth = self.__handle_authentication()
            r = requests.delete(self.url+resource,auth=auth,params=params)
            return (self.__handle_response(r))

    #### private methods

    def __handle_response(self,r):
        """
        Create a STSPlatformResponse from a requests response
        """
        return STSPlatformResponse(r)

    def __handle_authentication(self):
        """
        Create an object (key,value) for requests from a Client {auth:{key:value}} object
        """
        if self.auth is None:
            return self.auth
        else:
            return (self.auth["key_id"],self.auth["key_password"])

    def __handle_params(self,params):
        """
        Handle parameters received. Make sure params is not empty
        """
        if params is None:
            return {}
        else:
            return params

    def __handle_payload (self, payload):
        """
        Handle payload received, attempting to create a json string.
        """
        payload = self.__handle_params(payload)
        try:
            return json.dumps(payload)
        except:
            raise STSPlatformError("Malformed payload")


class STSPlatformResponse(object):
    """
    A response object from any STS Platform Resource.
    It contains the following parameters:

    data -- dictionary built from parsing the server JSON response
    code -- an integer storing the REST code response received on the call
    """
    def __init__(self,response):
        try:
            self.data = response.json()
        except:
            self.data = None
        self.code = response.status_code


class STSPlatformError(Exception):
    """
    Raised when the client received an error
    Attributes:
        error -- the error raised
    """
    def __init__(self,error):
        self.error = error


#our base class
class Client(RequestHandler):
    """
    The base class of this library.

    Attributes:
        config -- (optional) a configuration dictionary

    Returns:
        an STSPlatformResponse object containing "data" and "code" parameters

    The configuration should be:
    {
        "url": "http://wotkit.sensetecnic.com/api",
        "auth": {}
    }
    Auth should contain either username and password or oauth key, for example:
    {"username":"john", "password":"smith"} or {"oauth_key":"2341lkj2f12341"}
    """
    def __init__(self, config=None):
        super(Client,self).__init__(None)
        if config is not None:
                self.set_config(config)

class Sensors(RequestHandler):
    """
    The Sensors resource of the STS Platform API

    Attributes:
        handler -- a client object
        id -- (optional) the numerical or string id of the sensor

    Returns:
        an STSPlatformResponse object containing "data" and "code" parameters

    Inherits from RequestHandler, with access to the get, post, put and delete methods.
    """
    def __init__(self, handler, id=""):
        super(Sensors,self).__init__(handler, id)

class Data(RequestHandler):
    """
    The Data resource of the STS Platform API

    Attributes:
        handler -- a sensor object
        id -- (optional) the id (timestamp of the data), only used to delete

    Returns:
        an STSPlatformResponse object containing "data" and "code" parameters

    Inherits from RequestHandler, with access to the get, post, put and delete methods.
    """
    def __init__(self, handler, id=""):
        super(Data,self).__init__(handler, id)

class Fields(RequestHandler):
    """
    The Fields resource of the STS Platform API

    Attributes:
        handler -- a client object
        id -- (optional) the numerical or string id of the field

    Returns:
        an STSPlatformResponse object containing "data" and "code" parameters

    Inherits from RequestHandler, with access to the get, post, put and delete methods.
    """
    def __init__(self, handler, id=""):
        super(Fields,self).__init__(handler, id)

class Tags(RequestHandler):
    """
    The Tags resource of the library

    Attributes:
        handler -- a client object
        id -- (optional) the numerical or string id of the tag

    Returns:
        an STSPlatformResponse object containing "data" and "code" parameters

    Inherits from RequestHandler, with access to the get, post, put and delete methods.
    """
    def __init__(self, handler,id=""):
        super(Tags,self).__init__(handler, id)

class Orgs(RequestHandler):
    """
    The Orgs resource of the STS Platform API

    Attributes:
        handler -- a client object
        id -- (optional) the numerical or string id of the organization

    Returns:
        an STSPlatformResponse object containing "data" and "code" parameters

    Inherits from RequestHandler, with access to the get, post, put and delete methods.
    """
    def __init__(self,handler,id=""):
        super(Orgs,self).__init__(handler, id)

class News(RequestHandler):
    """
    The News resource of the STS Platform API

    Attributes:
        handler -- a client object
        id -- (optional) the numerical or string id of the news

    Returns:
        an STSPlatformResponse object containing "data" and "code" parameters

    Inherits from RequestHandler, with access to the get, post, put and delete methods.
    """
    def __init__(self,handler,id=""):
        super(News,self).__init__(handler, id)

class Stats(RequestHandler):
    """
    The Stats resource of the STS Platform API

    Attributes:
        handler -- a client object
        id -- (optional) the numerical or string id of the stats

    Returns:
        an STSPlatformResponse object containing "data" and "code" parameters

    Inherits from RequestHandler, with access to the get, post, put and delete methods.
    """
    def __init__(self,handler,id=""):
        super(Stats,self).__init__(handler, id)
