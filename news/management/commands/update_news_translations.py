from django.core.management.base import BaseCommand
from django.conf import settings
from news.models import News, News_Content 

class Command(BaseCommand):
    help = 'Set default and empty translation fields for News and News_Content'

    def handle(self, *args, **options):
        default_lang = getattr(settings, 'MODELTRANSLATION_DEFAULT_LANGUAGE', 'en')
        languages = [lang_code for lang_code, _ in settings.LANGUAGES]

        def update_fields(instance, fields):
            for field in fields:
                default_value = getattr(instance, field, '')
                default_field = f"{field}_{default_lang}"
                if not getattr(instance, default_field, None):
                    setattr(instance, default_field, default_value)

                for lang in languages:
                    if lang != default_lang:
                        translated_field = f"{field}_{lang}"
                        if not getattr(instance, translated_field, None):
                            setattr(instance, translated_field, '')

        for news in News.objects.all():
            update_fields(news, ['title', 'content'])
            news.save()

        for item in News_Content.objects.all():
            update_fields(item, ['description'])
            item.save()

        self.stdout.write(self.style.SUCCESS("✅ Translation fields for News and News_Content set successfully."))
