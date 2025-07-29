import os
from PIL import Image, UnidentifiedImageError
from io import BytesIO
import shutil
import warnings

# Image limits
Image.MAX_IMAGE_PIXELS = 200000000
warnings.filterwarnings("ignore", "Image size")

# SVG desteği
try:
    import cairosvg
    SVG_SUPPORT = True
except ImportError:
    SVG_SUPPORT = False

# Hedef boyut aralığı (KB) - 100KB hedef
TARGET_MIN_KB = 95
TARGET_MAX_KB = 105

# WebP kalite aralığı - 100KB için daha yüksek kalite
WEBP_QUALITY_MIN = 50
WEBP_QUALITY_MAX = 95

# Minimum ve maksimum görsel boyutu (px) - Boyut sınırlaması kaldırıldı
MIN_IMAGE_DIMENSION = 50   # Çok küçük boyutları engelle
MAX_IMAGE_DIMENSION = 2000 # Çok büyük boyutları sınırla

# Desteklenen uzantılar
if SVG_SUPPORT:
    IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.webp', '.svg', '.bmp', '.tiff', '.gif')
else:
    IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.webp', '.bmp', '.tiff', '.gif')

# Kaynak ve hedef dizinler
SOURCE_DIR = "/Avtoil/gallery"
COMPRESSED_OUTPUT_DIR = "/Avtoil/mediafile/gallery"

def get_file_size_kb(buffer):
    return len(buffer.getvalue()) / 1024

def resize_to_max(img, min_dimension=MIN_IMAGE_DIMENSION, max_dimension=MAX_IMAGE_DIMENSION):
    width, height = img.size
    longest_side = max(width, height)

    # Sadece çok büyük görselleri küçült
    if longest_side > max_dimension:
        scale = max_dimension / longest_side
        new_width = int(width * scale)
        new_height = int(height * scale)
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    # Çok küçük görselleri büyüt
    elif longest_side < min_dimension:
        scale = min_dimension / longest_side
        new_width = int(width * scale)
        new_height = int(height * scale)
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    # Normal boyuttaki görselleri olduğu gibi bırak
    return img

def compress_webp(img):
    last_buffer = None
    best_buffer = None
    best_quality = None
    
    # Önce hedef aralığa uymaya çalış
    for quality in range(WEBP_QUALITY_MAX, WEBP_QUALITY_MIN - 1, -5):
        buffer = BytesIO()
        try:
            img.save(buffer, format="WEBP", quality=quality, optimize=True)
            size_kb = get_file_size_kb(buffer)
            
            # Hedef aralıkta bir değer bulundu
            if TARGET_MIN_KB <= size_kb <= TARGET_MAX_KB:
                return buffer
            
            # En iyi alternatifi sakla (hedef maksimuma en yakın olan)
            if best_buffer is None or abs(size_kb - TARGET_MAX_KB) < abs(get_file_size_kb(best_buffer) - TARGET_MAX_KB):
                best_buffer = buffer
                best_quality = quality
            
            last_buffer = buffer
        except:
            continue
    
    # Hedef aralıkta bir değer bulunamadıysa, en iyi alternatifi döndür
    if best_buffer is not None:
        return best_buffer
    
    # Son çare olarak en son buffer'ı döndür
    return last_buffer

def convert_svg_to_image(svg_path):
    if not SVG_SUPPORT:
        return None
    try:
        png_data = cairosvg.svg2png(url=svg_path)
        img = Image.open(BytesIO(png_data))
        return img
    except:
        return None

def safe_makedirs(path):
    try:
        if os.path.exists(path):
            if os.path.isfile(path):
                os.remove(path)
        os.makedirs(path, exist_ok=True)
        return True
    except:
        return False

def process_single_image(original_image_path, compressed_image_save_path):
    try:
        if not os.path.exists(original_image_path) or not os.access(original_image_path, os.R_OK):
            return False

        file_ext = os.path.splitext(original_image_path)[1].lower()

        if file_ext == '.svg':
            img = convert_svg_to_image(original_image_path)
            if img is None:
                return False
        else:
            try:
                img = Image.open(original_image_path)
            except:
                return False

        img = resize_to_max(img)

        # Mode dönüşümü
        try:
            if img.mode in ['P', 'LA']:
                img = img.convert("RGBA")
            elif img.mode not in ['RGB', 'RGBA', 'L']:
                img = img.convert("RGB")
        except:
            try:
                img = img.convert("RGB")
            except:
                return False

        base_name = os.path.splitext(os.path.basename(compressed_image_save_path))[0]
        dir_name = os.path.dirname(compressed_image_save_path)
        compressed_image_save_path = os.path.join(dir_name, base_name + '.webp')

        if not safe_makedirs(dir_name):
            return False

        buffer = compress_webp(img)
        if buffer is None or len(buffer.getvalue()) == 0:
            return False

        with open(compressed_image_save_path, "wb") as f_out:
            f_out.write(buffer.getvalue())

        # Dosya boyutunu ve görsel boyutunu kontrol et ve rapor et
        final_size_kb = os.path.getsize(compressed_image_save_path) / 1024
        
        # Görsel boyutunu kontrol et
        try:
            check_img = Image.open(compressed_image_save_path)
            img_width, img_height = check_img.size
            print(f"✅ {os.path.basename(original_image_path)} → {final_size_kb:.2f} KB ({img_width}x{img_height}px)")
        except:
            print(f"✅ {os.path.basename(original_image_path)} → {final_size_kb:.2f} KB")

        return True

    except Exception as e:
        print(f"❌ {os.path.basename(original_image_path)} işlenirken hata: {str(e)}")
        return False

def is_safe_path(path, base_dir):
    try:
        abs_base = os.path.abspath(base_dir)
        abs_path = os.path.abspath(path)
        return abs_path.startswith(abs_base)
    except:
        return False

def process_source_directory():
    if not os.path.exists(SOURCE_DIR) or not os.path.isdir(SOURCE_DIR):
        print("❌ Geçerli kaynak dizini bulunamadı.")
        return

    if not safe_makedirs(COMPRESSED_OUTPUT_DIR):
        print("❌ Hedef dizin oluşturulamadı.")
        return

    processed_count = 0
    total_original_size = 0
    total_compressed_size = 0

    for root, _, files in os.walk(SOURCE_DIR):
        if not is_safe_path(root, SOURCE_DIR):
            continue

        for file in files:
            if not file.lower().endswith(IMAGE_EXTENSIONS):
                continue

            original_path = os.path.join(root, file)
            if not is_safe_path(original_path, SOURCE_DIR):
                continue

            relative_path = os.path.relpath(original_path, SOURCE_DIR)
            base_name = os.path.splitext(relative_path)[0]
            compressed_save_path = os.path.join(COMPRESSED_OUTPUT_DIR, base_name + '.webp')

            if os.path.exists(compressed_save_path):
                continue

            # Orijinal dosya boyutunu kaydet
            original_size = os.path.getsize(original_path)
            total_original_size += original_size

            if process_single_image(original_path, compressed_save_path):
                processed_count += 1
                compressed_size = os.path.getsize(compressed_save_path)
                total_compressed_size += compressed_size

    # Sonuçları rapor et
    if processed_count > 0:
        compression_ratio = (total_compressed_size / total_original_size) * 100
        print(f"\n📊 İşlem Özeti:")
        print(f"   Toplam işlenen dosya: {processed_count}")
        print(f"   Orijinal toplam boyut: {total_original_size / 1024:.2f} KB")
        print(f"   Sıkıştırılmış toplam boyut: {total_compressed_size / 1024:.2f} KB")
        print(f"   Sıkıştırma oranı: {compression_ratio:.1f}%")
        print(f"   Tasarruf: {((total_original_size - total_compressed_size) / 1024):.2f} KB")

if __name__ == "__main__":
    print("🚀 100KB Hedef Boyut WebP Dönüştürme Başladı...")
    print(f"   Hedef dosya boyutu: {TARGET_MIN_KB}-{TARGET_MAX_KB} KB")
    print(f"   Kalite aralığı: {WEBP_QUALITY_MIN}-{WEBP_QUALITY_MAX}")
    print(f"   Görsel boyutu: Orijinal boyut korunuyor")
    process_source_directory()
    print("✅ İşlem Tamamlandı.")