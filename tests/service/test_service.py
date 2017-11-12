from service.server import Server
from service.components import Component
from unittest import TestCase
from unittest.mock import Mock, create_autospec
import requests, threading, time, json, os
from multiprocessing import Process

class TestServerAndComponent(TestCase):
    @classmethod
    def setUpClass(self):
        class MockComponent(Component):
            def process(self, json):
                return {"test" : "test"}

        self.component = MockComponent()
        self.server = Server("test", "4343")
        self.server.add_component_post("/test1", self.component)
        self.server.add_component_get("/test2", self.component)
        self.process = Process(target=self.server.run)
        self.process.start()
        time.sleep(5)

    @classmethod
    def tearDownClass(self):
        os.system("kill " + str(self.process.pid))
        time.sleep(5)

    def test_component_post_method_called(self):
        full_url = "http://127.0.0.1:4343/test1"
        request = json.loads('{"test":"test"}')
        r = requests.post(
            url = full_url,
            json = request)
        self.assertTrue("test" in r.text)

    def test_component_get_method_called(self):
        full_url = "http://127.0.0.1:4343/test2"
        request = json.loads("{}")
        r = requests.get(
            url = full_url,
            json = request)
        self.assertTrue("test" in r.text)
