from datetime import datetime
from data_files.data import insert_user_data
from flask_server import utils
from flask_server.model.products import Products
from flask_server.model.progress import Progress
from flask_server.model.restaurants import Restaurants
from flask_server.model.sessions import Sessions
from flask_server.model.users import Users
from flask_server.googlemaps_api import get_nearby_restaurants_from_gmaps

if __name__ == '__main__':
    users = Users()
    """upsert from file"""
    # users.batch_upsert_from_file('./data_files/users.json')
    """delete user"""
    # users.delete_rows(rows_to_delete=['0712345679'], identifier_type='phone_number')
    """insert user"""
    # a = users.insert_user(user_data=insert_user_data)
    """update user"""
    # a = users.update_user('5', 'user_id', {'last_login': datetime.now()})
    """check user credentials"""
    # a = users.get_user_data_from_email('bornac@hotmail.com')

    """created table object from dict"""
    # r2 = Restaurants(**restaurant_data[1])

    restaurants = Restaurants()
    """upserting from code"""
    # restaurants.upsert_row(rows=restaurant_data)

    """upserting from file"""
    # restaurants.batch_upsert('./data_files/restaurants.json')

    """deleting and getting the receipt"""
    # b = restaurants.delete_rows(['1'], identifier_type='id')

    # sess = Sessions()
    """delete session"""
    # a = sess.delete_session(2)
    """rests in city"""
    # a = restaurants.get_restaurants_in_given_city('city')

    products = Products()
    # a = products.upsert_products_from_file('./data_files/products.json')
    # a = products.get_restaurant_products('Uncle John', 'meal')

    a = utils.calculate_caloric_needs_per_day(bmr=int(utils.calculate_bmr(weight_in_kg=80.3,
                                                                          height_in_cm=179,
                                                                          age_in_years=23,
                                                                          gender='male')),
                                              activity_level='moderate')
    progress = Progress()
    a = progress.get_progress(email='catalinmicu98@gmail.com')
    print(get_nearby_restaurants_from_gmaps('Tineretului 17, Chiajna, Ilfov'))
    b=2
