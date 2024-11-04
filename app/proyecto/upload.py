def docModeloActa(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f'Proyecto/{instance.slug}/ModeloActa/'+ filename

def docDerechoPropietario(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f'Proyecto/{instance.slug}/DerechoPropietario/'+ filename


def docDeclaracionjurada(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f'Proyecto/{instance.slug}/Declaracionjurada/'+ filename