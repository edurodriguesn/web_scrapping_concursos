from django.db import models

# concursos/models.py
from django.db import models
from django.conf import settings

class Concurso(models.Model):
    titulo = models.CharField(max_length=200)
    link = models.URLField(unique=True)
    estado = models.CharField(max_length=20)
    data_concurso = models.DateField()
    descricao = models.TextField()
    data_cadastro = models.DateTimeField(auto_now_add=True)
    novo = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-data_cadastro']
    
    def __str__(self):
        return self.titulo