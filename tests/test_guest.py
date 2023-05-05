from src.guests import get_all

def test_get_all_guests():
    guests = get_all()
    guests.clear()
    assert len(guests.get_all_guests()) == 0
    guest1 = guests.add_guest('John', 'Doe', '555-555-5555', '123 Main St', 'Anytown', 'NY')
    assert len(guests.get_all_guests()) == 1
    guest2 = guests.add_guest('Colin', 'Brown', '336-279-6083', '6184 Barmot Dr', 'Greensboro', 'NC')
    assert len(guests.get_all_guests()) == 2
    assert guests.get_guest_by_id(guest1).first_name == 'John'
    guests.update_guest(guest1, 'Bob', 'Doe', '555-555-5555', '123 Main St', 'Anytown', 'NY')
    assert guests.get_guest_by_id(guest1).first_name == 'Bob'
    guests.check_in(guest1)
    guests.check_in(guest1)
    assert guests.get_guest_by_id(guest1).visits == 1
    guests.delete_guest(guest1)
    assert len(guests.get_all_guests()) == 1
    assert guests.get_guest_by_id(guest2).first_name == 'Colin'