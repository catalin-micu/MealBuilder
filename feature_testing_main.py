from flask_server.model.restaurants import Restaurants
from flask_server.model.users import Users


if __name__ == '__main__':
    users = Users()
    users_rows = users.get_all_rows()

    restaurant_data = [
        {
            "restaurant_name": "saucy_stakes",
            "franchise_id": "street_name/street_number",
            "email": "my.restaurant@ggmail.com",
            "passwd": "password2",
            "city": "city",
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
        }
    ]
    # r2 = Restaurants(**restaurant_data[1])
    # b=2

    restaurants = Restaurants()
    restaurants.upsert_row(rows=restaurant_data)
    # restaurants.batch_upsert('./data_files/restaurants.json')
