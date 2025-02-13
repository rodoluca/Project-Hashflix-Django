from django.shortcuts import render, redirect, reverse
from .models import Filme, Usuario
from .forms import CriarContaForm, FormHomepage
from django.views.generic import TemplateView, ListView, DetailView, FormView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


# Create your views here.


class Homepage(FormView): # CBV
    template_name = 'homepage.html'
    form_class = FormHomepage

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # redireciona para a homefilmes
            return redirect('filme:homefilmes')
        else:
            # redireciona para a homepage
            return super().get(request, *args, **kwargs)

    def get_success_url(self):
        email = self.request.POST.get('email')
        usuarios = Usuario.objects.filter(email=email)
        if usuarios:
            return reverse('filme:login')
        else:
            return reverse('filme:criarconta')

        # toda url tem que ter um success_url
        return reverse('filme:login')


class Homefilmes(LoginRequiredMixin, ListView):
    template_name = 'homefilmes.html'
    model = Filme
    # object_list -> lista de itens do modelo


class DetalhesFilme(LoginRequiredMixin, DetailView):
    template_name = 'detalhesfilme.html'
    model = Filme
    # object -> 1 item do nosso modelo

    def get(self, request, *args, **kwargs):
        #descobrir qual o filme esta sendo acessado
        filme = self.get_object()
        # somar 1 nas visualizacoes do filme
        filme.visualizacoes += 1
        #salvar
        filme.save()

        # adicionar de maneira automatica os filmes vistos na detailpage
        usuario = request.user
        usuario.filmes_vistos.add(filme)

        return super(DetalhesFilme, self).get(request, *args, **kwargs)
        # retorna o proprio valor da função padrao de get, redirecionando o usuario para a url final

    def get_context_data(self, **kwargs): #criando a lista de filmes q sera exibida na pagina de detail do filme
        context = super(DetalhesFilme, self).get_context_data(**kwargs) #executar a funcao da super classe para nao perder as funcoes iniciais setadas
        #filtrar a minha tabela filmes pegando os filmes cuja categoria é igual a categoria do filme da pagina (object)
        #self.get_object()
        filmes_relacionados = self.model.objects.filter(categoria=self.get_object().categoria)[0:5]
        context['filmes_relacionados'] = filmes_relacionados
        return context


class PesquisaFilme(LoginRequiredMixin, ListView):
    template_name = 'pesquisafilme.html'
    model = Filme

    #view para fazer a barra de pesquisa funcionar
    #editando o object_list
    def get_queryset(self):
        termo_pesquisa = self.request.GET.get('query')
        if termo_pesquisa:
            object_list = self.model.objects.filter(titulo__icontains=termo_pesquisa)
            return object_list
        else:
            return None


class PaginaPerfil(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'editarperfil.html'
    model = Usuario
    fields = ['first_name', 'last_name', 'email'] # mesmos nomes das colunas do banco de dados

    def test_func(self): # garante q os usuarios nao tenham acesso ao perfil de outros usuarios alterando o numero do perfil na URL
        user = self.get_object()
        return self.request.user == user

    def get_success_url(self):
        return reverse('filme:homefilmes')


class CriarConta(FormView):
    template_name = 'criarconta.html'
    form_class = CriarContaForm

    def form_valid(self, form):
        # sempre que editar o banco de dados, deve se salvar o formulario
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        # toda url tem que ter um success_url
        return reverse('filme:login')



# def homepage(request):
#     return render(request, 'homepage.html')

# url - view - html
# def homefilmes(request):
#     context = {}
#     lista_filmes = Filme.objects.all()
#     context['lista_filmes'] = lista_filmes
#     return render(request, 'homefilmes.html', context)
