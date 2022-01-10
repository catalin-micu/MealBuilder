update_user_data = {
        "passwd" : "password_update",
        "full_name" : "name_update",
        "card_nb" : "1",
        "card_holder_name" : "value-update",
        "card_expiry" : "12/29",
        "cvv" : 124,
        "preferred_addresses" : "fratiei 2",
    }

insert_user_data = {
        "email" : "insert@gmail.com",
        "passwd" : "password2",
        "full_name" : "cocostarcul",
        "card_nb" : "1234",
        "card_holder_name" : "coco-starcul",
        "card_expiry" : "1/1",
        "cvv" : 123,
        "preferred_addresses" : "ion ratiu 109",
        "phone_number": "07n-am_cartela"
    }

upsert_restaurant_data = [
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