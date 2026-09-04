#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import os
import sys
from datetime import datetime
from transform_data import DataTransformer
from database_schema import DatabaseManager


class ETLPipeline:
    
    def __init__(self):
        self.start_time = None
        self.end_time = None
        
    def extract(self):
        try:
            result_laptops = subprocess.run(['scrapy', 'crawl', 'laptops'], capture_output=True, text=True)
            result_books = subprocess.run(['scrapy', 'crawl', 'libreria'], capture_output=True, text=True)
            
            if os.path.exists('laptops_data.json') and os.path.exists('libreria_data.json'):
                return True
            return False
        except Exception as e:
            print(f"Error: {e}")
            return False
    
    def transform(self):
        try:
            transformer = DataTransformer()
            unified_df = transformer.run_transformation()
            return unified_df is not None and len(unified_df) > 0
        except Exception as e:
            print(f"Error: {e}")
            return False
    
    def load(self):
        try:
            db = DatabaseManager()
            db.setup_database('catalog_transformed.csv')
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False
    
    def run_pipeline(self, skip_extract=False):
        self.start_time = datetime.now()
        success = True
        
        if not skip_extract:
            if not self.extract():
                success = False
        
        if success or skip_extract:
            if not self.transform():
                success = False
        
        if success:
            if not self.load():
                success = False
        
        self.end_time = datetime.now()
        return success


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Pipeline ETL')
    parser.add_argument('--skip-extract', action='store_true')
    args = parser.parse_args()
    
    pipeline = ETLPipeline()
    success = pipeline.run_pipeline(skip_extract=args.skip_extract)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
