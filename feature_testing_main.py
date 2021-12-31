from flask_server.model.restaurants import Restaurants
from flask_server.model.users import Users


if __name__ == '__main__':
    users = Users()
    users_rows = users.get_all_rows()

    restaurants = Restaurants()
    restaurant_data = [
        {
            "restaurant_name": "my_restaurant_22",
            "franchise_id": "street_name/street_number",
            "email": "my.restaurant@ggmail.com",
            "passwd": "password2",
            "city": "city",
            "provides_custom_meals": True,
            "provides_scheduled_delivery": False
        },
        {
            "restaurant_name": "my_restaurant_12",
            "franchise_id": "brazda_lui_novac/54",
            "email": "la.rocca@gmail.com",
            "passwd": "password2",
            "city": "city",
            "provides_custom_meals": True,
            "provides_scheduled_delivery": False
        }
    ]
    restaurants.upsert_row(rows=restaurant_data)
