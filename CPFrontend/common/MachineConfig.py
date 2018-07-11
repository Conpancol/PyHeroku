import os


class MachineConfigurator:
    """configurations"""
    def __init__(self):
        self.backend = ""
        self.local_backend = 'http://localhost:4567'

    def getBackend(self):
        envvar = os.getenv('BACKEND_URL')
        print(envvar)
        if envvar is None:
            return self.local_backend
        else:
            return envvar


