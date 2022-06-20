

class AbstractIntegration:
    _application = None

    def __init__(self, application):
        self._application = application

    def list_permissions(self):
        """List available permissions for this application"""
        raise NotImplemented

    def lookup_user(self, user_id):
        """Verify user exists and is active and return the correct user_id"""
        raise NotImplemented

    def grant_access(self, user_id, permissions: list[str]):
        raise NotImplemented

    def remove_access(self, user_id, permission: str):
        raise NotImplemented


class DummyIntegration(AbstractIntegration):

    _permissions = ["Lorem", "ipsum", "dolor", "sit", "amet", "consectetuer", "adipiscing", "elit", "Donec", "odio", "Quisque", "volutpat", "mattis", "eros", "Nullam", "malesuada", "erat", "ut", "turpis", "Suspendisse", "urna", "nibh", "viverra", "non", "semper", "suscipit", "posuere", "pede"]

    def list_permissions(self):
        return self._permissions

    def lookup_user(self, user_id):
        return user_id

    def grant_access(self, user_id, permissions=None):
        return True

    def remove_access(self, user_id, permission=None):
        return True
