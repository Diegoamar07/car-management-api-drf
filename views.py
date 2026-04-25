from django.shortcuts import render, redirect
# importando a nossa classe(Tabela).
from cars.models import Car
from cars.forms import CarModelForm
from django.db.models import Q
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

# Importando FileInput para remover este campo da class CarsUpdateView(UpdateView)
from django.forms.widgets import FileInput

from rest_framework import viewsets
from cars.serializers import CarSerializer


class CarsListView(ListView):
    model = Car
    template_name = "cars.html"
    context_object_name = "cars"
    paginate_by = 4


    def get_queryset(self):
        cars = super().get_queryset().select_related("brand").order_by("model")
        search = self.request.GET.get("search")
        if search:
            cars = cars.filter(Q(model__icontains=search) | Q(brand__name__icontains=search))
            # cars = cars.filter(model__icontains=search) ## filtrando somente por model
        return cars


# Usando a mesma logica de captura da queryset do CarsListView, e enviando
# para a mesma chave 'lista' do template 'lista.html'
class CarsManagementListView(CarsListView):
    template_name = "lista.html"
    context_object_name = "lista"



## Abaixo segue CBV(view) basica que foi substituida pela CBV(ListView) acima.
# class CarsView(View):

#     def get(self, request):
#         busca = request.GET.get("search")
#         if busca:
#             cars = Car.objects.filter(
#                 Q(model__icontains=busca) | Q(brand__name__icontains=busca)
#             )
#         else:
#             cars = Car.objects.select_related("brand").order_by("model")
#         return render(request, "cars.html", {"cars": cars})


## Abaixo segue nossa FBV antiga.
# def cars_view(request):

#     cars = Car.objects.all().order_by("model")
#     search = request.GET.get("search")

#     if search:
#         cars = cars.filter(model__icontains=search)
           
#         ## consulta atraves MARCA.
#         # cars = cars.filter(brand__name__icontains=search)

#     return render(
    
#         request, 
#         "cars.html", 
#         {"cars": cars}    
#     )

##-------------------------------------------------------------------------------------


class CarsCreateView(CreateView):
    model = Car
    form_class = CarModelForm
    template_name = "new_car.html"
    # Mesmo que redirect("APELIDO") - 1 precisa IMPORTAR funcao reverse_lazy e dai pode passar o APELIDO da rota
    success_url = reverse_lazy("lista_car")
    
    # # Mesmo que redirect(ROTA EXPLICITA) - Aqui é so passar o nome da rota igual ao da path() começando com '/rota/'
    # success_url = "/lista_car/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        context["new_car_form"] = context["form"]
        return context

    ## para salvar dados extras na tabela como quem criou o cadastro, data_criacao, data_alteracao, status:ativo ou inativo. estes campos precisa JA ESTAR NO MODEL.
    # def form_valid(self, form):
    #     usuario = self.request.user 
    #     form.instance.created_by = usuario # ou direto: self.request.user
    #     return super().form_valid(form)

##---
# ## CBV(View) antigo. Troquei pela CBV(CreateView) acima.
# class NewCarView(View):
    
#     def get(self, request, id=None):
#         car = None
#         if id:
#             car = Car.objects.get(id=id)
#         # aqui estou carregando os dados para o cadastro do carro.
#         new_car_form = CarModelForm(instance=car)
#         return render(request, "new_car.html", {"new_car_form": new_car_form})


#     def post(self, request, id=None):
#         car = None
#         if id:
#             car = Car.objects.get(id=id) 
#         new_car_form = CarModelForm(request.POST, request.FILES, instance=car)
#         if new_car_form.is_valid():
#             new_car_form.save()
#             return redirect("cars_list")
#         return render(request, "new_car.html", {"new_car_form": new_car_form})

##---
# ## FBV antigo que trocamos para a CBV conforme acima.
# def new_car_view(request, id=None):

#     car = None
#     if id:
#         car = Car.objects.get(id=id)

#     if request.method == "POST":
#         new_car_form = CarModelForm(request.POST, request.FILES, instance=car)
        
#         if new_car_form.is_valid():
#             new_car_form.save()
#             return redirect("cars_list") 
    
#     else:
#         # esta linha faz carregar todos os dados da tabela COM os dados vindo da instance=car
#         new_car_form = CarModelForm(instance=car)

    
#     return render(request, "new_car.html", {"new_car_form": new_car_form})
            
##----------------------------------------------------------------------

class CarsUpdateView(UpdateView):
    model = Car
    template_name = "new_car.html"    
    form_class = CarModelForm
    success_url = reverse_lazy("cars_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
    
        # Capturando o dicionario com sua chave "form": objeto(estrutura HTML) e as regras do model
        form = context["form"]        
        context["new_car_form"] = form
        return context


##----------------------------------------------------------------------
"""
Abaixo tenho uma CBV(ListView) e outra CBV(view) para chamar o filtro da tela
do template lista.html. Estou trocando estas duas pela class CarsListView(ListView):
que ja esta funcioando para filtrar a rota 'cars/' Entao vou usar esta mesma view
de filtragem para a rota 'lista_car/'.


"""

# class CarroListView(ListView):

#     model = Car
#     template_name = "lista.html"
#     context_object_name = "lista"

#     def get_queryset(self):
#         queryset = super().get_queryset().select_related("brand").order_by("model")
#         search = self.request.GET.get("busca")
#         if search:
#             queryset = queryset.filter(
#                 Q(model__icontains=search) | Q(brand__name__icontains=search))
#         return queryset


# class ListaView(View):
    
#     def get(self, request):        
#         busca = request.GET.get("busca")
#         if busca:
#             lista = Car.objects.filter(
#                 Q(model__icontains=busca) | Q(brand__name__icontains=busca)
#                 ).select_related("brand").order_by("model")
#         else:
#             lista = Car.objects.select_related("brand").order_by("model")
#         return render(request, "lista.html", {"lista": lista})


## Listar os carros feito com FBV. Foi trocada pela CBV acima.
# def lista_view(request):

#     lista = []
#     busca = request.GET.get("busca")

#     if busca:
#         lista = Car.objects.filter(
#             Q(model__icontains=busca) | Q(brand__name__icontains=busca)
#             ).select_related("brand")
    

#     return render(request, "lista.html", {"lista": lista})

##---------------------------------------------------------------------------------

class CarsDeleteView(DeleteView):
    model = Car
    template_name = "exclui_car.html"
    success_url = reverse_lazy("cars_list")


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        car = context["object"]
        context["car_form"] = car
        return context


##-----
## Esta CBV(view) abaixo foi trocada pela CBV(DeleteView) acima.
# class ExcluirCarView(View):

#     def get(self, request, id=None):
#         car = None
#         if id:
#             car = Car.objects.get(id=id)
#         car_form = CarModelForm(instance=car)
#         return render(request, "exclui_car.html", {"car_form": car_form})

#     def post(self, request, id=None):
#         if id:
#             car = Car.objects.get(id=id)
#             car.delete()
#         return redirect("cars_list")


##---------------------------------------------------------------------------

## ABAIXO SEGUE A VIEW REFERENTE AO forms.Form
# def new_car_view(request):
#     # # verifica se o usuario e um superuser (acesse o /admin para ser)
#     # if not request.user.is_superuser:
#     #     return redirect("cars_list")
    

#     if request.method == "POST":
#         # iniciando objeto com dados do tipo texto e dos dados condigo binario FIles 
#         new_car_form = CarForm(request.POST, request.FILES)        
#         # Methodo 'is_valid' vai efetuar Try/exepts no objeto para verificar se cada
#         # campo do objeto corresponde ao seu valor passado corretamente. Retorna
#         # True ou False caso o campo for invalido.
#         if new_car_form.is_valid():
#             # Methodo save vamos subescrever para salvar os dados do nosso objeto
#             # dentro da tabela de carros. Methodo vai estar em forms.py
#             new_car_form.save()
            
#             # redirecionando o usuario para a tela lista de carros.
#             return redirect("cars_list")
    
#     else:    
#         # Retorna um objeto formulario que contem seus atributos. como .fields - .keys() - .values() ou .items()
#         # new_car_form.fields == retorna um dicionario onde chave e nome do campo e valor e o objeto charfield, textfield.
#         # podemos usar para acessar .keys() ou somente iterar for key in new_car_form.fields onde key ja vai ser o nome do campo ex: "brand"
#         # podemos usar atributo .values() pega direto o objeto de cada campo ou .items() pega tanto chave quanto valor.
#         # Importante: para acessarmos os atributos .keys() .values() ou .items() precisa ser apos usarmos o .fields que retorna o dicionario. ex: new_car_form.fields.values()
#         new_car_form = CarForm()


        # """ 
        # Abaixo eu criei testes de permisao de usuarios para liberar os campos ou nao
        # do cadastro de carros. depois iterei sobre o dicionario do objeto formulario
        # ao usar new_car_form.fields estou iterando sobre o dicionario onde a chave
        # vai ser o nome do campo ex: "brand" e o valor vai ser o objeto ex: charfield.
        # """
        # if request.user.is_superuser:
        #     campos_liberados = ["brand", "plate"]
        # else:
        #     campos_liberados = []

        # for chave, valor in new_car_form.fields.items():
        #     # if chave == "brand" or chave ==  "plate":
        #     ## ou podemos simpleficar o (if conforme abaixo)
        #     if chave in campos_liberados:
        #         valor.disabled = False
        #         valor.widget.attrs['style'] = "background-color: red;"
        #     else:
        #         valor.disabled = True

    # return render(
    #     request,
    #     "new_car.html",
    #     {"new_car_form": new_car_form},
    # )
##---------------------------------------------------------------------------------



##---------------------------------------------------------
    ## Imprimindo os dados do usuario
    # if request.method == "POST":
    #     print("DADOS RECEBIDOS COM SUCESSO")
    #     print("POST:", request.POST)
    #     print("FILES:", request.FILES)        

    # for i, (campo, valor) in enumerate(request.POST.items(), 1):
    #     print(f"Campo: {campo} - valor: {valor}")
    ##------------------------------------------------------------------

    # if request.method == "POST":
    #     meu_dict = request.POST.dict()
    #     meu_dict_completo = request.POST.lists()
    #     print(meu_dict)
    #     print(meu_dict_completo)
    ##------------------------------------------------------------------

## Abaixo pegamos todos os dados do primeiro argumento(request.POST) junto com
## os dados do segundo argumento de files(request.FILES) e depois iteramos sobre eles.

# todos_os_dados = {**new_car_form.data, **new_car_form.files}

# for campo, valor in todos_os_dados.items():
#     print(f"{campo}: {valor}")


"""
Resumo da estrutura de um "Sênior" em Django Templates:

Ação	         |     Rota (URL)	   |     Método HTTP            |	   View

Listar/Buscar      /produtos/	             GET	                       ListaView
Cadastrar          /produtos/novo/	         GET (ver) / POST (salvar)	   SalvarView (sem ID)
Editar             /produtos/editar/<id>/	 GET (ver) / POST (salvar)	   SalvarView (com ID)
Deletar            /produtos/deletar/<id>/	 POST	                       DeletarView

"""

##----------------------------------------------------------------------------------

class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer







