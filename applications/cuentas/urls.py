from django.urls import path

from . import views

app_name = 'cuentas_app'

urlpatterns = [
    path('registro/', views.registro, name="registro"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('passwordOlvidado/', views.passwordOlvidado, name="passwordOlvidado"),
    path('resetpassword_validate/<uidb64>/<token>', views.resetpassword_validate, name="resetpassword_validate"),
    path('resetPassword/', views.resetPassword, name="resetPassword"),
    path('activar/<uidb64>/<token>/', views.activar, name="activar"),

]
