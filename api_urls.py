from django.urls import path, include
from rest_framework import routers
from .views import CarViewSet


# Router(objeto) cria automaticamente todas rotas de um CRUD
# Creating the object(router) - allows urls for (CRUD)  
router = routers.DefaultRouter()
router.register('cars', CarViewSet, basename='cars')


urlpatterns = [
    # route for api(JSON)
    path('', include(router.urls)),

]
