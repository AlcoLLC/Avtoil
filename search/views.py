from django.shortcuts import render
from django.db.models import Q
from django.utils.translation import get_language
from django.core.paginator import Paginator
import re

# Import all your models
from about.models import AboutAvtoil, AboutContent, DocumentsCertification, Sustainability
from products.models import Product_group, Segments, Oil_Types, Viscosity, Product, ProductProperty
from contact.models import  ContactInfo
from faq.models import FAQ
from home.models import HomeSwiper, BecomePartner, SolutionsHybrid, SolutionsHybridContent, Review
from news.models import News, News_Content
from services.models import Service, Service_Content
from partnership.models import Partnership, Partnership_Content, PartnerReview, PartnerFAQ


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
    
    if query and len(query) >= 2:  
        current_language = get_language()
        is_english = current_language == 'en'
        
        # Search Products
        if is_english:
            product_fields = ['title', 'description', 'features_benefits', 'application', 
                            'recommendations', 'product_id', 'api', 'ilsac', 'acea', 'jaso']
        else:
            product_fields = ['title', 'description', 'product_id']
        
        products = Product.objects.filter(build_search_q(query, product_fields)).distinct()
        
        for product in products:
            title = product.title or ''
            description = product.description or ''
            results.append({
                'title': title,
                'description': description[:200] + '...' if description and len(description) > 200 else description,
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
                'title': swiper.title or '',
                'description': (swiper.description or '')[:200] + '...' if swiper.description and len(swiper.description) > 200 else swiper.description or '',
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
            title = group.title or ''
            description = group.description or ''
            results.append({
                'title': title,
                'description': description[:200] + '...' if description and len(description) > 200 else description,
                'url': f'/product/',
                'type': 'Product Group',
                'image': group.image.url if group.image else None
            })
        
        # Search Segments
        if is_english:
            segment_fields = ['title']
        else:
            segment_fields = ['title']
        
        segments = Segments.objects.filter(build_search_q(query, segment_fields)).distinct()
        
        for segment in segments:
            title = segment.title or ''
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
            title = oil_type.title or ''
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
                'title': viscosity.title or '',
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
            property_name = prop.property_name or ''
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
            title = news.title or ''
            content = news.content or ''
            results.append({
                'title': title,
                'description': content[:200] + '...' if content and len(content) > 200 else content,
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
            description = content.description or ''
            news_title = content.news.title or ''
            results.append({
                'title': news_title,
                'description': description[:200] + '...' if description and len(description) > 200 else description,
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
            question = faq.question or ''
            answer = faq.answer or ''
            results.append({
                'title': question,
                'description': answer[:200] + '...' if answer and len(answer) > 200 else answer,
                'url': '/faq/',
                'type': 'FAQ',
                'image': None
            })
        
        # Search About Avtoil
        if is_english:
            about_fields = ['title', 'description']
        else:
            about_fields = ['title', 'description']
        
        about_avtoil = AboutAvtoil.objects.filter(build_search_q(query, about_fields)).distinct()

        for content in about_avtoil:
            title = content.title or ''
            description = content.description or ''
            results.append({
                'title': title,
                'description': description[:200] + '...' if description and len(description) > 200 else description,
                'url': '/about/',
                'type': 'About',
                'image': content.image.url if content.image else None
            })
                     
        # Search About Content
        if is_english:
            about_content_fields = ['title', 'description']
        else:
            about_content_fields = ['title', 'description']
        
        about_content = AboutContent.objects.filter(build_search_q(query, about_content_fields)).distinct()

        for content in about_content:
            title = content.title or ''
            description = content.description or ''
            results.append({
                'title': title,
                'description': description[:200] + '...' if description and len(description) > 200 else description,
                'url': '/about/',
                'type': 'About Content',
                'image': content.image.url if content.image else None
            })
        
        # Search Documents & Certifications
        if is_english:
            cert_fields = ['title', 'description']
        else:
            cert_fields = ['title', 'description']
        
        certifications_contents = DocumentsCertification.objects.filter(build_search_q(query, cert_fields)).distinct()

        for content in certifications_contents:
            title = content.title or ''
            description = content.description or ''
            results.append({
                'title': title,
                'description': description[:200] + '...' if description and len(description) > 200 else description,
                'url': '/about/',
                'type': 'Documents & Certifications',
                'image':  None
            })
        
        # Search Sustainability
        sustainability_items = Sustainability.objects.filter(build_search_q(query, ['description'])).distinct()
        
        for item in sustainability_items:
            description = item.description or ''
            results.append({
                'title': 'Sustainability',
                'description': description[:200] + '...' if description and len(description) > 200 else description,
                'url': '/about/',
                'type': 'Sustainability',
                'image': item.image.url if item.image else None
            })

        # Search Contact Info
        if is_english:
            contact_fields = ['title', 'description', 'avtoil_headquarters', 'avtoil_factory', 
                            'registers', 'contact_address']
        else:
            contact_fields = ['title', 'description', 'avtoil_headquarters', 'avtoil_factory']
        
        contact_infos = ContactInfo.objects.filter(build_search_q(query, contact_fields)).distinct()
        
        for contact in contact_infos:
            title = contact.title or ''
            description = contact.description or ''
            results.append({
                'title': title,
                'description': description[:200] + '...' if description and len(description) > 200 else description,
                'url': '/contact/',
                'type': 'Contact',
                'image': None
            })
        
        # Search Service
        if is_english:
            service_fields = ['title', 'description']
        else:
            service_fields = ['title', 'description']
        
        service_services = Service.objects.filter(build_search_q(query, service_fields)).distinct()
        
        for service in service_services:
            title = service.title or ''
            description = service.description or ''
            results.append({
                'title': title,
                'description': description[:200] + '...' if description and len(description) > 200 else description,
                'url': '/services/',
                'type': 'Service',
                'image': service.image.url if service.image else None
            })
        
        # Search Service Content
        if is_english:
            service_content_fields = ['title', 'description']
        else:
            service_content_fields = ['title', 'description']
        
        service_contents = Service_Content.objects.filter(build_search_q(query, service_content_fields)).distinct()

        for content in service_contents:
            title = content.title or ''
            description = content.description or ''
            results.append({
                'title': title,
                'description': description[:200] + '...' if description and len(description) > 200 else description,
                'url': '/services/',
                'type': 'Service Content',
                'image': content.image.url if content.image else None
            })
        
        # Search Partnership
        if is_english:
            partnership_fields = ['title', 'description']
        else:
            partnership_fields = ['title', 'description']
        
        partnerships = Partnership.objects.filter(build_search_q(query, partnership_fields)).distinct()
        
        for partnership in partnerships:
            title = partnership.title or ''
            description = partnership.description or ''
            results.append({
                'title': title,
                'description': description[:200] + '...' if description and len(description) > 200 else description,
                'url': '/partnership/',
                'type': 'Partnership',
                'image': partnership.main_image.url if partnership.main_image else None
            })
        
        # Search Partnership Content
        partnership_contents = Partnership_Content.objects.filter(build_search_q(query, ['title'])).distinct()
        
        for content in partnership_contents:
            title = content.title or ''
            results.append({
                'title': title,
                'description': f'Partnership Content: {title}',
                'url': '/partnership/',
                'type': 'Partnership Content',
                'image': None
            })
        
        # Search Partner Reviews
        if is_english:
            review_fields = ['name', 'position', 'review']
        else:
            review_fields = ['name', 'position', 'review']
        
        partner_reviews = PartnerReview.objects.filter(
            build_search_q(query, review_fields),
            is_active=True
        ).distinct()
        
        for review in partner_reviews:
            name = review.name or ''
            position = review.position or ''
            review_text = review.review or ''
            results.append({
                'title': f'{name} - {position}',
                'description': review_text[:200] + '...' if review_text and len(review_text) > 200 else review_text,
                'url': '/partnership/',
                'type': 'Partner Review',
                'image': review.image.url if review.image else None
            })
        
        # Search Partner FAQ
        if is_english:
            partner_faq_fields = ['question', 'answer']
        else:
            partner_faq_fields = ['question', 'answer']
        
        partner_faqs = PartnerFAQ.objects.filter(
            build_search_q(query, partner_faq_fields),
            is_active=True
        ).distinct()
        
        for faq in partner_faqs:
            question = faq.question or ''
            answer = faq.answer or ''
            results.append({
                'title': question,
                'description': answer[:200] + '...' if answer and len(answer) > 200 else answer,
                'url': '/partnership/',
                'type': 'Partner FAQ',
                'image': None
            })


        # BecomePartner axtarışı
        become_partners = BecomePartner.objects.filter(
            build_search_q(query, ['title', 'description'])
        ).distinct()
        for item in become_partners:
            results.append({
                'title': item.title or '',
                'description': (item.description or '')[:200] + '...',
                'url': '/become-partner/',
                'type': 'Become Partner',
                'image': item.image.url if item.image else None
            })

        # SolutionsHybrid axtarışı
        solutions_hybrids = SolutionsHybrid.objects.filter(
            build_search_q(query, ['title', 'description_left', 'description_right'])
        ).distinct()
        for item in solutions_hybrids:
            results.append({
                'title': item.title or '',
                'description': ((item.description_left or '') + " " + (item.description_right or ''))[:200] + '...',
                'url': '/solutions-hybrid/',
                'type': 'Solutions Hybrid',
                'image': None
            })

        # SolutionsHybridContent axtarışı
        solutions_contents = SolutionsHybridContent.objects.filter(
            build_search_q(query, ['content'])
        ).distinct()
        for item in solutions_contents:
            results.append({
                'title': f"Content: {item.content}" or '',
                'description': '',
                'url': '/solutions-hybrid/',
                'type': 'Solutions Hybrid Content',
                'image': None
            })

        # Review axtarışı
        reviews = Review.objects.filter(
            build_search_q(query, ['first_name', 'surname', 'summary', 'review'])
        ).distinct()
        for review in reviews:
            results.append({
                'title': f"{review.first_name} {review.surname} - {review.summary}",
                'description': (review.review or '')[:200] + '...',
                'url': '/reviews/',
                'type': 'Review',
                'image': None
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