from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
import re
from .models import (
    Page, Event, Gallery, Contact, SiteSettings, Slider,
    GalleryAlbum, GalleryPhoto, CommitteeMember, DurgaSangha
)

def get_site_context():
    """Get common site context for all views"""
    try:
        site_settings = SiteSettings.objects.first()
    except SiteSettings.DoesNotExist:
        site_settings = None
    
    menu_pages = Page.objects.filter(show_in_menu=True, is_published=True).order_by('menu_order')
    
    return {
        'site_settings': site_settings,
        'menu_pages': menu_pages,
    }

def home(request):
    context = get_site_context()
    
    # Get slider items
    slider_items = Slider.objects.filter(is_active=True).order_by('order')[:5]
    
    # Get featured content for homepage
    upcoming_events = Event.objects.filter(is_active=True).order_by('date_time')[:3]
    featured_gallery = Gallery.objects.filter(is_featured=True)[:6]
    
    context.update({
        'slider_items': slider_items,
        'upcoming_events': upcoming_events,
        'featured_gallery': featured_gallery,
    })
    
    return render(request, 'durga_mondir/home.html', context)

def page_detail(request, slug):
    page = get_object_or_404(Page, slug=slug, is_published=True)
    context = get_site_context()
    context['page'] = page
    return render(request, 'durga_mondir/page_detail.html', context)



def events(request):
    context = get_site_context()
    
    event_list = Event.objects.filter(is_active=True).order_by('date_time')
    
    # Filter upcoming/past events
    filter_type = request.GET.get('filter', 'all')
    if filter_type == 'upcoming':
        from django.utils import timezone
        event_list = event_list.filter(date_time__gt=timezone.now())
    elif filter_type == 'past':
        from django.utils import timezone
        event_list = event_list.filter(date_time__lt=timezone.now())
    
    # Pagination
    paginator = Paginator(event_list, 6)  # Show 6 events per page
    page_number = request.GET.get('page')
    events_page = paginator.get_page(page_number)
    
    context.update({
        'events': events_page,
        'filter_type': filter_type,
    })
    
    return render(request, 'durga_mondir/events.html', context)

def gallery_view(request):
    context = get_site_context()
    
    # Get gallery albums
    albums = GalleryAlbum.objects.all().order_by('-created_at')
    
    # Pagination for albums
    paginator = Paginator(albums, 12)  # Show 12 albums per page
    page_number = request.GET.get('page')
    albums_page = paginator.get_page(page_number)
    
    context.update({
        'albums': albums_page,
    })
    
    return render(request, 'durga_mondir/gallery.html', context)

def album_detail(request, album_id):
    """Album detail view with infinite scroll for photos"""
    context = get_site_context()
    album = get_object_or_404(GalleryAlbum, id=album_id)
    
    # Get photos for this album
    photos = album.photos.all().order_by('created_at')
    
    # For AJAX requests (infinite scroll)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        page = int(request.GET.get('page', 1))
        paginator = Paginator(photos, 20)  # 20 photos per load
        photos_page = paginator.get_page(page)
        
        from django.http import JsonResponse
        
        photos_data = []
        for photo in photos_page:
            photos_data.append({
                'id': photo.id,
                'title': photo.title,
                'image_url': photo.image.url,
                'description': photo.description or '',
            })
        
        return JsonResponse({
            'photos': photos_data,
            'has_next': photos_page.has_next(),
            'next_page': photos_page.next_page_number() if photos_page.has_next() else None
        })
    
    # Initial page load - first 20 photos
    paginator = Paginator(photos, 20)
    photos_page = paginator.get_page(1)
    
    context.update({
        'album': album,
        'photos': photos_page,
    })
    
    return render(request, 'durga_mondir/album_detail.html', context)

def contact(request):
    context = get_site_context()
    
    if request.method == 'POST':
        # Handle contact form submission
        contact_form = Contact(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone', ''),
            subject=request.POST.get('subject'),
            message=request.POST.get('message')
        )
        contact_form.save()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'message': 'আপনার বার্তা সফলভাবে পাঠানো হয়েছে!'})
        else:
            context['success_message'] = 'আপনার বার্তা সফলভাবে পাঠানো হয়েছে!'
    
    return render(request, 'durga_mondir/contact.html', context)

def committee(request):
    """Committee members view"""
    context = get_site_context()
    
    # Get all active committee members ordered by position priority
    members = CommitteeMember.objects.filter(is_active=True).order_by('order', 'name')
    
    context.update({
        'members': members,
    })
    
    return render(request, 'durga_mondir/committee.html', context)


def durga_sangha(request):
    """Durga Sangha members view"""
    context = get_site_context()
    
    # Get all active durga sangha members ordered by position priority
    members = DurgaSangha.objects.filter(is_active=True).order_by('order', 'name')
    
    context.update({
        'members': members,
    })
    
    return render(request, 'durga_mondir/durga_sangha.html', context)