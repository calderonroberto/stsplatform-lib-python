import unittest
import inspect
import random
import string
import json
import stsplatform.client as sts

print ">>>>> YOU MUST CONFIGURE YOUR KEY AND PASSWORD IN tests/alltests.py LINE 10 for testing this library"

KEY_ID = ''
KEY_PASSWORD = ''
TEST_SENSOR = 'calderonroberto.data' #a previously created sensor for tests

class TestSTSPlatform(unittest.TestCase):

    def setUp(self):
        self.config = {"url":"http://wotkit.sensetecnic.com/api","auth":{"key_id":KEY_ID, "key_password":KEY_PASSWORD}}
        self.config_url = {"url":"http://wotkit.sensetecnic.com/api/v1"}
        self.config_auth_username = {"auth":{"username":KEY_ID, "password":KEY_PASSWORD}}
        self.config_auth_key = {"auth":{"key_id":KEY_ID, "key_password":KEY_PASSWORD}}

    def tearDown(self):
        pass

    def test_should_initialize_without_config(self):
        w = sts.Client()
        self.assertEqual(w.url, "http://wotkit.sensetecnic.com/api")
        self.assertEqual(w.auth, None)

    def test_should_not_initialize_with_bad_args(self):
        self.assertRaises(Exception, sts.Client, {"url":"wrong"} )
        self.assertRaises(Exception,sts.Client, {"auth":{"u":"p"}} )

    def test_should_initialize_with_good_config(self):
        w = sts.Client(self.config)
        self.assertEqual(w.url, "http://wotkit.sensetecnic.com/api")
        self.assertEqual(w.auth, {'key_id':KEY_ID,'key_password':KEY_PASSWORD})
        w = sts.Client(self.config_url)
        self.assertEqual(w.url, "http://wotkit.sensetecnic.com/api/v1")
        self.assertEqual(w.auth, None)
        w = sts.Client(self.config_auth_username)
        self.assertEqual(w.auth, {'key_id':KEY_ID,'key_password':KEY_PASSWORD})

    def test_sensors(self):
        sensorname = ''.join(random.SystemRandom().choice(string.ascii_lowercase) for _ in range(7))
        testsensor = {
            'name':sensorname,
            'longName':'Delete Me Sensor',
            'description':'Sensor auto generated for tests..'
        }
        w = sts.Client(self.config)
        s = sts.Sensors(w)

        #has methods
        self.assertTrue(inspect.ismethod(s.get))
        self.assertTrue(inspect.ismethod(s.post))
        self.assertTrue(inspect.ismethod(s.delete))
        self.assertTrue(inspect.ismethod(s.put))

        #can be created
        r = s.post(testsensor)
        self.assertEquals(r.code, 201)

        #can be retrieved
        s = sts.Sensors(w, sensorname)
        r = s.get()
        self.assertEquals(r.data['name'], sensorname)

        #can be updated
        s = sts.Sensors(w,sensorname)
        r = s.put({'description':'An updated description'}) #update has no response
        self.assertEquals(r.code, 204)
        r = s.get()
        self.assertEquals(r.data['description'], 'An updated description')

        #can be deleted
        s = sts.Sensors(w,sensorname)
        r = s.delete()
        self.assertEquals(r.code, 204)

    def test_data(self):

        randomvalue= random.randrange(0, 101, 2)

        w = sts.Client(self.config)
        s = sts.Sensors(w, TEST_SENSOR)
        d = sts.Data(s)

        #has methods
        self.assertTrue(inspect.ismethod(d.get))
        self.assertTrue(inspect.ismethod(d.post))
        self.assertTrue(inspect.ismethod(d.delete))
        self.assertTrue(inspect.ismethod(d.put))

        #cam be created
        r = d.post({'value':randomvalue})
        self.assertEquals(r.code, 201)

        #can be retrieved
        r = d.get({'beforeE':'1'})
        self.assertEquals(r.data[0]['value'], randomvalue)

        #can upload batch data (put)
        batchdata = [
            {"timestamp":"2012-12-12T03:34:28.626Z","value":67.0,"lng":-123.1404,"lat":49.20532},
            {"timestamp":"2012-12-12T03:34:28.665Z","value":63.0,"lng":-123.14054,"lat":49.20554}
        ]
        r = d.put(batchdata)
        self.assertEquals(r.code, 204)

        #can delete data
        d = sts.Data(s,"2012-12-12T03:34:28.626Z")
        r = d.delete()
        self.assertEquals(r.code,204)


    def test_fields(self):

        newfield = {
            "name": "newfield",
            "longName": "newfield",
            "type": "NUMBER",
            "index": 99,
            "required": "false",
            "value": 0
        }

        w = sts.Client(self.config)
        s = sts.Sensors(w, TEST_SENSOR)
        f = sts.Fields(s)

        #can be retrieved
        r = f.get()
        self.assertEquals(r.data[0]['name'], 'value')

        #can be updated
        newfield['units'] = 'kms'
        f = sts.Fields(s, 'newfield')
        r = f.put(newfield)
        self.assertEquals(r.code,204)

        #can be deleted
        f = sts.Fields(s, 'newfield')
        r = f.delete()
        self.assertEquals(r.code,204)


    def test_tags(self):
        w = sts.Client(self.config)
        t = sts.Tags(w)

        #can be queried
        r = t.get()
        self.assertEquals(r.code, 200)

    def test_orgs(self):
        w = sts.Client(self.config)
        o = sts.Orgs(w)

        #can be queried
        r = o.get({'text':'sensetecnic'})
        self.assertEquals(r.code,200)

        #can get one Org
        o = sts.Orgs(w,'sensetecnic')
        r = o.get()
        self.assertEquals(r.data['name'],'sensetecnic')


    def test_news(self):
        w = sts.Client(self.config)
        n = sts.News(w)

        #can be queried
        r = n.get()
        self.assertEquals(r.code,200)

    def test_stats(self):
        w = sts.Client(self.config)
        s = sts.Stats(w)

        #can be queried
        r = s.get()
        self.assertEquals(r.code,200)

if __name__ == '__main__':
    unittest.main()
