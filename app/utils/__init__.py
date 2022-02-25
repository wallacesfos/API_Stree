
def analyze_keys(keys, request):
    
    for key in request.keys():
        if not key in keys:
            raise KeyError(f"Must contain the keys: {keys}")

    try:

        for key in keys:
            request[key]

    except KeyError:
        raise KeyError(f"Must contain the keys: {keys}")




