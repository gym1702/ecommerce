from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('El usuario debe tener un email')
        
        if not username:
            raise ValueError('El usuario debe tener un username')
        
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, first_name, last_name, username, email, password=None):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password, 
            first_name = first_name,
            last_name = last_name,
        )

        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user
    



class Account(AbstractBaseUser):
    #campos personalizados
    first_name = models.CharField('Nombres', max_length=50)
    last_name = models.CharField('Apellidos', max_length=50)
    username = models.CharField('Nombre de usuario', max_length=50, unique=True)    
    email = models.CharField('Email', max_length=100, unique=True)
    phone = models.CharField('Telefono', max_length=10)

    #campos por defecto para django
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active= models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    #valor por default para nombre de usuario
    USERNAME_FIELD = 'email'

    #campos requeridos
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    #Llama a Manager creado
    objects = MyAccountManager()


    class Meta:
        verbose_name_plural = 'Cuentas'


    def __str__(self):
        return self.email
    
    def full_name(self):
        return self.first_name + ' ' + self.last_name
    
    #Otorga permisos de administrador
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, add_label):
        return True



class UserProfile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE, verbose_name='Usuario')
    address_line_1 = models.CharField(max_length=100, blank=True, verbose_name='Direccion 1')
    address_line_2 = models.CharField(max_length=100, blank=True, verbose_name='Direccion 2')
    profile_picture = models.ImageField(upload_to='userprofile', blank=True, verbose_name='Imagen de perfil')
    city = models.CharField(max_length=50, blank=True, verbose_name='Ciudad')
    state = models.CharField(max_length=50, blank=True, verbose_name='Estado')
    country = models.CharField(max_length=50, blank=True, verbose_name='Pais')
    credit = models.BooleanField(default=False, verbose_name='Tiene credito')

    def __str__(self):
        return str(self.user.full_name)
    
    def full_address(self):
        return {self.address_line_1} + ', ' + {self.address_line_2}
    
    class Meta:
        verbose_name_plural = 'Perfil de usuario'