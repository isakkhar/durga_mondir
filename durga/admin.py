from django.contrib import admin
from .models import (
    Page, Event, Gallery, Contact, SiteSettings, Slider, 
    GalleryAlbum, GalleryPhoto, CommitteeMember, DurgaSangha, DurgaPujaCountdown, PujaDay, DonationInfo
)

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_published', 'show_in_menu', 'menu_order', 'created_at')
    list_filter = ('is_published', 'show_in_menu', 'created_at')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('is_published', 'show_in_menu', 'menu_order')
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new object
            obj.author = request.user
        super().save_model(request, obj, form, change)



@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_time', 'location', 'is_featured', 'is_active')
    list_filter = ('is_featured', 'is_active', 'date_time')
    search_fields = ('title', 'description', 'location')
    list_editable = ('is_featured', 'is_active')

class GalleryPhotoInline(admin.TabularInline):
    model = GalleryPhoto
    extra = 5
    fields = ('title', 'image', 'description')

@admin.register(GalleryAlbum)
class GalleryAlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_photos_count', 'is_featured', 'created_at')
    list_filter = ('is_featured', 'created_at')
    search_fields = ('title', 'description')
    list_editable = ('is_featured',)
    inlines = [GalleryPhotoInline]
    
    def get_photos_count(self, obj):
        return obj.get_photos_count()
    get_photos_count.short_description = 'ছবির সংখ্যা'

@admin.register(GalleryPhoto)
class GalleryPhotoAdmin(admin.ModelAdmin):
    list_display = ('title', 'album', 'created_at')
    list_filter = ('album', 'created_at')
    search_fields = ('title', 'album__title')

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('title', 'gallery_type', 'is_featured', 'created_at')
    list_filter = ('gallery_type', 'is_featured', 'created_at')
    search_fields = ('title', 'description')
    list_editable = ('is_featured',)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject')
    list_editable = ('is_read',)
    readonly_fields = ('name', 'email', 'phone', 'subject', 'message', 'created_at')

@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'order', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'subtitle', 'description')
    list_editable = ('is_active', 'order')
    ordering = ['order', '-created_at']
    
    fieldsets = (
        ('মূল তথ্য', {
            'fields': ('title', 'subtitle', 'description')
        }),
        ('ছবি ও বাটন', {
            'fields': ('image', 'button_text', 'button_link'),
            'description': 'সর্বোত্তম ফলাফলের জন্য 16:9 অনুপাতের ছবি (যেমন: 1920x1080) ব্যবহার করুন।'
        }),
        ('সেটিংস', {
            'fields': ('is_active', 'order')
        })
    )

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('সাইটের মূল তথ্য', {
            'fields': ('site_title', 'site_tagline', 'site_description')
        }),
        ('লোগো ও ছবি', {
            'fields': ('logo', 'favicon')
        }),
        ('যোগাযোগের তথ্য', {
            'fields': ('contact_email', 'contact_phone', 'address')
        }),
        ('সামাজিক মাধ্যম', {
            'fields': ('facebook_url', 'youtube_url')
        }),
        ('গুগল ম্যাপ', {
            'fields': ('google_map_url',),
            'description': 'গুগল ম্যাপের সম্পূর্ণ iframe embed কোড এখানে পেস্ট করুন। Google Maps > Share > Embed a map থেকে কোড কপি করুন।'
        }),
        ('প্রসাদ হল ও ভক্ত নিবাস', {
            'fields': ('prasad_hall_image',),
            'description': 'হোম পেইজে প্রদর্শিত প্রসাদ হল ও ভক্ত নিবাসের ছবি'
        }),
        ('ফুটার', {
            'fields': ('footer_text',)
        })
    )
    
    def has_add_permission(self, request):
        # Only allow one instance
        return not SiteSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(CommitteeMember)
class CommitteeMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'category', 'category_order', 'order', 'phone', 'is_active')
    list_filter = ('category', 'position', 'is_active')
    search_fields = ('name', 'position', 'phone')
    list_editable = ('category_order', 'order', 'is_active')
    ordering = ('category_order', 'order', 'name')
    
    fieldsets = (
        ('ব্যক্তিগত তথ্য', {
            'fields': ('name', 'position', 'image')
        }),
        ('ক্যাটাগরি', {
            'fields': ('category', 'category_order'),
            'description': 'একই ক্যাটাগরির সকল সদস্যকে একই category_order দিন। ছোট সংখ্যা আগে দেখাবে।'
        }),
        ('যোগাযোগ', {
            'fields': ('phone',)
        }),
        ('অন্যান্য', {
            'fields': ('order', 'is_active')
        }),
    )


@admin.register(DurgaSangha)
class DurgaSanghaAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'category', 'category_order', 'order', 'phone', 'is_active')
    list_filter = ('category', 'position', 'is_active')
    search_fields = ('name', 'position', 'phone', 'description')
    list_editable = ('category_order', 'order', 'is_active')
    ordering = ('category_order', 'order', 'name')
    
    fieldsets = (
        ('ব্যক্তিগত তথ্য', {
            'fields': ('name', 'position', 'image')
        }),
        ('ক্যাটাগরি', {
            'fields': ('category', 'category_order'),
            'description': 'একই ক্যাটাগরির সকল সদস্যকে একই category_order দিন। ছোট সংখ্যা আগে দেখাবে।'
        }),
        ('যোগাযোগ ও বিবরণ', {
            'fields': ('phone', 'description')
        }),
        ('অন্যান্য', {
            'fields': ('order', 'is_active')
        }),
    )


@admin.register(DurgaPujaCountdown)
class DurgaPujaCountdownAdmin(admin.ModelAdmin):
    list_display = ('title', 'target_date', 'days_remaining', 'is_active')
    list_filter = ('is_active', 'target_date')
    search_fields = ('title', 'message_before', 'message_after')
    list_editable = ('is_active',)
    
    fieldsets = (
        ('মূল তথ্য', {
            'fields': ('title', 'target_date', 'background_image')
        }),
        ('বার্তা', {
            'fields': ('message_before', 'message_after')
        }),
        ('সেটিংস', {
            'fields': ('is_active',)
        })
    )
    
    def days_remaining(self, obj):
        return f"{obj.days_remaining()} দিন"
    days_remaining.short_description = 'অবশিষ্ট দিন'


@admin.register(PujaDay)
class PujaDayAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'get_formatted_date', 'order', 'is_active')
    list_filter = ('is_active', 'date')
    search_fields = ('title', 'description')
    list_editable = ('order', 'is_active')
    ordering = ('order', 'date')
    
    fieldsets = (
        ('মূল তথ্য', {
            'fields': ('title', 'date', 'image')
        }),
        ('বিস্তারিত', {
            'fields': ('description',)
        }),
        ('সেটিংস', {
            'fields': ('order', 'is_active')
        })
    )
    
    def get_formatted_date(self, obj):
        return obj.get_formatted_date()
    get_formatted_date.short_description = 'বাংলা তারিখ'


@admin.register(DonationInfo)
class DonationInfoAdmin(admin.ModelAdmin):
    list_display = ('bank_account_number', 'bkash_number', 'nagad_number', 'is_active', 'updated_at')
    list_filter = ('is_active', 'created_at')
    list_editable = ('is_active',)
    
    fieldsets = (
        ('ব্যাংক তথ্য', {
            'fields': ('bank_name', 'bank_account_name', 'bank_account_number', 'bank_branch', 'bank_routing_number'),
            'description': 'ব্যাংক সম্পর্কিত সকল তথ্য এখানে দিন'
        }),
        ('মোবাইল ব্যাংকিং', {
            'fields': ('bkash_number', 'nagad_number', 'rocket_number'),
            'description': 'বিকাশ, নগদ, রকেট নাম্বার'
        }),
        ('অতিরিক্ত তথ্য', {
            'fields': ('other_payment_info', 'donation_note')
        }),
        ('সেটিংস', {
            'fields': ('is_active',)
        })
    )
    
    def has_add_permission(self, request):
        # Only allow one instance
        return not DonationInfo.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False
