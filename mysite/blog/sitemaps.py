from django.contrib.sitemaps import Sitemap
from .models import Post

# Przekazanie wyszukiwarkom stron internetowych

class PostSitemap(Sitemap):
# Dziedziczymy po wbudowanym module
    changefreq = 'weekly'
    # Częstowtliwość zmiany posta
    priority = 0.9
    # Trafnośc w witrynie (max 1)

    def items(self):
        return Post.published.all()
        # Kolekcja obiektów które mają znaleść się w mapie wirtyn
            
    def lastmod(self, obj):
        return obj.publish
    # Pobier każdy items() i dodaje dane ostaniej modyfikacji