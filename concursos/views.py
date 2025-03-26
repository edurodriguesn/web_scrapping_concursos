from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from concursos.models import Concurso

def lista_concursos(request):
    concursos = Concurso.objects.all().order_by('-data_cadastro')
    return render(request, 'concursos/resultados.html', {'concursos': concursos})