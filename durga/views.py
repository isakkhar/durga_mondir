from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
import re
from .models import (
    Page, Event, Gallery, Contact, SiteSettings, Slider,
    GalleryAlbum, GalleryPhoto, CommitteeMember, DurgaSangha, DurgaPujaCountdown, PujaDay, DonationInfo
)

def get_site_context():
    """Get common site context for all views"""
    try:
        site_settings = SiteSettings.objects.first()
    except SiteSettings.DoesNotExist:
        site_settings = None
    
    menu_pages = Page.objects.filter(show_in_menu=True, is_published=True).order_by('menu_order')
    
    # Get active countdown for all pages
    countdown = DurgaPujaCountdown.objects.filter(is_active=True).first()
    
    # Convert countdown days to Bengali
    countdown_days_bangla = None
    if countdown and countdown.is_countdown_active():
        days = countdown.days_remaining()
        # Convert to Bengali digits
        bangla_digits = {'0': '০', '1': '১', '2': '২', '3': '৩', '4': '৪', 
                        '5': '৫', '6': '৬', '7': '৭', '8': '৮', '9': '৯'}
        countdown_days_bangla = ''.join(bangla_digits.get(d, d) for d in str(days))
    
    return {
        'site_settings': site_settings,
        'menu_pages': menu_pages,
        'countdown': countdown,
        'countdown_days_bangla': countdown_days_bangla,
    }

def home(request):
    context = get_site_context()
    
    # Get slider items
    slider_items = Slider.objects.filter(is_active=True).order_by('order')[:5]
    
    # Get featured content for homepage
    upcoming_events = Event.objects.filter(is_active=True).order_by('date_time')[:3]
    featured_gallery = Gallery.objects.filter(is_featured=True)[:6]
    
    # Get active countdown
    countdown = DurgaPujaCountdown.objects.filter(is_active=True).first()
    
    # Get gallery albums for showcase
    featured_albums = GalleryAlbum.objects.filter(is_featured=True)[:4]
    
    # Get puja days
    puja_days = PujaDay.objects.filter(is_active=True).order_by('order', 'date')[:6]
    
    # Get donation info
    donation_info = DonationInfo.objects.filter(is_active=True).first()
    
    context.update({
        'slider_items': slider_items,
        'upcoming_events': upcoming_events,
        'donation_info': donation_info,
        'featured_gallery': featured_gallery,
        'countdown': countdown,
        'featured_albums': featured_albums,
        'puja_days': puja_days,
    })
    
    return render(request, 'durga_mondir/home.html', context)

def page_detail(request, slug):
    page = get_object_or_404(Page, slug=slug, is_published=True)
    context = get_site_context()
    context['page'] = page
    return render(request, 'durga_mondir/page_detail.html', context)



def events(request):
    from django.utils import timezone
    from django.db.models import Case, When, Value, IntegerField
    
    context = get_site_context()
    
    now = timezone.now()
    
    # Get all events and order by upcoming first, then by date
    # Upcoming events in ascending order (nearest first)
    # Past events in descending order (most recent first)
    all_events = Event.objects.filter(is_active=True).annotate(
        is_upcoming_int=Case(
            When(date_time__gt=now, then=Value(0)),  # Upcoming = 0 (comes first)
            default=Value(1),  # Past = 1 (comes later)
            output_field=IntegerField(),
        )
    ).order_by('is_upcoming_int', 'date_time')
    
    # Filter upcoming/past events for list view
    filter_type = request.GET.get('filter', 'all')
    event_list = all_events
    
    if filter_type == 'upcoming':
        event_list = event_list.filter(date_time__gt=now)
    elif filter_type == 'past':
        event_list = event_list.filter(date_time__lt=now).order_by('-date_time')
    
    # Pagination for list view
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
    from collections import OrderedDict
    context = get_site_context()
    
    # Get all active committee members ordered by category_order, then member order
    all_members = CommitteeMember.objects.filter(is_active=True).order_by('category_order', 'order', 'name')
    
    # Group members by category dynamically while preserving order
    members_by_category = OrderedDict()
    for member in all_members:
        category = member.category
        if category not in members_by_category:
            members_by_category[category] = []
        members_by_category[category].append(member)
    
    context.update({
        'members_by_category': members_by_category,
    })
    
    return render(request, 'durga_mondir/committee.html', context)


def durga_sangha(request):
    """Durga Sangha members view"""
    from collections import OrderedDict
    context = get_site_context()
    
    # Get all active durga sangha members ordered by category_order, then member order
    all_members = DurgaSangha.objects.filter(is_active=True).order_by('category_order', 'order', 'name')
    
    # Group members by category dynamically while preserving order
    members_by_category = OrderedDict()
    for member in all_members:
        category = member.category
        if category not in members_by_category:
            members_by_category[category] = []
        members_by_category[category].append(member)
    
    context.update({
        'members_by_category': members_by_category,
    })
    
    return render(request, 'durga_mondir/durga_sangha.html', context)