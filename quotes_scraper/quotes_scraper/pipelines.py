# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
import csv
import os


class QuotesScraperPipeline:
    def process_item(self, item, spider):
        return item


class JsonWriterPipeline:
    """Pipeline para guardar items en archivos JSON"""
    
    def open_spider(self, spider):
        """Se ejecuta cuando el spider se abre"""
        filename = f'{spider.name}_data.json'
        self.file = open(filename, 'w', encoding='utf-8')
        self.file.write('[\n')
        self.item_count = 0
        
    def close_spider(self, spider):
        """Se ejecuta cuando el spider se cierra"""
        self.file.write('\n]')
        self.file.close()
    
    def process_item(self, item, spider):
        """Procesa cada item y lo guarda en JSON"""
        adapter = ItemAdapter(item)
        
        # Agregar coma si no es el primer item
        if self.item_count > 0:
            self.file.write(',\n')
        
        # Escribir item como JSON
        line = json.dumps(dict(adapter), ensure_ascii=False, indent=2)
        self.file.write(line)
        self.item_count += 1
        
        return item


class CsvWriterPipeline:
    """Pipeline para guardar items en archivos CSV"""
    
    def open_spider(self, spider):
        """Se ejecuta cuando el spider se abre"""
        filename = f'{spider.name}_data.csv'
        self.file = open(filename, 'w', newline='', encoding='utf-8-sig')
        self.writer = None
        self.fieldnames = None
        
    def close_spider(self, spider):
        """Se ejecuta cuando el spider se cierra"""
        self.file.close()
    
    def process_item(self, item, spider):
        """Procesa cada item y lo guarda en CSV"""
        adapter = ItemAdapter(item)
        
        # Crear writer con los campos del primer item
        if self.writer is None:
            self.fieldnames = list(adapter.keys())
            self.writer = csv.DictWriter(
                self.file, 
                fieldnames=self.fieldnames
            )
            self.writer.writeheader()
        
        # Escribir item como fila CSV
        self.writer.writerow(dict(adapter))
        
        return item
