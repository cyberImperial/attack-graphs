def use_mock_client(binder):
    binder.gets  = {}
    binder.posts = {}
    binder.lastest_post = None
    return binder

def mock_client(binder):
    class MockClient():
        def __init__(self, *args):
            self.binder = binder

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

    return MockClient
