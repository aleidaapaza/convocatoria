def convocatoria_doc(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f'Convocatoria/{instance.slug}/'+ filename