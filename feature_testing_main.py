from flask_server.model.restaurants import Restaurants
from flask_server.model.users import Users


if __name__ == '__main__':
    users = Users()
    """upsert from file"""
    # users.batch_upsert_from_file('./data_files/users.json')
    """delete user"""
    # users.delete_rows(rows_to_delete=['0712345679'], identifier_type='phone_number')
    user_data = {
        "email" : "value2",
        "passwd" : "password2",
        "full_name" : "insert_user_test2",
        "card_nb" : "123432142114",
        "card_holder_name" : "Jane-Doe22222",
        "card_expiry" : "07/26",
        "cvv" : 123,
        "preferred_addresses" : "fratiei 3",
        "phone_number": "jamaica2"
    }
    a = users.insert_user(user_data)

    restaurant_data = [
        {
            "restaurant_name": "value",
            "franchise_id": "value",
            "email": "value",
            "passwd": "value",
            "city": "value",
            "provides_custom_meals": True,
            "provides_scheduled_delivery": False
        },
        {
            "restaurant_name": "from_base_table",
            "franchise_id": "brazda_lui_novac/54",
            "email": "la.rocca@gmail.com",
            "passwd": "password2",
            "city": "city",
            "provides_custom_meals": True,
            "provides_scheduled_delivery": False
        },
        {
            "restaurant_name": "lovi-te-ar foamea",
            "franchise_id": "sergent/86",
            "email": "email@email.com",
            "passwd": "password2",
            "city": "chiajna",
            "provides_custom_meals": True,
            "provides_scheduled_delivery": False
        }
    ]
    """created table object from dict"""
    # r2 = Restaurants(**restaurant_data[1])
    # b=2

    # restaurants = Restaurants()

    """upserting from code"""
    # restaurants.upsert_row(rows=restaurant_data)

    """upserting from file"""
    # restaurants.batch_upsert('./data_files/restaurants.json')

    """deleting and getting the receipt"""
    # b = restaurants.delete_rows(['1'], identifier_type='id')
