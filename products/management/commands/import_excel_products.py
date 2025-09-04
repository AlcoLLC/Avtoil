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
        # NEW: Add a flexible argument for the key column name.
        parser.add_argument(
            '--key-column',
            type=str,
            default='Product ID',
            help='The name of the column that uniquely identifies a product. Defaults to "Product ID".'
        )

    # products/management/commands/import_excel_products.py

# ... (diğer her şey aynı kalacak) ...

    # products/management/commands/import_excel_products.py

# ... (diğer her şey aynı kalacak) ...

    def handle(self, *args, **options):
        file_path = options['file_path']
        key_column_name = options['key_column']
        
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f'File {file_path} does not exist'))
            return

        if not file_path.lower().endswith(('.xlsx', '.xls')):
            self.stdout.write(self.style.ERROR('This command only supports Excel files (.xlsx, .xls)'))
            return

        self.stdout.write(self.style.SUCCESS(f"Using '{key_column_name}' as the key identifier column."))

        try:
            xls = pd.ExcelFile(file_path)
            
            total_success = 0
            total_errors = 0

            for sheet_name in xls.sheet_names:
                self.stdout.write(self.style.HTTP_INFO(f'\n--- Processing sheet: {sheet_name} ---'))
                
                df_for_header_find = pd.read_excel(xls, sheet_name=sheet_name, header=None)
                
                header_row_index = -1
                for i, row in df_for_header_find.iterrows():
                    if key_column_name in [str(x).strip() for x in row.values]:
                        header_row_index = i
                        break
                
                if header_row_index == -1:
                    self.stdout.write(self.style.WARNING(f"Could not find a header row with '{key_column_name}' in sheet '{sheet_name}'. Skipping sheet."))
                    continue

                # --- YENİ MANTIK: Başlık yapısını otomatik algıla ---
                is_multi_level = False
                # Bir sonraki satırın var olup olmadığını kontrol et
                if header_row_index + 1 < len(df_for_header_find):
                    next_row_values = [str(x).strip() for x in df_for_header_find.iloc[header_row_index + 1].values]
                    # Çok seviyeli başlıklarda bulunan anahtar kelimeler
                    sub_header_keywords = ['API', 'ILSAC', 'ACEA', 'JASO', 'OEM specifications']
                    if any(keyword in next_row_values for keyword in sub_header_keywords):
                        is_multi_level = True

                if is_multi_level:
                    # Bu sayfa ÇOK SEVİYELİ bir başlığa sahip
                    self.stdout.write(self.style.HTTP_INFO(f"Detected multi-level header in sheet '{sheet_name}'."))
                    df = pd.read_excel(xls, sheet_name=sheet_name, header=[header_row_index, header_row_index + 1])
                    
                    # Çok seviyeli başlığı tek seviyeye indir (flatten)
                    new_columns = []
                    for col in df.columns:
                        top_level_header = str(col[0]).strip()
                        sub_level_header = str(col[1]).strip()
                        if top_level_header == key_column_name:
                            new_columns.append(key_column_name)
                        elif 'unnamed' in sub_level_header.lower():
                            new_columns.append(top_level_header)
                        else:
                            new_columns.append(sub_level_header)
                    df.columns = new_columns
                else:
                    # Bu sayfa TEK SEVİYELİ bir başlığa sahip
                    self.stdout.write(self.style.HTTP_INFO(f"Detected single-level header in sheet '{sheet_name}'."))
                    df = pd.read_excel(xls, sheet_name=sheet_name, header=header_row_index)
                    # Sütun isimlerindeki olası boşlukları temizle
                    df.columns = [str(col).strip() for col in df.columns]
                # --- OTOMATİK ALGILAMA MANTIĞININ SONU ---

                if key_column_name not in df.columns:
                    self.stdout.write(self.style.ERROR(f"Key column '{key_column_name}' not found in the final headers for sheet '{sheet_name}'. Skipping sheet."))
                    continue
                
                df.dropna(subset=[key_column_name], inplace=True, how='all')
                
                id_cols = [key_column_name, 'Product Name', 'product_group_id', 'oil_type_id', 'viscosity_id', 'segments', 'liters']
                for col in id_cols:
                    if col in df.columns:
                        df[col] = df[col].ffill()

                agg_funcs = {}
                for col in df.columns:
                    if col in df:
                        if df[col].dtype == 'object':
                            agg_funcs[col] = lambda x: '\n'.join(x.dropna().astype(str).unique())
                        else:
                            agg_funcs[col] = 'first'
                
                if key_column_name in agg_funcs:
                    agg_funcs.pop(key_column_name)
                
                processed_df = df.groupby(key_column_name).agg(agg_funcs).reset_index()

                data = processed_df.to_dict('records')
                
                success_count = 0
                error_count = 0
                
                for row_num, row in enumerate(data, start=1):
                    try:
                        with transaction.atomic():
                            self.import_product(row, key_column_name)
                            success_count += 1
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f'Error importing product from sheet "{sheet_name}" (row {row_num}): {row.get(key_column_name)}. Reason: {str(e)}'))
                        error_count += 1
                
                self.stdout.write(self.style.SUCCESS(f'Sheet "{sheet_name}" processing complete. Success: {success_count}, Errors: {error_count}'))
                total_success += success_count
                total_errors += error_count

            self.stdout.write(self.style.SUCCESS(f'\nImport finished for all sheets. Total Success: {total_success}, Total Errors: {total_errors}'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An unexpected error occurred: {str(e)}'))
               
    # MODIFIED: The function now accepts key_column_name as an argument.
    def import_product(self, row, key_column_name):
        def get_value(key, default=''):
            value = row.get(key, default)
            value_str = str(value).strip()
            return '' if pd.isna(value) or value_str.lower() == 'nan' else value_str

        # MODIFIED: Use the key_column_name to get the product ID.
        product_id = get_value(key_column_name)
        if not product_id:
            raise ValueError(f"Row has no value in the key column '{key_column_name}'.")

        if Product.objects.filter(product_id=product_id).exists():
            self.stdout.write(f'Skipping existing product with ID: {product_id}')
            return

        title = get_value('Product Name')
        if not title:
            title = f"Product {product_id}"

        product_slug = slugify(title)
        if not product_slug:
             product_slug = str(product_id) # Ensure slug is a string
        
        counter = 1
        original_slug = product_slug
        while Product.objects.filter(slug=product_slug).exists():
            product_slug = f'{original_slug}-{counter}'
            counter += 1

        product_data = {
            'product_id': product_id,
            'title': title,
            'slug': product_slug,
            'description': get_value('Description'),
            'features_benefits': get_value('Features & Benefits'),
            'application': get_value('Application'),
            'api': get_value('API') or None,
            'ilsac': get_value('ILSAC') or None,
            'acea': get_value('ACEA') or None,
            'jaso': get_value('JASO') or None,
            'oem_sertification': get_value('OEM specifications'),
            'recommendations': get_value('Recommendation') or None,
            'pds_url': get_value('pds_url') or None,
            'sds_url': get_value('sds_url') or None,
        }
        
        # Foreign Key and M2M relations remain the same...
        product_group = None
        product_group_id = get_value('product_group_id')
        if product_group_id:
            try:
                product_group = Product_group.objects.get(id=int(float(product_group_id)))
            except (Product_group.DoesNotExist, ValueError):
                self.stdout.write(self.style.WARNING(f'Product group ID {product_group_id} not found for product {product_id}.'))

        oil_type = None
        oil_type_id = get_value('oil_type_id')
        if oil_type_id:
            try:
                oil_type = Oil_Types.objects.get(id=int(float(oil_type_id)))
            except (Oil_Types.DoesNotExist, ValueError):
                self.stdout.write(self.style.WARNING(f'Oil type ID {oil_type_id} not found for product {product_id}.'))

        viscosity = None
        viscosity_id = get_value('viscosity_id')
        if viscosity_id:
            try:
                viscosity = Viscosity.objects.get(id=int(float(viscosity_id)))
            except (Viscosity.DoesNotExist, ValueError):
                self.stdout.write(self.style.WARNING(f'Viscosity ID {viscosity_id} not found for product {product_id}.'))

        product = Product.objects.create(
            **product_data,
            product_group=product_group,
            oil_type=oil_type,
            viscosity=viscosity,
        )
        
        segments_data = get_value('segments')
        if segments_data:
            segment_items = [item.strip() for item in segments_data.split(',') if item.strip()]
            for segment_item in segment_items:
                try:
                    segment = Segments.objects.get(id=int(segment_item)) if segment_item.isdigit() else Segments.objects.get(title__iexact=segment_item)
                    product.segments.add(segment)
                except Segments.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f'Segment "{segment_item}" not found for product {product_id}.'))

        liters_data = get_value('liters')
        if liters_data:
            liter_items = [item.strip() for item in str(liters_data).split(',') if item.strip()]
            for liter_item in liter_items:
                try:
                    liter = Liter.objects.get(volume=float(liter_item)) if liter_item.replace('.', '', 1).isdigit() else Liter.objects.get(id=int(liter_item))
                    product.liters.add(liter)
                except (Liter.DoesNotExist, ValueError):
                    self.stdout.write(self.style.WARNING(f'Liter "{liter_item}" not found for product {product_id}.'))

        self.stdout.write(self.style.SUCCESS(f'Successfully created product: {product.title}'))