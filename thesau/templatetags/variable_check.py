from django.template.defaulttags import register

@register.filter
def exist(var):
    try:
        var
    except NameError:
        return False
    else:
        if var is None:
            return False
        else:
            return True