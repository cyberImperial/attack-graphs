def mock_client(binder):
    client_cls = MockClient
    client_cls.binder = binder
    client_cls.binder.gets  = {}
    client_cls.binder.posts = {}
    client_cls.binder.lastest_post = None
    return client_cls

class MockClient():
    def __init__(self, *args):
        pass

    @property
    def url(self):
        return "http://test"

    @property
    def port(self):
        return "5000"

    def get(self, resource, default=None):
        if resource in self.binder.gets:
            self.binder.gets[resource] += 1
        else:
            self.binder.gets[resource] = 1
        return default

    def post(self, resource, json, default=None):
        if resource in self.binder.posts:
            self.binder.posts[resource] += 1
        else:
            self.binder.posts[resource] = 1
        self.binder.lastest_post = json
        return default
