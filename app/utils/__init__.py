
def analyze_keys(keys, request):
    
    for key in request.keys():
        if not key in keys:
            raise KeyError(f"Must contain the keys: {keys}")

