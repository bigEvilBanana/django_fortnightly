class CompanyNotSupported(Exception):
    def __init__(self, message, *args, **kwargs):
        self.message = message
        super(CompanyNotSupported, self).__init__(*args, *kwargs)

    def __str__(self):
        return self.message
