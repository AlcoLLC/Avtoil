from django.shortcuts import render
from django.db.models import Q
from django.utils.translation import get_language
from django.core.paginator import Paginator
import re

# Import all your models
from about.models import AboutAvtoil, AboutContent, DocumentsCertification, Sustainability
from products.models import Product_group, Segments, Oil_Types, Viscosity, Liter, Product, ProductProperty
from contact.models import Contact, ContactInfo
from faq.models import FAQ
from home.models import HomeSwiper
from news.models import News, News_Content
from services.models import Service, Service_Content


def create_search_queries(query):
    """
    Create multiple search queries from the input:
    1. Full query
    2. Individual words
    3. Partial matches for each word
    """
    queries = []
    
    # Add the full query
    queries.append(query.strip())
    
    # Split by spaces and add individual words (minimum 2 characters)
    words = [word.strip() for word in query.split() if len(word.strip()) >= 2]
    queries.extend(words)
    
    return queries


def build_search_q(query, fields):
    """
    Build a Q object for searching across multiple fields with partial matching
    """
    q_objects = Q()
    search_queries = create_search_queries(query)
    
    for field in fields:
        for search_term in search_queries:
            q_objects |= Q(**{f"{field}__icontains": search_term})
    
    return q_objects


def search_view(request):
    query = request.GET.get('search', '').strip()
    results = []
    total_results = 0
    
    if query and len(query) >= 2:  # Minimum 2 characters for search
        current_language = get_language()
        is_english = current_language == 'en'
        
        # Search Products
        if is_english:
            product_fields = ['title', 'description', 'features_benefits', 'application', 
                            'recommendations', 'product_id', 'api', 'ilsac', 'acea', 'jaso']
        else:
            product_fields = [ 'title', 'description', 'product_id']
        
        products = Product.objects.filter(build_search_q(query, product_fields)).distinct()
        
        for product in products:
            title = product.title if not is_english and product.title else 'product.title'
            description = product.description if not is_english and product.description else 'product.description'
            results.append({
                'title': title,
                'description': description[:200] + '...' if description and len(description) > 200 else description or '',
                'url': f'/product/{product.slug}/',
                'type': 'Product',
                'image': product.image.url if product.image else None
            })

        # Search Home Swiper
        swiper_fields = ['title', 'description', 'title_description']
        
        swipers = HomeSwiper.objects.filter(
            build_search_q(query, swiper_fields),
            is_active=True
        ).distinct()
        
        for swiper in swipers:
            results.append({
                'title': swiper.title,
                'description': swiper.description[:200] + '...' if swiper.description and len(swiper.description) > 200 else swiper.description or '',
                'url': swiper.link or '/',
                'type': 'Home Banner',
                'image': swiper.image.url if swiper.image else None
            })
        
        # Search Product Groups
        if is_english:
            group_fields = ['title', 'description']
        else:
            group_fields = ['title', 'description']
        
        product_groups = Product_group.objects.filter(build_search_q(query, group_fields)).distinct()
        
        for group in product_groups:
            title = group.title  if not is_english and group.title else 'group.title'
            description = group.description if not is_english and group.description else 'group.description'
            results.append({
                'title': title,
                'description': description[:200] + '...' if description and len(description) > 200 else description or '',
                'url': f'/product/',
                'type': 'Product Group',
                'image': group.image.url if group.image else None
            })
        
        # Search Segments
        if is_english:
            segment_fields = ['title']
        else:
            segment_fields = [ 'title']
        
        segments = Segments.objects.filter(build_search_q(query, segment_fields)).distinct()
        
        for segment in segments:
            title = segment.title if not is_english and segment.title else 'segment.title'
            results.append({
                'title': title,
                'description': f'Product Segment: {title}',
                'url': f'/product/?segment={segment.slug}',
                'type': 'Product Segment',
                'image': None
            })
        
        # Search Oil Types
        if is_english:
            oil_type_fields = ['title']
        else:
            oil_type_fields = ['title']
        
        oil_types = Oil_Types.objects.filter(build_search_q(query, oil_type_fields)).distinct()
        
        for oil_type in oil_types:
            title = oil_type.title if not is_english and oil_type.title else 'oil_type.title'
            results.append({
                'title': title,
                'description': f'Oil Type: {title}',
                'url': f'/product/?oil_type={oil_type.slug}',
                'type': 'Oil Type',
                'image': None
            })
        
        # Search Viscosity
        viscosities = Viscosity.objects.filter(build_search_q(query, ['title'])).distinct()
        
        for viscosity in viscosities:
            results.append({
                'title': viscosity.title,
                'description': f'Viscosity: {viscosity.title}',
                'url': f'/product/?viscosity={viscosity.slug}',
                'type': 'Viscosity',
                'image': None
            })
        
        # Search Product Properties
        if is_english:
            property_fields = ['property_name', 'test_method', 'typical_value']
        else:
            property_fields = ['property_name', 'test_method', 'typical_value']
        
        product_properties = ProductProperty.objects.filter(build_search_q(query, property_fields)).distinct()
        
        for prop in product_properties:
            property_name = prop.property_name if not is_english and prop.property_name else ''
            results.append({
                'title': f'{prop.product.title} - {property_name}',
                'description': f'Property: {property_name}, Test Method: {prop.test_method}, Value: {prop.typical_value}',
                'url': f'/product/{prop.product.slug}/',
                'type': 'Product Property',
                'image': None
            })
        
        # Search News
        if is_english:
            news_fields = ['title', 'content']
        else:
            news_fields = ['title', 'content']
        
        news_items = News.objects.filter(
            build_search_q(query, news_fields),
            is_active=True
        ).distinct()
        
        for news in news_items:
            title = news.title if not is_english and news.title else ''
            content = news.content if not is_english and news.content else ''
            results.append({
                'title': title,
                'description': content[:200] + '...' if content and len(content) > 200 else content or '',
                'url': f'/news/{news.id}/',
                'type': 'News',
                'image': news.image.url if news.image else None
            })
        
        # Search News Content
        if is_english:
            news_content_fields = ['description']
        else:
            news_content_fields = ['description']
        
        news_contents = News_Content.objects.filter(build_search_q(query, news_content_fields)).distinct()
        
        for content in news_contents:
            description = content.description if not is_english and content.description else ''
            news_title = content.news.title  if not is_english and content.news.title  else ''
            results.append({
                'title': news_title,
                'description': description[:200] + '...' if description and len(description) > 200 else description or '',
                'url': f'/news/{content.news.id}/',
                'type': 'News',
                'image': content.image.url if content.image else None
            })
        
        # Search FAQ
        if is_english:
            faq_fields = ['question', 'answer']
        else:
            faq_fields = ['question', 'answer']
        
        faqs = FAQ.objects.filter(
            build_search_q(query, faq_fields),
            is_active=True
        ).distinct()
        
        for faq in faqs:
            question = faq.question if not is_english and faq.question else ''
            answer = faq.answer if not is_english and faq.answer else ''
            results.append({
                'title': question,
                'description': answer[:200] + '...' if answer and len(answer) > 200 else answer or '',
                'url': '/faq/',
                'type': 'FAQ',
                'image': None
            })
        
         # Search About Avtoil
        if is_english:
            cert_fields = ['title', 'description']
        else:
            cert_fields = ['title', 'description']
        
        about_avtoil = AboutAvtoil.objects.filter(build_search_q(query, cert_fields)).distinct()

        for content in about_avtoil:
            title = content.title if not is_english and content.title else ''
            description = content.description  if not is_english and content.description else ''
            results.append({
                'title': title,
                'description': description[:200] + '...' if description and len(description) > 200 else description or '',
                'url': '/about/',
                'image': content.image.url if content.image else None
            })
        
              
         # Search About Content
        if is_english:
            cert_fields = ['title', 'description']
        else:
            cert_fields = ['title', 'description']
        
        about_content = AboutContent.objects.filter(build_search_q(query, cert_fields)).distinct()

        for content in about_content:
            title = content.title if not is_english and content.title else ''
            description = content.description  if not is_english and content.description else ''
            results.append({
                'title': title,
                'description': description[:200] + '...' if description and len(description) > 200 else description or '',
                'url': '/about/',
                'image': content.image.url if content.image else None
            })
        

        # Search Documents & Certifications
        if is_english:
            cert_fields = ['title', 'description']
        else:
            cert_fields = ['title', 'description']
        
        certifications_contents = DocumentsCertification.objects.filter(build_search_q(query, cert_fields)).distinct()

        for content in certifications_contents:
            title = content.title if not is_english and content.title else ''
            description = content.description  if not is_english and content.description else ''
            results.append({
                'title': title,
                'description': description[:200] + '...' if description and len(description) > 200 else description or '',
                'url': '/about/',
                'type': 'Documents & Certifications',
                'image': content.image.url if content.image else None
            })
        
      
        # Search Sustainability
        sustainability_items = Sustainability.objects.filter(build_search_q(query, ['description'])).distinct()
        
        for item in sustainability_items:
            description = item.description if not is_english and item.description else ''
            results.append({
                'title': 'Sustainability',
                'description': description[:200] + '...' if description and len(description) > 200 else description or '',
                'url': '/about/',
                'type': 'Sustainability',
                'image': item.image.url if item.image else None
            })

        
        # Search Contact Info
        if is_english:
            contact_fields = ['title', 'description', 'aminol_headquarters', 'aminol_factory', 
                            'registers', 'contact_address']
        else:
            contact_fields = ['title', 'description', 'aminol_headquarters', 'aminol_factory']
        
        contact_infos = ContactInfo.objects.filter(build_search_q(query, contact_fields)).distinct()
        
        for contact in contact_infos:
            title = contact.title if not is_english and contact.title else ''
            description = contact.description if not is_english and contact.description else ''
            results.append({
                'title': title,
                'description': description[:200] + '...' if description and len(description) > 200 else description or '',
                'url': '/contact/',
                'type': 'Contact',
                'image': None
            })
        
        # Search Aminol Official Service
        if is_english:
            service_fields = ['title', 'title_description', 'description']
        else:
            service_fields = ['title', 'description']
        
        service_services = Service.objects.filter(build_search_q(query, service_fields)).distinct()
        
        for service in service_services:
            title = service.title if not is_english and service.title else ''
            description = service.description if not is_english and service.description else ''
            results.append({
                'title': title,
                'description': description[:200] + '...' if description and len(description) > 200 else description or '',
                'url': '/services/',
                'type': 'Service',
                'image': service.image.url if service.image else None
            })
        
        # Search Service Content
        if is_english:
            service_content_fields = ['title', 'description']
        else:
            service_content_fields = [ 'title', 'description']
        
        service_contents = Service_Content.objects.filter(build_search_q(query, service_content_fields)).distinct()
        
        for content in service_contents:
            title = content.title if not is_english and content.title else ''
            description = content.description if not is_english and content.description else ''
            results.append({
                'title': title,
                'description': description[:200] + '...' if description and len(description) > 200 else description or '',
                'url': '/services/',
                'type': 'Service',
                'image': content.image.url if content.image else None
            })
               
        # Remove duplicates based on title and type
        seen = set()
        unique_results = []
        for result in results:
            identifier = (result['title'], result['type'])
            if identifier not in seen:
                seen.add(identifier)
                unique_results.append(result)
        
        results = unique_results
        total_results = len(results)
        
        # Sort results by relevance (exact matches first, then partial matches)
        def calculate_relevance(result):
            title_lower = result['title'].lower()
            desc_lower = result['description'].lower()
            query_lower = query.lower()
            
            # Exact match in title gets highest score
            if query_lower in title_lower:
                return 100
            # Exact match in description gets high score
            elif query_lower in desc_lower:
                return 80
            # Partial word matches get medium score
            else:
                score = 0
                for word in query_lower.split():
                    if word in title_lower:
                        score += 20
                    elif word in desc_lower:
                        score += 10
                return score
        
        results.sort(key=calculate_relevance, reverse=True)
        
        paginator = Paginator(results, 10) 
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    else:
        page_obj = None
    
    context = {
        'query': query,
        'results': page_obj,
        'total_results': total_results,
    }
    
    return render(request, 'search.html', context)