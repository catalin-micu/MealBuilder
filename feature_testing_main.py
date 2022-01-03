from flask_server.model.restaurants import Restaurants
from flask_server.model.users import Users


if __name__ == '__main__':
    users = Users()
    users_rows = users.get_all_rows()

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
        }
    ]
    # r2 = Restaurants(**restaurant_data[1])
    # b=2

    restaurants = Restaurants()
    # restaurants.upsert_row(rows=restaurant_data)
    # result = restaurants.batch_upsert('./data_files/restaurants.json')
    b = restaurants.delete_rows(['14', '15'], identifier_type='id')
    a=2
