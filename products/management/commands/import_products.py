from django.core.management.base import BaseCommand
from django.db import transaction
from products.models import Product, Product_group, Segments, Oil_Types, Viscosity, Liter
import csv
import os


class Command(BaseCommand):
    help = 'Import products from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']
        
        if not os.path.exists(csv_file_path):
            self.stdout.write(
                self.style.ERROR(f'File {csv_file_path} does not exist')
            )
            return

        with open(csv_file_path, 'r', encoding='utf-8') as file:
            # Read CSV with proper handling
            csv_reader = csv.DictReader(file)
            
            # Get the fieldnames to understand the structure
            fieldnames = csv_reader.fieldnames
            self.stdout.write(f"CSV columns: {fieldnames}")
            
            success_count = 0
            error_count = 0
            
            for row_num, row in enumerate(csv_reader, start=2):  # Start from 2 because header is row 1
                try:
                    with transaction.atomic():
                        self.import_product(row)
                        success_count += 1
                        self.stdout.write(f"Successfully imported row {row_num}")
                        
                except Exception as e:
                    error_count += 1
                    self.stdout.write(
                        self.style.ERROR(f'Error importing row {row_num}: {str(e)}')
                    )
                    
            self.stdout.write(
                self.style.SUCCESS(
                    f'Import completed. Success: {success_count}, Errors: {error_count}'
                )
            )

    def import_product(self, row):
        """Import a single product from CSV row"""
        
        # Extract basic product data
        product_data = {
            'title': row.get('title', '').strip(),
            'description': row.get('description', '').strip(),
            'features_benefits': row.get('features_benefits', '').strip(),
            'application': row.get('application', '').strip(),
            'product_id': row.get('product_id', '').strip(),
            'slug': row.get('slug', '').strip(),
            'api': row.get('api', '').strip() or None,
            'ilsac': row.get('ilsac', '').strip() or None,
            'acea': row.get('acea', '').strip() or None,
            'jaso': row.get('jaso', '').strip() or None,
            'oem_sertification': row.get('oem_sertification', '').strip() or None,
            'recommendations': row.get('recommendations', '').strip() or None,
            'pds_url': row.get('pds_url', '').strip() or None,
            'sds_url': row.get('sds_url', '').strip() or None,
        }
        
        # Handle image field
        image_path = row.get('image', '').strip()
        if image_path:
            product_data['image'] = image_path
        
        # Handle ID field if provided in CSV
        product_id_from_csv = row.get('id', '').strip()
        if product_id_from_csv and product_id_from_csv.isdigit():
            product_data['id'] = int(product_id_from_csv)
            
        # Create or get foreign key relationships
        
        # Handle Product Group
        product_group = None
        product_group_id = row.get('product_group_id', '').strip()
        if product_group_id:
            try:
                product_group = Product_group.objects.get(id=int(product_group_id))
            except (Product_group.DoesNotExist, ValueError):
                self.stdout.write(
                    self.style.WARNING(f'Product group with ID {product_group_id} not found')
                )
        
        # Handle Oil Type
        oil_type = None
        oil_type_id = row.get('oil_type_id', '').strip()
        if oil_type_id:
            try:
                oil_type = Oil_Types.objects.get(id=int(oil_type_id))
            except (Oil_Types.DoesNotExist, ValueError):
                self.stdout.write(
                    self.style.WARNING(f'Oil type with ID {oil_type_id} not found')
                )
        
        # Handle Viscosity
        viscosity = None
        viscosity_id = row.get('viscosity_id', '').strip()
        if viscosity_id:
            try:
                viscosity = Viscosity.objects.get(id=int(viscosity_id))
            except (Viscosity.DoesNotExist, ValueError):
                self.stdout.write(
                    self.style.WARNING(f'Viscosity with ID {viscosity_id} not found')
                )
        
        # Create or update the product with ID handling
        if 'id' in product_data and product_data['id']:
            # If ID is provided, use update_or_create with ID as lookup
            product, created = Product.objects.update_or_create(
                id=product_data['id'],
                defaults={
                    **{k: v for k, v in product_data.items() if k != 'id'},
                    'product_group': product_group,
                    'oil_type': oil_type,
                    'viscosity': viscosity,
                }
            )
        else:
            # Use product_id as lookup if no ID is specified
            product, created = Product.objects.update_or_create(
                product_id=product_data['product_id'],
                defaults={
                    **{k: v for k, v in product_data.items() if k != 'id'},
                    'product_group': product_group,
                    'oil_type': oil_type,
                    'viscosity': viscosity,
                }
            )
        
        # Handle Many-to-Many relationships
        
        # Handle Segments
        segments_data = row.get('segments', '').strip()
        if segments_data:
            # Clear existing segments first
            product.segments.clear()
            
            # If segments are stored as comma-separated IDs or names
            segment_items = [item.strip() for item in segments_data.split(',') if item.strip()]
            
            for segment_item in segment_items:
                try:
                    # Try to get by ID first
                    if segment_item.isdigit():
                        segment = Segments.objects.get(id=int(segment_item))
                    else:
                        # Try to get by name
                        segment = Segments.objects.get(name__iexact=segment_item)
                    
                    product.segments.add(segment)
                    
                except Segments.DoesNotExist:
                    self.stdout.write(
                        self.style.WARNING(f'Segment "{segment_item}" not found')
                    )
        
        # Handle Liters
        liters_data = row.get('liters', '').strip()
        if liters_data:
            # Clear existing liters first
            product.liters.clear()
            
            # If liters are stored as comma-separated values
            liter_items = [item.strip() for item in liters_data.split(',') if item.strip()]
            
            for liter_item in liter_items:
                try:
                    # Try to get by ID first
                    if liter_item.isdigit():
                        liter = Liter.objects.get(id=int(liter_item))
                    else:
                        # Try to get by value
                        liter = Liter.objects.get(value__iexact=liter_item)
                    
                    product.liters.add(liter)
                    
                except Liter.DoesNotExist:
                    self.stdout.write(
                        self.style.WARNING(f'Liter "{liter_item}" not found')
                    )
        
        action = "Created" if created else "Updated"
        self.stdout.write(f'{action} product: {product.title} (ID: {product.id})')
        
        return product

    def get_or_create_related_object(self, model_class, identifier, name_field='name'):
        """Helper method to get or create related objects"""
        if not identifier:
            return None
            
        try:
            # Try to get by ID first
            if str(identifier).isdigit():
                return model_class.objects.get(id=int(identifier))
            else:
                # Try to get by name field
                filter_kwargs = {f'{name_field}__iexact': identifier}
                return model_class.objects.get(**filter_kwargs)
                
        except model_class.DoesNotExist:
            # Create new object if it doesn't exist (optional)
            if hasattr(model_class, name_field):
                create_kwargs = {name_field: identifier}
                obj, created = model_class.objects.get_or_create(**create_kwargs)
                if created:
                    self.stdout.write(f'Created new {model_class.__name__}: {identifier}')
                return obj
            return None
