from django.db import models
from Users.models import User

class Subject(models.Model):
    name = models.CharField(
        verbose_name = 'Nombre de la asignatura',
        max_length = 75,
        null = False,
        blank = False,
        unique=True,
        )
    class Meta:
        verbose_name = 'Asignatura'
        verbose_name_plural = 'Asignaturas'

    def __str__(self):
        return self.name

class Document(models.Model):
    title = models.CharField(
        verbose_name = 'Título del documento',
        max_length = 150,
        null = False,
        blank = False,
        unique=True,
        )

    file = models.FileField(
        verbose_name = 'Archivo',
        upload_to='documents/',
        )

    upload_date = models.DateTimeField(
        verbose_name = 'Fecha de subida',
        auto_now_add=True,
        )
    
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name = 'Propietario'
        )      
    
    subject = models.ForeignKey(
        Subject,
        on_delete=models.SET_NULL,
        verbose_name= 'Asignatura',
        null = True,
        blank = True,
        unique=False,
        )

    class Meta:
        verbose_name = 'Documento'
        verbose_name_plural = 'Documentos'

    def __str__(self):
        return self.title
    
