from .models import Review

def review_context(request):
    """
    Global context processor for reviews
    This will be available in all templates
    """
    return {
        'approved_reviews': Review.objects.filter(is_approved=True).order_by('-approved_at')[:10],
        'review_count': Review.objects.filter(is_approved=True).count(),
    }