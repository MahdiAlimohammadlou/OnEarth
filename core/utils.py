
def get_current_url(request):
    return request.scheme + "://" + request.get_host()

def get_full_url(obj, field_name, base_url):
    field = getattr(obj, field_name)
    if field != "":
        return base_url + field.url
    else:
        return ""
    
