import json, requests

class Client():
    """
    A wrapper for RESTful requests made to a server.
    """

    def __init__(self, url, port):
        self.url = url
        self.port = port

    def get(self, resource):
        pass

    def post(self, resource, json):
        full_url = self.url + ":" + self.port + resource
        try:
            r = requests.post(
                url = full_url,
                json = json)
        except Exception as e:
            pass

class DBRequst(Client):
    def db_request(self, resource, product, version):
        db_json = json.loads("[{ \
            \"product\" : \"" + product + "\",\
            \"version\" : \"" + version + "\"\
        }]")
        return self.post(resource, resource, db_json)
