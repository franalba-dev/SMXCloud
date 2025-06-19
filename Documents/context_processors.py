from django.contrib.auth.models import Group

def is_not_alumno(request):
    if not request.user.is_authenticated:
        return {'is_not_alumno': False}
    return {'is_not_alumno': not request.user.groups.filter(name='Alumnos').exists()}