from django.core.management.base import BaseCommand
from django.db import transaction
from products.models import Product, Product_group, Segments, Oil_Types, Viscosity, Liter
import csv
import os
import pandas as pd


class Command(BaseCommand):
    help = 'Import products from CSV or Excel file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the CSV or Excel file')
        parser.add_argument(
            '--sheet', 
            type=str, 
            default=None, 
            help='Excel sheet name (if not specified, uses the first sheet)'
        )

    def handle(self, *args, **options):
        file_path = options['file_path']
        sheet_name = options.get('sheet')
        
        if not os.path.exists(file_path):
            self.stdout.write(
                self.style.ERROR(f'File {file_path} does not exist')
            )
            return

        try:
            # Determine file type and read accordingly
            if file_path.lower().endswith(('.xlsx', '.xls')):
                df = pd.read_excel(file_path, sheet_name=sheet_name)
                self.stdout.write(f"Reading Excel file: {file_path}")
                if sheet_name:
                    self.stdout.write(f"Sheet: {sheet_name}")
            elif file_path.lower().endswith('.csv'):
                # Try different encodings for CSV files
                encodings_to_try = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
                df = None
                
                for encoding in encodings_to_try:
                    try:
                        df = pd.read_csv(file_path, encoding=encoding)
                        self.stdout.write(f"Successfully read CSV with {encoding} encoding")
                        break
                    except UnicodeDecodeError:
                        continue
                
                if df is None:
                    self.stdout.write(
                        self.style.ERROR('Could not read CSV file with any supported encoding')
                    )
                    return
            else:
                self.stdout.write(
                    self.style.ERROR('Unsupported file format. Please use .xlsx, .xls, or .csv')
                )
                return

            # Display columns found
            columns = df.columns.tolist()
            self.stdout.write(f"Columns found: {columns}")
            
            # Replace NaN values with empty strings
            df = df.fillna('')
            
            success_count = 0
            error_count = 0
            
            for index, row in df.iterrows():
                try:
                    with transaction.atomic():
                        self.import_product(row)
                        success_count += 1
                except Exception as e:
                    error_count += 1
                    self.stdout.write(
                        self.style.ERROR(f'Error importing row {index + 2}: {str(e)}')
                    )
                    
            self.stdout.write(
                self.style.SUCCESS(
                    f'Import completed. Success: {success_count}, Errors: {error_count}'
                )
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error reading file: {str(e)}')
            )
            return

    def import_product(self, row):
        """Import a single product from a pandas Series (row)"""
        
        # Convert pandas Series to dict-like access
        def safe_get(key, default=''):
            try:
                value = row.get(key, default)
                return str(value).strip() if pd.notna(value) else default
            except:
                return default

        # Get Product ID
        product_id = safe_get('Product ID')
        if not product_id:
            raise ValueError("Product ID is required but was not found in the row.")

        # Skip if product already exists
        if Product.objects.filter(product_id=product_id).exists():
            self.stdout.write(f'Skipping existing product with ID: {product_id}')
            return

        product_data = {
            'product_id': product_id,
            'title': safe_get('Product Name'),
            'description': safe_get('Description'),
            'features_benefits': safe_get('Features & Benefits'),
            'application': safe_get('Application'),
            
            # Performance columns
            'api': safe_get('API') or None,
            'ilsac': safe_get('ILSAC') or None,
            'acea': safe_get('ACEA') or None,
            'jaso': safe_get('JASO') or None,
            
            # Other specifications
            'oem_sertification': safe_get('OEM Specifications') or None,
            'recommendations': safe_get('Recommendation') or None,
            
            # Additional fields
            'slug': safe_get('slug') or None,
            'pds_url': safe_get('pds_url') or None,
            'sds_url': safe_get('sds_url') or None,
        }
        
        # --- Related Models Management ---
        
        # Product Group
        product_group = None
        product_group_id = safe_get('product_group_id')
        if product_group_id:
            try:
                product_group = Product_group.objects.get(id=int(product_group_id))
            except (Product_group.DoesNotExist, ValueError):
                self.stdout.write(self.style.WARNING(f'Product group with ID {product_group_id} not found.'))

        # Oil Type
        oil_type = None
        oil_type_id = safe_get('oil_type_id')
        if oil_type_id:
            try:
                oil_type = Oil_Types.objects.get(id=int(oil_type_id))
            except (Oil_Types.DoesNotExist, ValueError):
                self.stdout.write(self.style.WARNING(f'Oil type with ID {oil_type_id} not found.'))

        # Viscosity
        viscosity = None
        viscosity_id = safe_get('viscosity_id')
        if viscosity_id:
            try:
                viscosity = Viscosity.objects.get(id=int(viscosity_id))
            except (Viscosity.DoesNotExist, ValueError):
                self.stdout.write(self.style.WARNING(f'Viscosity with ID {viscosity_id} not found.'))

        # Create the product
        product = Product.objects.create(
            **product_data,
            product_group=product_group,
            oil_type=oil_type,
            viscosity=viscosity,
        )
        
        # --- Many-to-Many Relationships ---

        # Segments
        segments_data = safe_get('segments')
        if segments_data:
            segment_items = [item.strip() for item in str(segments_data).split(',') if item.strip()]
            for segment_item in segment_items:
                try:
                    if segment_item.isdigit():
                        segment = Segments.objects.get(id=int(segment_item))
                    else:
                        segment = Segments.objects.get(name__iexact=segment_item)
                    product.segments.add(segment)
                except Segments.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f'Segment "{segment_item}" not found.'))

        # Liters
        liters_data = safe_get('liters')
        if liters_data:
            liter_items = [item.strip() for item in str(liters_data).split(',') if item.strip()]
            for liter_item in liter_items:
                try:
                    if liter_item.isdigit():
                        liter = Liter.objects.get(id=int(liter_item))
                    else:
                        liter = Liter.objects.get(value__iexact=liter_item)
                    product.liters.add(liter)
                except Liter.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f'Liter "{liter_item}" not found.'))

        self.stdout.write(self.style.SUCCESS(f'Successfully created product: {product.title}'))