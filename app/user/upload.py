def carnetdoc(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f'MAE/{instance.slug}/' + filename

def asignaciondoc(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f'MAE/{instance.slug}/' + filename