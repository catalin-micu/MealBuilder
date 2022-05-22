ACCEPTED_ACTIVITY_LEVEL_VALUES = {
    'sedentary': 1.2,
    'light': 1.375,
    'moderate': 1.55,
    'very': 1.725,
    'extra': 1.9
}


def transform_addresses_to_iterable(addresses: str) -> list:
    addr_list = []
    if not addresses:
        return addr_list

    var = addresses.split('//')
    for item in var:
        address, city = item.split('-')
        addr_list.append({'address': address, 'city': city})

    return addr_list


def calculate_caloric_needs_per_day(bmr: int, activity_level: str) -> int:
    if activity_level not in list(ACCEPTED_ACTIVITY_LEVEL_VALUES.keys()):
        raise ValueError(f"Invalid activity level '{activity_level}'; please choose from:"
                         f" {ACCEPTED_ACTIVITY_LEVEL_VALUES}")

    return int(bmr * ACCEPTED_ACTIVITY_LEVEL_VALUES.get(activity_level))


def calculate_bmr(weight_in_kg: float, height_in_cm: float, age_in_years: int, gender: str) -> float:
    if gender not in {'male', 'female'}:
        raise ValueError(f"Invalid gender, provided value is '{gender}'")

    if gender == 'male':
        return 66.5 + (13.75 * weight_in_kg) + (5.003 * height_in_cm) - (6.75 * age_in_years)
    else:
        return 655.1 + (9.563 * weight_in_kg) + (1.85 * height_in_cm) - (4.676 * age_in_years)
