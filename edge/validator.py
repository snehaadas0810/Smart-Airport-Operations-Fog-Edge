def validate_message(data):

    if not isinstance(data, dict):
        return False

    if "sensor_id" not in data:
        return False

    if "sensor_type" not in data:
        return False

    return True