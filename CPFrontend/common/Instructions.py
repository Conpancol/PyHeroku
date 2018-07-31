import json


class Instructions:
    """Instrucciones de la funcionalidad de la apliacion"""
    def __init__(self, app, view):
        self.locale = "es_CO"
        self.app = app
        self.view = view
        self.resource = "resources/instructions/" + app + '.' + self.locale + '.json'

        try:
            json_file = open(self.resource, encoding='utf8')
            json_data = json_file.read()
            data = json.loads(json_data)
            self.title = data[self.view]['title']
            self.steps = data[self.view]['steps']
            json_file.close()
        except KeyError as exception:
            print(exception)
            self.title = 'NA'
            self.steps = ['NA']

    def __str__(self):
        return self.resource + '\n' + self.title

    def getTitle(self):
        return self.title

    def getSteps(self):
        return self.steps
