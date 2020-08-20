# Kolejnośc "imortów" zgodnie z ich blokami niżej poza  django.shortcuts które odnosi sie do wileu bloków
from django.core.mail import send_mail

from django.views.generic import ListView

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Paginator numerowanie strony
from taggit.models import Tag
# Tag otaguj
from django.db.models import Count
# Dodatkowe funkce agrgacji

from django.shortcuts import render, get_object_or_404
# Render wyrenderuj

from .models import Post, Comment

from django.contrib.postgres.search import SearchVector
from .forms import EmailPostForm, CommentForm, SearchForm


def post_search(request):
# Użyj jeżeli wymagany
    form = SearchForm()
    # forms.py
    query = None
    # definiujemy query przed użyciem
    results = []
    if 'query' in request.GET:
    # Jeżli wystąpi żądanie
        form = SearchForm(request.GET)
        # Przeszukaj baze
        if form.is_valid():
            query = form.cleaned_data['query']
            # Pobierz query
            results = Post.objects.annotate(
                search=SearchVector('title', 'body'),
                ).filter(search=query)
    return render(request,
        'blog/post/search.html',
        {'form': form,
        'query': query,
        'results': results})


# Definicja widoku wysałania posta przez e-mail
def post_share(request, post_id):
    # Pobranie posta na podstawie jego identyfikatora.
    post = get_object_or_404(Post, id=post_id,
                             status='published')
    #metoda get wczytuje bazowy widok
    sent = False
    # Zmienna pokazujaca czy udalo sie wysłac maila
    if request.method == 'POST':
        # Użytkownik wysyła formularz
        form = EmailPostForm(request.POST)
        # Pobramie danych
        if form.is_valid():
        # Weryfikacja pól formularza zakończyła się powodzeniem...
            cd = form.cleaned_data
            # Pobranie danych
            post_url = request.build_absolute_url(post.get_absolute_url())
            # Generowanie adresu URL Posta
            subject = '{} ({}) zachęca do przeczytania "{}"'.format(cd['name'],cd['email'], post.title)
            message = 'Przeczytaj post "{}" na stronie {}\n\n Komentarz dodany przez {}: {}'.format(post.title, post_url, cd['name'], cd['comments'])
            # Dane które automatycznie sa dopisywane do e-maila
            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            # Wyślij
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})

# Widok bloga dla użytkowników
class PostListView(ListView):
    queryset = Post.published.all()
    # Pobierz wszystkie obiekty
    context_object_name = 'posts'
    # Ustawiamy wymgany atrybut odpowiedzi
    paginate_by = 2
    # Ilość obiektów
    template_name = 'blog/post/list.html'
    # Adres URL *Ten jest domyślny

# Widok bloga dla użytkowników z opcjonalnym polem tag
def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    # Wczytaj publiczne posty
    tag = None
    if tag_slug:
        # Jeżeli pole tag_slug nie jest puste
        tag = get_object_or_404(Tag, slug=tag_slug)
        # Budujemy kolecje QuerySet
        object_list = object_list.filter(tags__in=[tag])
        # Wyświetl żądane elementy
    paginator = Paginator(object_list, 3)
    # Trzy posty na każdej stronie
    page = request.GET.get('page')
    # Otrzymaj strone
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # Jeżeli zmienna page nie jest liczbą całkowitą,
        # wówczas pobierana jest pierwsza strona wyników.
        posts = paginator.page(1)
    except EmptyPage:
        # Jeżeli zmienna page ma wartość większą niż numer ostatniej strony
        # wyników, wtedy pobierana jest ostatnia strona wyników.
        posts = paginator.page(paginator.num_pages)
    return render(request,
                  'blog/post/list.html',
                  {'page': page,
                   'posts': posts,
                   'tag':tag})

# Szczegóły posta
def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)

    comments = post.comments.filter(active=True)
    # Lista aktywnych komentarzy dla danego posta.
    if request.method == 'POST':
        # Komentarz został opublikowany.
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            # Utworzenie obiektu Comment, ale jeszcze nie zapisujemy go w bazie danych.
            new_comment.post = post
            # Przypisanie komentarza do bieżącego posta.
            new_comment.save()
            # Zapisanie komentarza w bazie danych.
    else:
        comment_form = CommentForm()

    post_tags_ids = post.tags.values_list('id', flat=True)
    # Pobieramy tagi danego posta
    # flat=true oznacza ze otrzymujemy liste jednorodną
    similar_posts = Post.published.filter(tags__in=post_tags_ids)\
        .exclude(id=post.id)
    # Pobieramy wszystkie posty z przynajmniej jednym fspólnym tagiem poza bieżącym postem
    similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
                        .order_by('-same_tags','-publish')[:4]
    # Dodaje adnotacje do obiektów nastepnie je sortuje i skraca
    # Count licznik obiektów

    return render(request,
                  'blog/post/detail.html',
                  {'post': post,
                   'comments': comments,
                   'comment_form': comment_form,
                   'similar_posts': similar_posts})

