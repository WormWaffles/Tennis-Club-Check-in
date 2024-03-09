from random import randint
from src.guest import Guest

_guests = None

def get_all():
    global _guests


    class Guests:
        '''dict of Guest objects'''
        def __init__(self):
            self._guests: dict[str, Guest] = {}

        def get_all_guests(self):
            '''get all guests'''
            return self._guests
        
        def add_guest(self, first_name, last_name, phone_number, street_address, city, state, zip_code):
            '''add a guest'''
            guest_id = 'G' + str(randint(10000, 99999))
            self._guests[guest_id] = Guest(first_name, last_name, phone_number, street_address, city, state, zip_code)
            return guest_id
        
        def get_guest_by_id(self, guest_id):
            '''get a guest by id'''
            return self._guests[guest_id]
        
        def update_guest(self, guest_id, first_name, last_name, phone_number, street_address, city, state, zip_code):
            '''update a guest'''
            self._guests[guest_id] = Guest(first_name, last_name, phone_number, street_address, city, state, zip_code)
        
        def check_in(self, guest_id):
            '''check in a guest'''
            # search csv for guest_id
            with open('logs/guests/guests.csv', 'r') as guests:
                for line in guests:
                    if line.split(',')[0] == str(guest_id):
                        # if found, do not check in guest
                        return False
            # if not found, log in csv
            with open('logs/guests/guests.csv', 'a') as guests:
                guests.write(f'\n{guest_id},{self._guests[guest_id].first_name},{self._guests[guest_id].last_name},{self._guests[guest_id].phone_number},{self._guests[guest_id].street_address},{self._guests[guest_id].city},{self._guests[guest_id].state},{self._guests[guest_id].zip_code}')
            self._guests[guest_id].visits += 1
            return True
        
        def delete_guest(self, guest_id):
            '''deletes a guest'''
            guest = self._guests[guest_id]
            if not guest:
                return False
            del self._guests[guest_id]
            return True
        
        def clear(self) -> None:
            '''clears the guests'''
            self._guests.clear()
        
    if _guests is None:
        _guests = Guests()

    return _guests