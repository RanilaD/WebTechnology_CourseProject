from WebTechnology_Course.forms import UserCreationForm


def breadcrumbs(request):
    parts = ['/'] + ' '.join(request.path.split('/')).split()
    if parts.__len__() == 1:
        return {
            "breadcrumbs": f"""<li><a href="/" class="active">/</a><span></span></li><li></li>"""
        }

    li = ""
    url_acc = "/"
    for i in range(parts.__len__() - 1):
        if i > 0:
            url_acc += parts[i] + "/"
        li += f"""<li><a href="{url_acc}" class="">{parts[i]}</a><span></span></li>"""
    url_acc += parts[parts.__len__() - 1]
    li += f"""<li><a href="{url_acc}" class="active">{parts[parts.__len__() - 1]}</a><span></span></li>"""
    li += """<li></li>"""
    return {
        "breadcrumbs": li
    }

def registration_form(request):
    return {
        'registration_form': UserCreationForm()
    }