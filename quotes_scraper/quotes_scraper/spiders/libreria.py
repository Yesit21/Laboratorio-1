import scrapy
from datetime import datetime
from quotes_scraper.items import ProductItem
import re


class LibreriaSpider(scrapy.Spider):
    name = "libreria"
    allowed_domains = ["books.toscrape.com"]
    
    # Todas las categorías para un catálogo completo
    start_urls = [
        "https://books.toscrape.com/",
    ]

    def parse(self, response):
        """Extrae información de libros"""
        
        # Recorrer los libros de la página
        for book in response.css("article.product_pod"):
            item = ProductItem()
            
            # Información básica
            item['source'] = 'books'
            item['product_name'] = book.css("h3 a::attr(title)").get()
            
            # Precio
            price_raw = book.css("p.price_color::text").get()
            item['price_raw'] = price_raw
            item['currency'] = '£'
            # Limpiar precio: remover £ y convertir a float
            if price_raw:
                price_clean = price_raw.strip().replace('£', '').replace(',', '')
                try:
                    item['price'] = float(price_clean)
                except ValueError:
                    item['price'] = None
            else:
                item['price'] = None
            
            # Rating (convertir clase CSS a número)
            rating_class = book.css("p.star-rating::attr(class)").get()
            item['rating_raw'] = rating_class
            item['rating'] = self._extract_rating(rating_class)
            
            # Reviews (no disponible en listado)
            item['review_count'] = 0
            
            # Disponibilidad
            availability_list = book.css("p.instock.availability::text").getall()
            # Limpiar espacios en blanco
            availability_clean = ' '.join([text.strip() for text in availability_list if text.strip()])
            item['availability'] = availability_clean or 'Unknown'
            
            # Categoría (extraer del breadcrumb)
            breadcrumbs = response.css("ul.breadcrumb li a::text").getall()
            item['category'] = breadcrumbs[-1] if breadcrumbs else 'Books'
            
            # Descripción (no disponible en listado)
            item['description'] = None
            
            # URLs
            product_link = book.css("h3 a::attr(href)").get()
            item['product_url'] = response.urljoin(product_link) if product_link else None
            item['image_url'] = response.urljoin(book.css("img::attr(src)").get())
            
            # Metadata
            item['scraped_at'] = datetime.now().isoformat()
            
            yield item

        # Seguir a la siguiente página
        next_page = response.css("li.next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, self.parse)
    
    def _extract_rating(self, rating_class):
        """Convierte clase CSS de rating a número"""
        if not rating_class:
            return None
        
        # Mapeo de palabras a números
        rating_map = {
            'One': 1,
            'Two': 2,
            'Three': 3,
            'Four': 4,
            'Five': 5
        }
        
        # Buscar la palabra en la clase
        for word, number in rating_map.items():
            if word in rating_class:
                return number
        
        return None

