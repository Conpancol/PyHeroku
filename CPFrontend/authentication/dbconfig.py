class DBConfig:
    """Get all db configuration from environmental variable"""
    def __init__(self, envar):
        try:
            self.dbconfig = {}
            self.extractInfo(envar)

        except Exception as ex:
            print(ex)

    def extractInfo(self, envar):

        if envar != None:
            clean_envar = envar[11:]
            tokens = clean_envar.split('@')
            user_pwd = tokens[0].split(':')
            host_port_name = tokens[1].split('/')
            username = user_pwd[0]
            pwd = user_pwd[1]
            host_port = host_port_name[0].split(':')
            host = host_port[0]
            port = host_port[1]
            name = host_port_name[1]

            self.dbconfig['dbname'] = name
            self.dbconfig['dbuser'] = username
            self.dbconfig['dbpwd'] = pwd
            self.dbconfig['dbhost'] = host
            self.dbconfig['dbport'] = port

        else:
            raise Exception('No environment variable defined')

    def getConfig(self):
        return self.dbconfig
