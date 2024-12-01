class WMSException(Exception):
    def __init__(self, message="Some error occurred!"):
        self.message = message
        super().__init__(self.message)

class ClaimException(Exception):
    def __init__(self, message="Invalid Claim"):
        self.message = message
        super().__init__(self.message)

class WarrantyException(Exception):
    def __init__(self, message="Invalid Warranty"):
        self.message = message
        super().__init__(self.message)

class ProductException(Exception):
    def __init__(self, message="Invalid Product"):
        self.message = message
        super().__init__(self.message)

class S3Exception(Exception):
    def __init__(self, message="Unable to upload document"):
        self.message = message
        super().__init__(self.message)