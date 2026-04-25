# Import the serializers module from the framework
from rest_framework import serializers
# Import the car model
from cars.models import Car


class CarSerializer(serializers.ModelSerializer):    

    brand = serializers.SlugRelatedField(
            read_only=True,
            slug_field='name' 
    )

    discounted_value = serializers.SerializerMethodField()

    class Meta:
        model = Car
        fields = "__all__"        

    def get_discounted_value(self, obj):
        if obj.value:
            return obj.value * 0.10
        return 0


"""
Explicando alguns detalhes sobre a class serializer.
-----------------------------------------------------

    # criando novo campo para o JSON. Precisa ficar dentro da classe principal.
    # ao usar a class SerializerMethodField(), Esta class e boa para criar campos
    # que vao precisar de calculos antes de ser criado o arquivo JSON.
    discounted_value = serializers.SerializerMethodField()

    # O parametro 'obj' vai receber apenas uma instancia do model Car a cada volta do loop 
    # se tiver 10 objetos o ciclo se repete por 10x.
    def get_discounted_value(self, obj):
    
"""



