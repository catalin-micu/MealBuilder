def transform_addresses_to_iterable(addresses: str) -> list:
    addr_list = []
    var = addresses.split('//')
    for item in var:
        address, city = item.split('-')
        addr_list.append({'address': address, 'city': city})
    return addr_list