from email.policy import default

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

# Create your models here.

LISTA_CATEGORIAS = (
    ('ANALISES', 'Análises'),
    ('PROGRAMACAO', 'Programação'),
    ('APRESENTACAO', 'Apresentação'),
    ('OUTROS', 'Outros'),
)

# criar o filme
class Filme(models.Model):

    titulo = models.CharField(max_length=100)
    thumb = models.ImageField(upload_to='thumb_filmes')
    descricao = models.TextField(max_length=1000)
    categoria = models.CharField(max_length=15, choices=LISTA_CATEGORIAS)
    visualizacoes = models.IntegerField(default=0)
    data_criacao = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.titulo
#     garante que seja mostrado o titulo do filme na pagina admin


# criar os episodios
class Episodio(models.Model):
    filme =  models.ForeignKey("Filme",related_name="episodios", on_delete=models.CASCADE)# chave extrangeira de Filme
    titulo = models.CharField(max_length=100)                                                 # o related_name "cria" na tabela Filme um "campo" chamado episódios, onde possui todos os episódios relacionados a aquele filme
    video = models.URLField()

    def __str__(self):
        return self.filme.titulo + " - " + self.titulo


# criar o usuario --- Já vem criados no django
class Usuario(AbstractUser):
    filmes_vistos = models.ManyToManyField("Filme")


