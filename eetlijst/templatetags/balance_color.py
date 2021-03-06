from django.template.defaulttags import register


# set background color based on current balance
@register.filter
def bal_color(balance):

    pos = [110, 185, 110]
    neg = [185, 110, 110]
    alpha = '0.85'

    if balance >= 0:
        if balance > 30:
            rgba_color = str(pos[0]) + ', ' + str(pos[1]) + ', ' + str(pos[2]) + ', ' + alpha
        else:
            rgba_color = str(int(255 - balance*(255-pos[0])/30)) + ', ' + str(int(255 - balance*(255-pos[1])/30)) + ', ' + str(int(255 - balance*(255-pos[2])/30)) + ', ' + alpha

    else:
        if balance < -30:
            rgba_color = str(neg[0]) + ', ' + str(neg[1]) + ', ' + str(neg[2]) + ', ' + alpha
        else:
            rgba_color = str(int(255 + balance*(255-neg[0])/30)) + ', ' + str(int(255 + balance*(255-neg[1])/30)) + ', ' + str(int(255 + balance*(255-neg[2])/30)) + ', ' + alpha

    return rgba_color