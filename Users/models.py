from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Correo electrónico es un campo obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('El Superuser debe ser staff (is_staff=True).')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('El Superuser debe ser superusario. (is_superuser=True).')

        return self.create_user(email, password, **extra_fields)

    def get_by_natural_key(self, email):
        return self.get(**{self.model.USERNAME_FIELD: email})

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='Correo electrónico',
        max_length=75,
        unique=True,
        blank=False,
        null=False,
    )
    first_name = models.CharField(
        verbose_name='Nombre',
        max_length=50,
        unique=False,
        blank=False,
        null=False,
    )
    last_names = models.CharField(
        verbose_name='Apellidos',
        max_length=50,
        unique=False,
        blank=False,
        null=False,
    )
    birthday = models.DateField(
        verbose_name='Fecha de nacimiento',
        unique=False,
        blank=True,
        null=True,
    )

    class GenderChoices(models.TextChoices):
        Masculino = 'Masculino'
        Femenino = 'Femenino'

    gender = models.CharField(
        verbose_name="Género",
        choices=GenderChoices.choices,
        blank=True,
        null=True,
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_names']

    objects = UserManager()

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return f'{self.first_name} {self.last_names}'

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    # @property
    # def is_staff(self):
    #     return self.is_staff



    #bio,  gender
