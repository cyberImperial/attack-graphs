from service.server import Server
from service.components import Component
from unittest import TestCase
from unittest.mock import MagicMock
from unittest.mock import create_autospec
import requests, threading, time, json

class TestServerAndComponent(TestCase):
    @classmethod
    def setUpClass(self):
        self.server = Server("test", "4343")
        self.component = Component()
        self.component.receive_post = MagicMock()
        self.component.receive_get = MagicMock()
        self.server.add_component_post("/test1", self.component)
        self.server.add_component_get("/test2", self.component)
        threading.Thread(target=self.server.run).start()
        time.sleep(3)

    def test_component_post_method_called(self):
        full_url = "http://127.0.0.1:4343/test1"
        request = json.loads("{}")
        r = requests.post(
            url = full_url,
            json = request)
        self.component.receive_post.assert_called_once_with()

    def test_component_get_method_called(self):
        full_url = "http://127.0.0.1:4343/test2"
        request = json.loads("{}")
        r = requests.get(
            url = full_url,
            json = request)
        self.component.receive_get.assert_called_once_with()
