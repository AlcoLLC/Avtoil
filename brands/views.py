import os
import mimetypes
from django.http import FileResponse, Http404
from django.shortcuts import render, get_object_or_404
from .models import Brand_Portal, Brand_Portal_Content

def brand_portal_list(request):
    brand = Brand_Portal.objects.last()
    brand_contents = []
    if brand:
        brand_contents = Brand_Portal_Content.objects.filter(
            brand_portal=brand
        ).order_by('order', '-created_at') 
    
    context = {
        'brand': brand,
        'brand_contents': brand_contents,
    }
    
    return render(request, 'brand_portal.html', context)



def view_brand_content_pdf(request, content_id):
    content = get_object_or_404(Brand_Portal_Content, id=content_id)
    
    if not content.pdf or not os.path.exists(content.pdf.path):
        raise Http404("PDF dosyası bulunamadı.")

    mime_type, _ = mimetypes.guess_type(content.pdf.path)
    if not mime_type:
        mime_type = 'application/pdf'

    response = FileResponse(open(content.pdf.path, 'rb'), content_type=mime_type)
    response['Content-Disposition'] = f'inline; filename="{os.path.basename(content.pdf.name)}"'

    return response