from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from Documents.views import home, list_documents, upload_document, delete_document, update_document, list_subjects, create_subject, delete_subject, update_subject
from Users.views import list_users, create_user, delete_user, update_user, no_autorizado


urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    
    path('lista-de-documentos/', list_documents),
    path('subir-documento/', upload_document),
    path('eliminar-documento/<int:pk>', delete_document),
    path('editar-documento/<int:pk>', update_document),

    path('lista-de-asignaturas/', list_subjects, name='lista-asignaturas'),
    path('crear-asignatura/', create_subject),
    path('eliminar-asignatura/<int:pk>', delete_subject),
    path('editar-asignatura/<int:pk>', update_subject),
    
    path('lista-de-usuarios/', list_users),
    path('crear-usuario/', create_user),
    path('eliminar-usuario/<int:pk>', delete_user),
    path('editar-usuario/<int:pk>', update_user),

    path('users/', include('Users.urls')),
    path('users/', include('django.contrib.auth.urls')),
    path('no-autorizado/', no_autorizado),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)