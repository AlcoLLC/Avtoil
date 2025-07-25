import os
import shutil
from PIL import Image, UnidentifiedImageError
from io import BytesIO

# Yeni hedef boyut aralığı - maksimum 150 KB
TARGET_MIN_KB = 20
TARGET_MAX_KB = 150

# WebP kalite aralığı - daha yüksek kalite kullanıyoruz
WEBP_QUALITY_MIN = 40
WEBP_QUALITY_MAX = 85

IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.webp', '.svg', '.bmp', '.tiff', '.gif')

DIRECTORIES_TO_PROCESS = [
    {'source': 'staticfiles/images_1', 'target': 'staticfiles/images'},
    {'source': 'staticfiles/images_folder_1', 'target': 'staticfiles/images_folder'}
]

# SVG desteği için cairosvg import
try:
    import cairosvg
    SVG_SUPPORT = True
except ImportError:
    SVG_SUPPORT = False
    print("⚠️  SVG desteği yok. SVG dosyalarını işlemek için 'pip install cairosvg' komutunu çalıştırın.")


def get_file_size_kb(buffer):
    return len(buffer.getvalue()) / 1024


def compress_webp_to_target(img):
    """WebP formatında 20-150 KB hedef boyutuna sıkıştırma"""
    original_width, original_height = img.size
    last_buffer = None
    
    # Farklı boyut seçenekleri (küçükten büyüğe) - daha fazla seçenek
    size_multipliers = [0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2]
    
    for multiplier in size_multipliers:
        # Yeni boyutları hesapla
        new_width = max(100, int(original_width * multiplier))  # Minimum 100px
        new_height = max(100, int(original_height * multiplier))  # Minimum 100px
        
        # Resmi yeniden boyutlandır
        resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Farklı kalite seviyelerini dene (yüksekten düşüğe)
        for quality in range(WEBP_QUALITY_MAX, WEBP_QUALITY_MIN - 1, -5):
            buffer = BytesIO()
            resized_img.save(buffer, format="WEBP", quality=quality, optimize=True)
            size_kb = get_file_size_kb(buffer)
            
            # Hedef aralıkta mı kontrol et
            if TARGET_MIN_KB <= size_kb <= TARGET_MAX_KB:
                return buffer, size_kb, (new_width, new_height)
            
            # En son buffer'ı sakla
            last_buffer = buffer
            
            # Eğer maksimum boyutun üzerindeyse, kaliteyi düşür
            if size_kb > TARGET_MAX_KB:
                continue
            
            # Eğer minimum boyutun altındaysa, bir sonraki boyut multiplier'ına geç
            if size_kb < TARGET_MIN_KB:
                break
    
    # Hedef aralıkta bulamadıysak en son buffer'ı döndür
    if last_buffer:
        last_size = get_file_size_kb(last_buffer)
        # Son boyutları da hesaplayalım
        last_width = max(100, int(original_width * size_multipliers[-1]))
        last_height = max(100, int(original_height * size_multipliers[-1]))
        return last_buffer, last_size, (last_width, last_height)
    
    # Hiçbir şey bulamazsak ortalama bir versiyonu oluştur
    medium_img = img.resize((400, 400), Image.Resampling.LANCZOS)
    buffer = BytesIO()
    medium_img.save(buffer, format="WEBP", quality=60, optimize=True)
    size_kb = get_file_size_kb(buffer)
    return buffer, size_kb, (400, 400)


def convert_svg_to_image(svg_path):
    """SVG dosyasını PIL Image objesine dönüştür"""
    if not SVG_SUPPORT:
        return None
    
    try:
        # SVG'yi PNG'ye çevir
        png_data = cairosvg.svg2png(url=svg_path)
        # PNG verisini PIL Image'e yükle
        img = Image.open(BytesIO(png_data))
        return img
    except Exception as e:
        print(f"❌ SVG dönüştürme hatası {svg_path}: {e}")
        return None


def process_single_image(original_image_path, compressed_image_save_path, source_root):
    """Tek bir resim dosyasını 20-150 KB WebP formatına çevir"""
    try:
        if not os.path.exists(original_image_path) or not os.access(original_image_path, os.R_OK):
            print(f"⏭ Okunamayan dosya: {original_image_path}")
            return False

        original_size_kb = os.path.getsize(original_image_path) / 1024
        file_ext = os.path.splitext(original_image_path)[1].lower()

        # Çıktı dosyasının uzantısını .webp olarak değiştir
        base_name = os.path.splitext(os.path.basename(compressed_image_save_path))[0]
        dir_name = os.path.dirname(compressed_image_save_path)
        compressed_image_save_path = os.path.join(dir_name, base_name + '.webp')

        # SVG dosyası kontrolü
        if file_ext == '.svg':
            if not SVG_SUPPORT:
                print(f"⏭ SVG desteği yok, atlanıyor: {original_image_path}")
                return False
            
            img = convert_svg_to_image(original_image_path)
            if img is None:
                return False
            print(f"🔄 SVG WebP'ye dönüştürülüyor: {original_image_path}")
        else:
            img = Image.open(original_image_path)

        # WebP için mod dönüşümleri
        if img.mode == 'P':
            if img.info.get("transparency") is not None:
                img = img.convert("RGBA")
            else:
                img = img.convert("RGB")
        elif img.mode == 'LA':
            img = img.convert("RGBA")
        elif img.mode not in ('RGB', 'RGBA', 'L'):
            img = img.convert("RGB")

        # 20-150 KB hedefine WebP dosyasını oluştur
        buffer, compressed_size_kb, dimensions = compress_webp_to_target(img)
        
        if not buffer or len(buffer.getvalue()) == 0:
            print(f"❌ WebP sıkıştırması başarısız: {original_image_path}")
            return False

        os.makedirs(os.path.dirname(compressed_image_save_path), exist_ok=True)
        with open(compressed_image_save_path, "wb") as f_out:
            f_out.write(buffer.getvalue())

        # Hedef aralık kontrolü
        in_target_range = TARGET_MIN_KB <= compressed_size_kb <= TARGET_MAX_KB
        range_indicator = "🎯" if in_target_range else "📊"
        
        print(f"✔ WebP'ye dönüştürüldü: {original_image_path}")
        print(f"  ↳ Kaydedildi: {compressed_image_save_path}")
        print(f"  {range_indicator} {int(original_size_kb)} KB → {int(compressed_size_kb)} KB")
        print(f"  📐 Boyut: {dimensions[0]}x{dimensions[1]}")
        
        if not in_target_range:
            if compressed_size_kb < TARGET_MIN_KB:
                print(f"  ⚠️  Hedef aralığın altında ({TARGET_MIN_KB}-{TARGET_MAX_KB} KB)")
            else:
                print(f"  ⚠️  Hedef aralığın üstünde ({TARGET_MIN_KB}-{TARGET_MAX_KB} KB)")

        return True

    except FileNotFoundError:
        print(f"❌ Dosya bulunamadı: {original_image_path}")
        return False
    except UnidentifiedImageError:
        print(f"❌ Tanınamayan resim dosyası: {original_image_path}")
        return False
    except Exception as e:
        print(f"❌ Genel hata ({original_image_path}): {e}")
        return False


def process_directory_pair(source_dir, target_dir):
    """Bir kaynak-hedef dizin çiftini işle"""
    total_files = 0
    skipped_existing = 0
    processed = 0
    failed = 0
    svg_converted = 0
    in_target_range = 0

    print(f"📂 Kaynak: {source_dir}")
    print(f"💾 Hedef: {target_dir}")
    print(f"🎯 Hedef boyut: {TARGET_MIN_KB}-{TARGET_MAX_KB} KB")
    
    if not os.path.exists(source_dir):
        print(f"❌ Kaynak dizin mevcut değil: {source_dir}")
        return total_files, skipped_existing, processed, failed, svg_converted, in_target_range

    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.lower().endswith(IMAGE_EXTENSIONS):
                total_files += 1
                original_path = os.path.join(root, file)
                relative_path = os.path.relpath(original_path, source_dir)
                
                # Çıktı dosyasının uzantısını .webp olarak değiştir
                base_name = os.path.splitext(relative_path)[0]
                compressed_path = os.path.join(target_dir, base_name + '.webp')

                if os.path.exists(compressed_path):
                    print(f"⏭ WebP dosyası zaten mevcut: {compressed_path}")
                    skipped_existing += 1
                    continue

                is_svg = file.lower().endswith('.svg')

                if process_single_image(original_path, compressed_path, source_dir):
                    processed += 1
                    if is_svg:
                        svg_converted += 1
                    
                    # Hedef aralık kontrolü
                    if os.path.exists(compressed_path):
                        size_kb = os.path.getsize(compressed_path) / 1024
                        if TARGET_MIN_KB <= size_kb <= TARGET_MAX_KB:
                            in_target_range += 1
                else:
                    failed += 1

    return total_files, skipped_existing, processed, failed, svg_converted, in_target_range


def process_all_directories():
    """Tüm dizin çiftlerini işle"""
    print(f"🚀 20-150 KB WebP dönüştürme başlatıldı")
    print(f"🎯 Hedef boyut aralığı: {TARGET_MIN_KB}-{TARGET_MAX_KB} KB")
    print(f"🔧 Kalite aralığı: {WEBP_QUALITY_MIN}-{WEBP_QUALITY_MAX}")
    print(f"🔄 Tüm resimler optimize edilecek ve 20-150 KB aralığına sıkıştırılacak.")
    if SVG_SUPPORT:
        print("✅ SVG desteği aktif.")
    else:
        print("❌ SVG desteği yok.")
    print("-" * 80)

    totals = [0, 0, 0, 0, 0, 0]  # total, skipped, processed, failed, svg_converted, in_target_range

    for pair in DIRECTORIES_TO_PROCESS:
        source, target = pair['source'], pair['target']
        print(f"\n📁 İşleniyor: {source} → {target}")
        print("-" * 60)

        result = process_directory_pair(source, target)
        totals = [sum(x) for x in zip(totals, result)]

        print(f"\n📊 {source} → {target} özeti:")
        print(f"🔎 Toplam resim dosyası: {result[0]}")
        print(f"⏭ Atlanan (zaten var): {result[1]}")
        print(f"✔ WebP'ye çevrilen: {result[2]}")
        print(f"🔄 SVG'den çevrilen: {result[4]}")
        print(f"🎯 Hedef aralıkta ({TARGET_MIN_KB}-{TARGET_MAX_KB} KB): {result[5]}")
        print(f"❌ Başarısız: {result[3]}")

    print("\n" + "=" * 80)
    print("🏁 GENEL ÖZET - 20-150 KB WebP Dönüştürme")
    print(f"🔎 Toplam resim dosyası bulundu: {totals[0]}")
    print(f"⏭ Toplam atlanan (zaten mevcut): {totals[1]}")
    print(f"✔ Başarıyla WebP'ye çevrilen: {totals[2]}")
    print(f"🔄 SVG'den WebP'ye çevrilen: {totals[4]}")
    print(f"🎯 Hedef aralıkta ({TARGET_MIN_KB}-{TARGET_MAX_KB} KB): {totals[5]}")
    print(f"❌ Başarısız olan: {totals[3]}")
    print(f"🛠 İşlenmeye çalışılan toplam: {totals[2] + totals[3]}")
    
    if totals[2] > 0:
        success_rate = (totals[2] / (totals[2] + totals[3])) * 100
        target_success_rate = (totals[5] / totals[2]) * 100
        print(f"📈 Genel başarı oranı: {success_rate:.1f}%")
        print(f"🎯 Hedef aralık başarı oranı: {target_success_rate:.1f}%")


if __name__ == "__main__":
    process_all_directories()