from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
import json

from news.models import News
from services.models import Service, Service_Content
from products.models import Product_group, Product
from about.models import Sustainability
from .models import PartnerLogo, Gallery as GalleryImage, HomeSwiper, BecomePartner, SolutionsHybrid, Review

def get_client_ip(request):
    """Get client IP address"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def home_view(request): 
    """Home page view - only handles GET requests"""
    swiper_images = HomeSwiper.objects.filter(is_active=True).order_by('order')
    latest_news = News.objects.filter(is_active=True)[:3]   
    product_groups = Product_group.objects.all().order_by('-in_home', 'order')  
    products = Product.objects.all().order_by('-in_home', 'order')  
    partner_logos = PartnerLogo.objects.all()
    images = GalleryImage.objects.all().order_by('order')
    service_contents = Service_Content.objects.filter(in_home=True)
    sustainability = Sustainability.objects.last()
    sustainability_image = sustainability.image if sustainability else None
    become_partner = BecomePartner.objects.last()      
    solutions_hybrid = SolutionsHybrid.objects.last()
    solutions_contents = solutions_hybrid.SolutionsHybrid.all() if solutions_hybrid else []
    
    context = { 
        'swiper_images': swiper_images,
        'latest_news': latest_news, 
        'product_groups': product_groups,
        'products': products,
        'partner_logos': partner_logos,
        'images': images,
        'service_contents': service_contents,
        'sustainability_image': sustainability_image,
        'become_partner': become_partner,
        'solutions_hybrid': solutions_hybrid,
        'solutions_contents': solutions_contents,
    } 
     
    return render(request, 'home.html', context)

@csrf_protect
@require_POST
def submit_review(request):
    """Handle review submission for all pages"""
    try:
        # Get form data
        rating_value = request.POST.get('rating')
        first_name = request.POST.get('first_name', '').strip()
        surname = request.POST.get('surname', '').strip()
        email_address = request.POST.get('email_address', '').strip()
        summary = request.POST.get('summary', '').strip()
        review_text = request.POST.get('review', '').strip()
        agreement = request.POST.get('agreement')
        
        # Get the page user came from
        redirect_url = request.POST.get('redirect_url', '/')
        
        # Basic validations
        if not rating_value:
            messages.error(request, 'Please select a rating.')
            return redirect(redirect_url)
            
        if not agreement:
            messages.error(request, 'You must accept the agreement terms.')
            return redirect(redirect_url)
        
        # Check required fields
        required_fields = {
            'first_name': first_name,
            'surname': surname,
            'email_address': email_address,
            'summary': summary,
            'review': review_text
        }
        
        for field_name, field_value in required_fields.items():
            if not field_value:
                messages.error(request, 'All fields are required.')
                return redirect(redirect_url)

        # Spam check - same email in last 24 hours?
        recent_review = Review.objects.filter(
            email_address=email_address,
            created_at__gte=timezone.now() - timedelta(hours=24)
        ).first()
        
        if recent_review:
            messages.error(request, 'You have already submitted a review in the last 24 hours. Please wait.')
            return redirect(redirect_url)

        # Create review
        review = Review(
            first_name=first_name,
            surname=surname,
            email_address=email_address,
            summary=summary,
            review=review_text,
            rating=int(rating_value),
            ip_address=get_client_ip(request),
            is_approved=False
        )
        
        review.full_clean()
        review.save()
        
        messages.success(request, 'Thank you for your review! It will be published after approval.')
        return redirect(redirect_url)
        
    except ValueError:
        messages.error(request, 'Invalid rating value. Please select a rating.')
        return redirect(redirect_url)
    except ValidationError as e:
        error_message = ', '.join([str(error) for error in e.messages])
        messages.error(request, f'Validation error: {error_message}')
        return redirect(redirect_url)
    except Exception as e:
        messages.error(request, 'An error occurred while submitting your review. Please try again.')
        return redirect(redirect_url)

@csrf_protect
@require_POST
def submit_review_ajax(request):
    """AJAX review submission"""
    try:
        # Read JSON data
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.POST
        
        rating_value = data.get('rating')
        first_name = data.get('first_name', '').strip()
        surname = data.get('surname', '').strip()
        email_address = data.get('email_address', '').strip()
        summary = data.get('summary', '').strip()
        review_text = data.get('review', '').strip()
        agreement = data.get('agreement')
        
        # Validations
        if not rating_value:
            return JsonResponse({
                'success': False,
                'message': 'Please select a rating.'
            })
            
        if not agreement:
            return JsonResponse({
                'success': False,
                'message': 'You must accept the agreement terms.'
            })
        
        # Spam check
        recent_review = Review.objects.filter(
            email_address=email_address,
            created_at__gte=timezone.now() - timedelta(hours=24)
        ).first()
        
        if recent_review:
            return JsonResponse({
                'success': False,
                'message': 'You have already submitted a review in the last 24 hours.'
            })

        # Create review
        review = Review(
            first_name=first_name,
            surname=surname,
            email_address=email_address,
            summary=summary,
            review=review_text,
            rating=int(rating_value),
            ip_address=get_client_ip(request),
            is_approved=False
        )
        
        review.full_clean()
        review.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Thank you for your review! It will be published after approval.'
        })
        
    except ValidationError as e:
        return JsonResponse({
            'success': False,
            'message': ', '.join([str(error) for error in e.messages])
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'An error occurred. Please try again.'
        })

# Error handlers
def handler404(request, exception):
    return render(request, '404.html', status=404)

def handler500(request):
    return render(request, '500.html', status=500)

def handler403(request, exception):
    return render(request, '403.html', status=403)

def handler400(request, exception):
    return render(request, '400.html', status=400)