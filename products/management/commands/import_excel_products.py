from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.text import slugify
from products.models import Product, Product_group, Segments, Oil_Types, Viscosity, Liter
import pandas as pd
import os

class Command(BaseCommand):
    help = 'Import products from all sheets of an Excel file with a flexible key column for product identification.'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the Excel file')
        parser.add_argument(
            '--key-column',
            type=str,
            default='Product ID',
            help='The name of the column that uniquely identifies a product. Defaults to "Product ID".'
        )
        # New: Add option to specify which sheets to process
        parser.add_argument(
            '--sheets',
            type=str,
            nargs='*',
            help='Specific sheet names to process. If not provided, all sheets will be processed.'
        )
        # New: Add option for dry run
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Perform a dry run without actually creating products.'
        )
        # New: Add option to update existing products
        parser.add_argument(
            '--update-existing',
            action='store_true',
            help='Update existing products instead of skipping them.'
        )

    def handle(self, *args, **options):
        file_path = options['file_path']
        key_column_name = options['key_column']
        specific_sheets = options.get('sheets')
        dry_run = options['dry_run']
        update_existing = options['update_existing']
        
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f'File {file_path} does not exist'))
            return

        if not file_path.lower().endswith(('.xlsx', '.xls')):
            self.stdout.write(self.style.ERROR('This command only supports Excel files (.xlsx, .xls)'))
            return

        self.stdout.write(self.style.SUCCESS(f"Using '{key_column_name}' as the key identifier column."))
        
        if dry_run:
            self.stdout.write(self.style.WARNING("DRY RUN MODE: No products will be created or updated."))
        
        if update_existing:
            self.stdout.write(self.style.HTTP_INFO("UPDATE MODE: Existing products will be updated."))

        try:
            xls = pd.ExcelFile(file_path)
            
            # Filter sheets if specific sheets are requested
            sheets_to_process = specific_sheets if specific_sheets else xls.sheet_names
            
            # Validate requested sheets exist
            invalid_sheets = [sheet for sheet in sheets_to_process if sheet not in xls.sheet_names]
            if invalid_sheets:
                self.stdout.write(self.style.ERROR(f"Invalid sheet names: {invalid_sheets}"))
                self.stdout.write(self.style.HTTP_INFO(f"Available sheets: {xls.sheet_names}"))
                return
            
            total_success = 0
            total_errors = 0
            total_updated = 0
            total_skipped = 0

            for sheet_name in sheets_to_process:
                self.stdout.write(self.style.HTTP_INFO(f'\n--- Processing sheet: {sheet_name} ---'))
                
                # Find header row
                df_for_header_find = pd.read_excel(xls, sheet_name=sheet_name, header=None)
                header_row_index = self.find_header_row(df_for_header_find, key_column_name)
                
                if header_row_index == -1:
                    self.stdout.write(self.style.WARNING(f"Could not find a header row with '{key_column_name}' in sheet '{sheet_name}'. Skipping sheet."))
                    continue

                # Process headers (multi-level or single-level)
                df = self.process_headers(xls, sheet_name, header_row_index, key_column_name)
                
                if df is None or key_column_name not in df.columns:
                    self.stdout.write(self.style.ERROR(f"Key column '{key_column_name}' not found in sheet '{sheet_name}'. Skipping sheet."))
                    continue
                
                # Clean and process data
                processed_df = self.clean_and_group_data(df, key_column_name)
                data = processed_df.to_dict('records')
                
                success_count = 0
                error_count = 0
                updated_count = 0
                skipped_count = 0
                
                for row_num, row in enumerate(data, start=1):
                    try:
                        if not dry_run:
                            with transaction.atomic():
                                result = self.import_product(row, key_column_name, update_existing)
                                if result == 'created':
                                    success_count += 1
                                elif result == 'updated':
                                    updated_count += 1
                                elif result == 'skipped':
                                    skipped_count += 1
                        else:
                            # In dry run mode, just validate the data
                            self.validate_product_data(row, key_column_name)
                            success_count += 1
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f'Error processing product from sheet "{sheet_name}" (row {row_num}): {row.get(key_column_name)}. Reason: {str(e)}'))
                        error_count += 1
                
                self.stdout.write(self.style.SUCCESS(f'Sheet "{sheet_name}" processing complete. Created: {success_count}, Updated: {updated_count}, Skipped: {skipped_count}, Errors: {error_count}'))
                total_success += success_count
                total_errors += error_count
                total_updated += updated_count
                total_skipped += skipped_count

            self.stdout.write(self.style.SUCCESS(f'\nImport finished for all sheets. Total Created: {total_success}, Total Updated: {total_updated}, Total Skipped: {total_skipped}, Total Errors: {total_errors}'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An unexpected error occurred: {str(e)}'))

    def find_header_row(self, df_for_header_find, key_column_name):
        """Find the row index that contains the headers"""
        for i, row in df_for_header_find.iterrows():
            if key_column_name in [str(x).strip() for x in row.values]:
                return i
        return -1

    def process_headers(self, xls, sheet_name, header_row_index, key_column_name):
        """Process headers, handling both single-level and multi-level structures"""
        df_for_header_find = pd.read_excel(xls, sheet_name=sheet_name, header=None)
        
        # Check if multi-level headers exist
        is_multi_level = False
        if header_row_index + 1 < len(df_for_header_find):
            next_row_values = [str(x).strip() for x in df_for_header_find.iloc[header_row_index + 1].values]
            sub_header_keywords = ['API', 'ILSAC', 'ACEA', 'JASO', 'OEM specifications', 'Specification', 'Standard']
            if any(keyword in next_row_values for keyword in sub_header_keywords):
                is_multi_level = True

        if is_multi_level:
            self.stdout.write(self.style.HTTP_INFO(f"Detected multi-level header in sheet '{sheet_name}'."))
            df = pd.read_excel(xls, sheet_name=sheet_name, header=[header_row_index, header_row_index + 1])
            
            # Flatten multi-level columns
            new_columns = []
            for col in df.columns:
                top_level_header = str(col[0]).strip()
                sub_level_header = str(col[1]).strip()
                if top_level_header == key_column_name:
                    new_columns.append(key_column_name)
                elif 'unnamed' in sub_level_header.lower() or sub_level_header == 'nan':
                    new_columns.append(top_level_header)
                else:
                    new_columns.append(sub_level_header)
            df.columns = new_columns
        else:
            self.stdout.write(self.style.HTTP_INFO(f"Detected single-level header in sheet '{sheet_name}'."))
            df = pd.read_excel(xls, sheet_name=sheet_name, header=header_row_index)
            df.columns = [str(col).strip() for col in df.columns]
        
        return df

    def clean_and_group_data(self, df, key_column_name):
        """Clean the dataframe and group by product ID"""
        # Remove rows where key column is empty
        df.dropna(subset=[key_column_name], inplace=True, how='all')
        
        # Forward fill key identification columns
        id_cols = [key_column_name, 'Product Name', 'Product name', 'product_group_id', 'oil_type_id', 'viscosity_id', 'segments', 'liters']
        for col in id_cols:
            if col in df.columns:
                df[col] = df[col].ffill()

        # Define aggregation functions
        agg_funcs = {}
        for col in df.columns:
            if col in df:
                if df[col].dtype == 'object':
                    # For text columns, join unique values
                    agg_funcs[col] = lambda x: '\n'.join(x.dropna().astype(str).unique()) if not x.dropna().empty else ''
                else:
                    # For numeric columns, take first non-null value
                    agg_funcs[col] = 'first'
        
        # Don't aggregate the key column (it's the groupby column)
        if key_column_name in agg_funcs:
            agg_funcs.pop(key_column_name)
        
        # Group by product ID and aggregate
        processed_df = df.groupby(key_column_name).agg(agg_funcs).reset_index()
        return processed_df

    def validate_product_data(self, row, key_column_name):
        """Validate product data without creating the product (for dry run)"""
        def get_value(key, default=''):
            value = row.get(key, default)
            value_str = str(value).strip()
            return '' if pd.isna(value) or value_str.lower() == 'nan' else value_str

        product_id = get_value(key_column_name)
        if not product_id:
            raise ValueError(f"Row has no value in the key column '{key_column_name}'.")

        title = get_value('Product Name') or get_value('Product name')
        if not title:
            title = f"Product {product_id}"

        # Validate foreign key references
        product_group_id = get_value('product_group_id')
        if product_group_id:
            try:
                Product_group.objects.get(id=int(float(product_group_id)))
            except (Product_group.DoesNotExist, ValueError):
                self.stdout.write(self.style.WARNING(f'Product group ID {product_group_id} not found for product {product_id}.'))

        # Similar validation for other foreign keys...
        self.stdout.write(f'Validated product: {title} (ID: {product_id})')

    def import_product(self, row, key_column_name, update_existing=False):
        """Import or update a single product"""
        def get_value(key, default=''):
            value = row.get(key, default)
            value_str = str(value).strip()
            return '' if pd.isna(value) or value_str.lower() == 'nan' else value_str

        product_id = get_value(key_column_name)
        if not product_id:
            raise ValueError(f"Row has no value in the key column '{key_column_name}'.")

        # Check if product exists
        existing_product = Product.objects.filter(product_id=product_id).first()
        
        if existing_product:
            if not update_existing:
                self.stdout.write(f'Skipping existing product with ID: {product_id}')
                return 'skipped'
            else:
                # Update existing product
                product = existing_product
                self.stdout.write(f'Updating existing product with ID: {product_id}')
                action = 'updated'
        else:
            # Create new product
            product = Product()
            action = 'created'

        # Set product fields
        title = get_value('Product Name') or get_value('Product name')
        if not title:
            title = f"Product {product_id}"

        product_slug = slugify(title)
        if not product_slug:
            product_slug = str(product_id)
        
        # Ensure unique slug
        if not existing_product or product.slug != product_slug:
            counter = 1
            original_slug = product_slug
            while Product.objects.filter(slug=product_slug).exclude(id=product.id if existing_product else None).exists():
                product_slug = f'{original_slug}-{counter}'
                counter += 1

        # Set basic fields
        product.product_id = product_id
        product.title = title
        product.slug = product_slug
        product.description = get_value('Description')
        product.features_benefits = get_value('Features & Benefits')
        product.application = get_value('Application')
        product.api = get_value('API') or None
        product.ilsac = get_value('ILSAC') or None
        product.acea = get_value('ACEA') or None
        product.jaso = get_value('JASO') or None
        product.oem_sertification = get_value('OEM specifications')
        product.recommendations = get_value('Recommendation') or None
        product.pds_url = get_value('pds_url') or None
        product.sds_url = get_value('sds_url') or None

        # Handle foreign key relationships
        product_group_id = get_value('product_group_id')
        if product_group_id:
            try:
                product.product_group = Product_group.objects.get(id=int(float(product_group_id)))
            except (Product_group.DoesNotExist, ValueError):
                self.stdout.write(self.style.WARNING(f'Product group ID {product_group_id} not found for product {product_id}.'))
                product.product_group = None

        oil_type_id = get_value('oil_type_id')
        if oil_type_id:
            try:
                product.oil_type = Oil_Types.objects.get(id=int(float(oil_type_id)))
            except (Oil_Types.DoesNotExist, ValueError):
                self.stdout.write(self.style.WARNING(f'Oil type ID {oil_type_id} not found for product {product_id}.'))
                product.oil_type = None

        viscosity_id = get_value('viscosity_id')
        if viscosity_id:
            try:
                product.viscosity = Viscosity.objects.get(id=int(float(viscosity_id)))
            except (Viscosity.DoesNotExist, ValueError):
                self.stdout.write(self.style.WARNING(f'Viscosity ID {viscosity_id} not found for product {product_id}.'))
                product.viscosity = None

        product.save()

        # Handle many-to-many relationships
        segments_data = get_value('segments')
        if segments_data:
            if action == 'updated':
                product.segments.clear()
            segment_items = [item.strip() for item in segments_data.split(',') if item.strip()]
            for segment_item in segment_items:
                try:
                    segment = Segments.objects.get(id=int(segment_item)) if segment_item.isdigit() else Segments.objects.get(title__iexact=segment_item)
                    product.segments.add(segment)
                except Segments.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f'Segment "{segment_item}" not found for product {product_id}.'))

        liters_data = get_value('liters')
        if liters_data:
            if action == 'updated':
                product.liters.clear()
            liter_items = [item.strip() for item in str(liters_data).split(',') if item.strip()]
            for liter_item in liter_items:
                try:
                    liter = Liter.objects.get(volume=float(liter_item)) if liter_item.replace('.', '', 1).isdigit() else Liter.objects.get(id=int(liter_item))
                    product.liters.add(liter)
                except (Liter.DoesNotExist, ValueError):
                    self.stdout.write(self.style.WARNING(f'Liter "{liter_item}" not found for product {product_id}.'))

        status_message = f'Successfully {"updated" if action == "updated" else "created"} product: {product.title}'
        self.stdout.write(self.style.SUCCESS(status_message))
        
        return action