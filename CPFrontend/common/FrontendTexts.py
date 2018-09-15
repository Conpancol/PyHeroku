import json


class FrontendTexts:
    """El conjunto de todos los textos que figuran en la aplicacion - menus, ayudas, etiquetas"""
    def __init__(self, view):
        self.locale = "es_CO"
        self.view = view
        self.resource = "resources/language/" + view + '.' + self.locale + '.json'

        try:
            json_file = open(self.resource, encoding='utf8')
            json_data = json_file.read()
            data = json.loads(json_data)
            self.component = data[self.view]
            json_file.close()
        except KeyError as exception:
            print(exception)
            self.component = {'component': 'NA'}

    def __str__(self):
        return self.resource + '\n' + self.component

    def getComponent(self):
        return self.component
