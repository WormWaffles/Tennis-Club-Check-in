class Guest:
    def  __init__(self, first_name: str, last_name: str, phone_number: int, street_address: str, city: str, state: str, zip_code: int) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.street_address = street_address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.visits = 0