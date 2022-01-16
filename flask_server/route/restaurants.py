from flask import Blueprint, request, Response, jsonify

from flask_server.model.products import Products
from flask_server.model.restaurants import Restaurants

restaurants_blueprint = Blueprint('restaurants_blueprint', __name__, url_prefix='/restaurants')
restaurants = Restaurants()
products = Products()


@restaurants_blueprint.route('/upsert-from-code', methods=['POST'])
def upsert_from_code():
    """
    route that adds body of the request to the db as rows; request body = list of dicts
    :return: 200 for good request / 400 for empty rows list
    """
    data = request.json
    if len(data) == 0:
        return Response('No data to be upserted was found in the body of the request', status=400)

    receipt = restaurants.upsert_row(rows=data)
    return Response(f'Successfully upserted:\n{receipt}', status=200)


@restaurants_blueprint.route('/upsert-from-file', methods=['POST'])
def upsert_from_file():
    """
    upserts content of a file found on the local system; request body must be a dict that contains the key 'filePath'
    :return: 200 for good request
    """
    file_path = request.json.get('filePath')
    receipt = restaurants.batch_upsert(file_path)

    return Response(f'Succesfully upserted: {receipt}\n'
                    f'form {file_path}', status=200)


@restaurants_blueprint.route('/delete', methods=['DELETE'])
def delete():
    """
    request body will be a dict with 2 keys:
         - 'identifierType': value with witch the rows will be uniquely identified
         (id / email / franchise_id)
         - 'rows': list of column values for the rows that will be deleted
    :return: 200 for good request / 400 for invalid identifier or empty rows list
    """
    identifier = request.json.get('identifierType')
    rows = request.json.get('rows')

    if identifier not in {'id', 'email', 'franchise_id'} or len(rows) == 0:
        return Response('Invalid parameters', status=400)

    receipt = restaurants.delete_rows(rows_to_delete=rows, identifier_type=identifier)

    if len(receipt) == 0:
        return Response("Rows don't exist", status=400)
    return Response(f'Successfully deleted:\n{receipt}', status=200)


@restaurants_blueprint.route('/get-menu', methods=['POST'])
def get_restaurant_meals():
    return jsonify(products.get_restaurant_products(request.json.get('restaurant_name'), 'meal'))


@restaurants_blueprint.route('/get-products', methods=['POST'])
def get_restaurant_products_for_custom_feals():
    result_products = []
    restaurant_name = request.json.get('restaurant_name')

    protein_products = products.get_restaurant_products(restaurant_name, 'protein')
    if len(protein_products):
        result_products.append(*protein_products)

    carbs_products = products.get_restaurant_products(restaurant_name, 'carbs')
    if len(carbs_products):
        result_products.append(*carbs_products)

    fat_products = products.get_restaurant_products(restaurant_name, 'fat')
    if len(fat_products):
        result_products.append(*fat_products)

    if not len(result_products):
        return Response(f"No products for restaurant '{restaurant_name}'")

    return jsonify(result_products)

