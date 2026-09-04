import scrapy
from datetime import datetime
from quotes_scraper.items import ProductItem
import re


class LaptopsSpider(scrapy.Spider):
    name = "laptops"
    allowed_domains = ["webscraper.io"]
    start_urls = ["https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops"]

    def parse(self, response):
        """Extrae información de laptops"""
        
        # Iterar sobre cada producto en la página
        for product in response.css("div.col-md-4.col-xl-4"):
            item = ProductItem()
            
            # Información básica
            item['source'] = 'laptops'
            item['product_name'] = product.css("a.title::attr(title)").get()
            
            # Precio - extraer solo texto sin espacios en blanco
            price_element = product.css("h4.price")
            price_text = price_element.css("::text").re_first(r'\$[\d,.]+')
            item['price_raw'] = price_text if price_text else ''
            item['currency'] = '$'
            # Limpiar precio: remover $ y convertir a float
            if price_text:
                price_clean = price_text.replace('$', '').replace(',', '').strip()
                try:
                    item['price'] = float(price_clean)
                except ValueError:
                    item['price'] = None
            else:
                item['price'] = None
            
            # Descripción técnica
            item['description'] = product.css("p.description::text").get()
            
            # Rating (estrellas)
            rating_text = product.css("p[data-rating]::attr(data-rating)").get()
            item['rating_raw'] = rating_text
            if rating_text:
                try:
                    item['rating'] = int(rating_text)
                except (ValueError, TypeError):
                    item['rating'] = None
            else:
                item['rating'] = None
            
            # Reviews
            reviews_text = product.css("p.review-count::text").get()
            item['review_count'] = self._extract_review_count(reviews_text)
            
            # Categoría
            item['category'] = 'Laptops'
            
            # Disponibilidad (no está explícita en laptops, asumimos disponible)
            item['availability'] = 'Available'
            
            # URLs
            product_link = product.css("a.title::attr(href)").get()
            item['product_url'] = response.urljoin(product_link) if product_link else None
            item['image_url'] = product.css("img.img-fluid::attr(src)").get()
            
            # Metadata
            item['scraped_at'] = datetime.now().isoformat()
            
            yield item
        
        # Paginación: seguir al siguiente enlace si existe
        next_page = response.css("ul.pagination li a[rel='next']::attr(href)").get()
        if next_page:
            yield response.follow(next_page, self.parse)
    
    def _extract_review_count(self, reviews_text):
        """Extrae el número de reviews del texto"""
        if not reviews_text:
            return 0
        
        # Buscar números en el texto "14 reviews"
        match = re.search(r'(\d+)', reviews_text)
        if match:
            return int(match.group(1))
        return 0
