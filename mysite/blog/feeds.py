from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from .models import Post

# Subskrypcja bloga, informacja o nowych wiadomościach

class LatestPostsFeed(Feed):
# Podklasa Feed
    title = 'Mój blog'
    link = '/blog/'
    description = 'Nowe posty na moim blogu.'
    
    def items(self):
        return Post.published.all()[:5]
        # Obiekty które mają być umieszczone w wdiadomości
    

    def item_title(self, item):
        return item.title
        # Pobiera tytł obiektu
    

    def item_description(self, item):
        return truncatewords(item.body, 30)
        # pobiera zawrtość obiektu