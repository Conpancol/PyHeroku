class Comments:
    """clase base de comentarios"""
    def __init__(self):
        self.date = ''
        self.issuer = ''
        self.text = ''

    def setDate(self, date):
        self.date = date

    def setIssuer(self, issuer):
        self.issuer = issuer

    def setText(self, text):
        self.text = text

