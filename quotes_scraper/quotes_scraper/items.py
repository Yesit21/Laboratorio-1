import scrapy

class QuoteItem(scrapy.Item):
    text = scrapy.Field()
    author = scrapy.Field()
    tags = scrapy.Field()
    author_born_date = scrapy.Field()
    author_born_location = scrapy.Field()
    author_description = scrapy.Field()
    url = scrapy.Field()


class ProductItem(scrapy.Item):
    """Item unificado para productos del catálogo (libros y laptops)"""
    # Identificación
    source = scrapy.Field()  # 'books' o 'laptops'
    product_name = scrapy.Field()
    
    # Precio
    price = scrapy.Field()
    price_raw = scrapy.Field()  # Precio original con símbolo
    currency = scrapy.Field()  # '£' o '$'
    
    # Valoración
    rating = scrapy.Field()  # Número 1-5
    rating_raw = scrapy.Field()  # Rating original (CSS class o texto)
    review_count = scrapy.Field()  # Número de reviews
    
    # Información del producto
    description = scrapy.Field()
    category = scrapy.Field()
    availability = scrapy.Field()
    
    # URLs
    product_url = scrapy.Field()
    image_url = scrapy.Field()
    
    # Metadata
    scraped_at = scrapy.Field()  # Timestamp de extracción
