#!/bin/python

import requests
import re
import json
import time

class RequestHandler (object):

    def __init__(self, successor=None, id=""):
        self.__successor = successor # private, yo
        self.resource = "/"+ self.__class__.__name__.lower() +"/"+str(id)
        #defaults
        self.url = "http://wotkit.sensetecnic.com/api"
        self.auth = None

    def set_handler(self,handler):
        self.__successor = handler

    def set_config(self,config):

        if 'url' in config:
            if re.match("http://",config["url"]) is None:
                raise WotkitError('Malformed URL string')
            else:
                self.url = config['url']

        if 'auth' in config: #and username and password TODO
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
        if self.__successor != None:
            return self.__successor.get(params,  self.resource +  resource)
        else:
            if params is None:
                params = {}
            if self.auth is None:
                auth = self.auth
            else:
                auth = (self.auth["key_id"],self.auth["key_password"])
            r = requests.get(self.url+resource,auth=auth,params=params)
            return (self.__handle_response(r))

    def post(self, payload=None, resource=""):
        if self.__successor != None:
            return self.__successor.post(payload, self.resource + resource)
        else:
            if payload is None:
                payload = {}
            if self.auth is None:
                auth = self.auth
            else:
                auth = (self.auth["key_id"],self.auth["key_password"])
            try:
                data = json.dumps(payload)
            except:
                raise STSPlatformError("Malformed payload")
            headers = {'content-type': 'application/json'}
            r = requests.post(self.url+resource,auth=auth,headers=headers,data=data)
            return (self.__handle_response(r))

    def put(self, payload=None, resource=""):
        if self.__successor != None:
            return self.__successor.put(payload, self.resource + resource)
        else:
            if payload is None:
                payload = {}
            if self.auth is None:
                auth = self.auth
            else:
                auth = (self.auth["key_id"],self.auth["key_password"])
            try:
                data = json.dumps(payload)
            except:
                raise STSPlatformError("Malformed payload")
            headers = {'content-type': 'application/json'}
            r = requests.put(self.url+resource,auth=auth,headers=headers,data=data)
            return (self.__handle_response(r))

    def delete(self, params=None, resource=""):
        if self.__successor != None:
            return self.__successor.delete(params, self.resource + resource)
        else:
            if params is None:
                params = {}
            if self.auth is None:
                auth = self.auth
            else:
                auth = (self.auth["key_id"],self.auth["key_password"])
            r = requests.delete(self.url+resource,auth=auth,params=params)
            return (self.__handle_response(r))

    # private methods

    def __handle_response(self,r):
        return STSPlatformResponse(r)

class STSPlatformResponse(object):
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
    The base class of our library

    Attributes:
        config -- a configuration dictionary

    The configuration should be:
    {
        "url": "http://wotkit.sensetecnic.com/api",
        "auth": {}
    }
    Auth should contain either username and password or oauth key for example {"username":"john", "password":"smith"} or {"oauth_key":"2341lkj2f12341"}
    """
    def __init__(self, config=None):
        super(Client,self).__init__(None)
        if config is not None:
                self.set_config(config)

class Sensors(RequestHandler):
    def __init__(self, handler, id=""):
        super(Sensors,self).__init__(handler, id)

class Data(RequestHandler):
    def __init__(self, handler, id=""):
        super(Data,self).__init__(handler, id)

class Fields(RequestHandler):
    def __init__(self, handler, id=""):
        super(Fields,self).__init__(handler, id)

class Tags(RequestHandler):
    def __init__(self, handler,id=""):
        super(Tags,self).__init__(handler, id)

class Orgs(RequestHandler):
    def __init__(self,handler,id=""):
        super(Orgs,self).__init__(handler, id)

class News(RequestHandler):
    def __init__(self,handler,id=""):
        super(News,self).__init__(handler, id)

class Stats(RequestHandler):
    def __init__(self,handler,id=""):
        #resource = "/stats/"+str(id)
        super(Stats,self).__init__(handler, id)
