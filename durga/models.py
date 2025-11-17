from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image
import os

# Page Management Models
class Page(models.Model):
    title = models.CharField(max_length=200, verbose_name="পাতার শিরোনাম")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="URL স্লাগ")
    content = models.TextField(verbose_name="বিষয়বস্তু")
    meta_description = models.CharField(max_length=255, blank=True, verbose_name="মেটা বিবরণ")
    featured_image = models.ImageField(upload_to='pages/', blank=True, null=True, verbose_name="প্রধান ছবি")
    is_published = models.BooleanField(default=True, verbose_name="প্রকাশিত")
    show_in_menu = models.BooleanField(default=False, verbose_name="মেনুতে দেখান")
    menu_order = models.IntegerField(default=0, verbose_name="মেনু ক্রম")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, verbose_name="মূল পাতা")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="তৈরির তারিখ")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="সর্বশেষ আপডেট")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="লেখক")
    
    class Meta:
        verbose_name = "পাতা"
        verbose_name_plural = "পাতাসমূহ"
        ordering = ['menu_order', 'title']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('durga:page_detail', kwargs={'slug': self.slug})



# Events Model
class Event(models.Model):
    title = models.CharField(max_length=200, verbose_name="অনুষ্ঠানের নাম")
    description = models.TextField(verbose_name="বিবরণ")
    date_time = models.DateTimeField(verbose_name="তারিখ ও সময়")
    location = models.CharField(max_length=200, verbose_name="স্থান")
    featured_image = models.ImageField(upload_to='events/', blank=True, null=True, verbose_name="প্রধান ছবি")
    is_featured = models.BooleanField(default=False, verbose_name="বৈশিষ্ট্যযুক্ত")
    is_active = models.BooleanField(default=True, verbose_name="সক্রিয়")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="তৈরির তারিখ")
    
    class Meta:
        verbose_name = "অনুষ্ঠান"
        verbose_name_plural = "অনুষ্ঠানসমূহ"
        ordering = ['date_time']
    
    def __str__(self):
        return self.title
    
    @property
    def is_upcoming(self):
        return self.date_time > timezone.now()

# Gallery Model
class GalleryAlbum(models.Model):
    title = models.CharField(max_length=200, verbose_name="অ্যালবামের নাম")
    description = models.TextField(blank=True, verbose_name="বিবরণ")
    cover_image = models.ImageField(upload_to='albums/covers/', blank=True, null=True, verbose_name="কভার ছবি")
    is_featured = models.BooleanField(default=False, verbose_name="বৈশিষ্ট্যযুক্ত")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="তৈরির তারিখ")
    
    class Meta:
        verbose_name = "গ্যালারি অ্যালবাম"
        verbose_name_plural = "গ্যালারি অ্যালবামসমূহ"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def get_photos_count(self):
        return self.photos.count()

class GalleryPhoto(models.Model):
    album = models.ForeignKey(GalleryAlbum, on_delete=models.CASCADE, related_name='photos', verbose_name="অ্যালবাম")
    title = models.CharField(max_length=200, blank=True, verbose_name="ছবির নাম")
    image = models.ImageField(upload_to='albums/photos/', verbose_name="ছবি")
    description = models.TextField(blank=True, verbose_name="বিবরণ")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="আপলোড তারিখ")
    
    class Meta:
        verbose_name = "গ্যালারি ছবি"
        verbose_name_plural = "গ্যালারি ছবিসমূহ"
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.album.title} - {self.title or 'ছবি'}"

class Gallery(models.Model):
    GALLERY_TYPES = [
        ('photo', 'ছবি'),
        ('video', 'ভিডিও'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="শিরোনাম")
    description = models.TextField(blank=True, verbose_name="বিবরণ")
    gallery_type = models.CharField(max_length=10, choices=GALLERY_TYPES, default='photo', verbose_name="গ্যালারির ধরণ")
    image = models.ImageField(upload_to='gallery/', blank=True, null=True, verbose_name="ছবি")
    video_url = models.URLField(blank=True, verbose_name="ভিডিও লিংক")
    is_featured = models.BooleanField(default=False, verbose_name="বৈশিষ্ট্যযুক্ত")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="তৈরির তারিখ")
    
    class Meta:
        verbose_name = "গ্যালারি"
        verbose_name_plural = "গ্যালারিসমূহ"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def get_youtube_embed_url(self):
        """Convert YouTube watch URL to embed URL"""
        if self.video_url and ('youtube.com' in self.video_url or 'youtu.be' in self.video_url):
            import re
            # Extract video ID from various YouTube URL formats
            patterns = [
                r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)',
            ]
            
            for pattern in patterns:
                match = re.search(pattern, self.video_url)
                if match:
                    video_id = match.group(1)
                    return f'https://www.youtube.com/embed/{video_id}'
        
        return self.video_url

# Contact/Donation Model
class Contact(models.Model):
    name = models.CharField(max_length=100, verbose_name="নাম")
    email = models.EmailField(verbose_name="ইমেইল")
    phone = models.CharField(max_length=20, blank=True, verbose_name="ফোন")
    subject = models.CharField(max_length=200, verbose_name="বিষয়")
    message = models.TextField(verbose_name="বার্তা")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="তৈরির তারিখ")
    is_read = models.BooleanField(default=False, verbose_name="পড়া হয়েছে")
    
    class Meta:
        verbose_name = "যোগাযোগ"
        verbose_name_plural = "যোগাযোগসমূহ"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.subject}"

# Slider Model
class Slider(models.Model):
    title = models.CharField(max_length=200, blank=True, verbose_name="শিরোনাম")
    subtitle = models.CharField(max_length=300, blank=True, verbose_name="উপশিরোনাম")
    description = models.TextField(blank=True, verbose_name="বিবরণ")
    image = models.ImageField(upload_to='slider/', verbose_name="স্লাইডার ছবি")
    button_text = models.CharField(max_length=50, blank=True, verbose_name="বাটনের টেক্সট")
    button_link = models.CharField(max_length=200, blank=True, verbose_name="বাটনের লিংক")
    is_active = models.BooleanField(default=True, verbose_name="সক্রিয়")
    order = models.IntegerField(default=0, verbose_name="ক্রম")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="তৈরির তারিখ")
    
    class Meta:
        verbose_name = "স্লাইডার"
        verbose_name_plural = "স্লাইডারসমূহ"
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        if self.image:
            # Open image
            img = Image.open(self.image.path)
            
            # Set desired dimensions for slider (16:9 aspect ratio)
            output_size = (1920, 1080)  # Full HD resolution
            
            # Calculate crop dimensions to maintain aspect ratio
            img_width, img_height = img.size
            target_ratio = output_size[0] / output_size[1]  # 16:9 = 1.777
            img_ratio = img_width / img_height
            
            if img_ratio > target_ratio:
                # Image is wider, crop width
                new_width = int(img_height * target_ratio)
                left = (img_width - new_width) // 2
                top = 0
                right = left + new_width
                bottom = img_height
            else:
                # Image is taller, crop height
                new_height = int(img_width / target_ratio)
                left = 0
                top = (img_height - new_height) // 2
                right = img_width
                bottom = top + new_height
            
            # Crop and resize
            img = img.crop((left, top, right, bottom))
            img = img.resize(output_size, Image.Resampling.LANCZOS)
            
            # Save the processed image
            img.save(self.image.path, quality=85, optimize=True)

# Site Settings Model
class SiteSettings(models.Model):
    site_title = models.CharField(max_length=200, default="দুর্গা মন্দির", verbose_name="সাইটের নাম")
    site_tagline = models.CharField(max_length=200, blank=True, verbose_name="সাইটের স্লোগান")
    site_description = models.TextField(blank=True, verbose_name="সাইটের বিবরণ")
    logo = models.ImageField(upload_to='settings/', blank=True, null=True, verbose_name="লোগো")
    favicon = models.ImageField(upload_to='settings/', blank=True, null=True, verbose_name="ফ্যাভিকন")
    contact_email = models.EmailField(blank=True, verbose_name="যোগাযোগের ইমেইল")
    contact_phone = models.CharField(max_length=20, blank=True, verbose_name="যোগাযোগের ফোন")
    address = models.TextField(blank=True, verbose_name="ঠিকানা")
    facebook_url = models.URLField(blank=True, verbose_name="ফেসবুক পাতা")
    youtube_url = models.URLField(blank=True, verbose_name="ইউটিউব চ্যানেল")
    google_map_url = models.TextField(blank=True, verbose_name="গুগল ম্যাপ এম্বেড URL", 
                                      help_text="গুগল ম্যাপের এম্বেড কোড এখানে পেস্ট করুন")
    footer_text = models.TextField(blank=True, verbose_name="ফুটার টেক্সট")
    
    # প্রসাদ হল ও ভক্ত নিবাস
    prasad_hall_image = models.ImageField(upload_to='settings/', blank=True, null=True, 
                                         verbose_name="প্রসাদ হল ও ভক্ত নিবাস ছবি",
                                         help_text="হোম পেইজে প্রদর্শিত হবে")
    
    class Meta:
        verbose_name = "সাইট সেটিংস"
        verbose_name_plural = "সাইট সেটিংস"
    
    def __str__(self):
        return self.site_title

class CommitteeMember(models.Model):
    name = models.CharField(max_length=100, verbose_name="নাম")
    position = models.CharField(max_length=100, verbose_name="পদবী")
    category = models.CharField(max_length=100, default='কার্যনির্বাহী কমিটি', verbose_name="ক্যাটাগরি", 
                                help_text="যেমন: কার্যনির্বাহী কমিটি, উপদেষ্টা পরিষদ, বিশেষ সদস্য")
    category_order = models.PositiveIntegerField(default=0, verbose_name="ক্যাটাগরির ক্রম",
                                                  help_text="ছোট সংখ্যা আগে দেখাবে (যেমন: 1, 2, 3...)")
    image = models.ImageField(upload_to='committee/', verbose_name="ছবি")
    phone = models.CharField(max_length=20, blank=True, verbose_name="মোবাইল নাম্বার")
    order = models.PositiveIntegerField(default=0, verbose_name="সদস্যের ক্রম",
                                        help_text="একই ক্যাটাগরির মধ্যে সদস্যের ক্রম")
    is_active = models.BooleanField(default=True, verbose_name="সক্রিয়")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="যোগ করার তারিখ")
    
    class Meta:
        verbose_name = "কমিটির সদস্য"
        verbose_name_plural = "কমিটির সদস্যবর্গ"
        ordering = ['category_order', 'order', 'name']
    
    def __str__(self):
        return f"{self.name} - {self.position}"


class DurgaSangha(models.Model):
    name = models.CharField(max_length=100, verbose_name="নাম")
    position = models.CharField(max_length=100, verbose_name="পদবী")
    category = models.CharField(max_length=100, default='দুর্গা সংঘ', verbose_name="ক্যাটাগরি", 
                                help_text="যেমন: দুর্গা সংঘ, উপদেষ্টা, বিশেষ সদস্য")
    category_order = models.PositiveIntegerField(default=0, verbose_name="ক্যাটাগরির ক্রম",
                                                  help_text="ছোট সংখ্যা আগে দেখাবে (যেমন: 1, 2, 3...)")
    image = models.ImageField(upload_to='durga_sangha/', verbose_name="ছবি")
    phone = models.CharField(max_length=20, blank=True, verbose_name="মোবাইল নাম্বার")
    description = models.TextField(blank=True, null=True, verbose_name="বিবরণ")
    order = models.PositiveIntegerField(default=0, verbose_name="সদস্যের ক্রম",
                                        help_text="একই ক্যাটাগরির মধ্যে সদস্যের ক্রম")
    is_active = models.BooleanField(default=True, verbose_name="সক্রিয়")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="যোগ করার তারিখ")
    
    class Meta:
        verbose_name = "দুর্গা সংঘের সদস্য"
        verbose_name_plural = "দুর্গা সংঘের সদস্যবর্গ"
        ordering = ['category_order', 'order', 'name']
    
    def __str__(self):
        return f"{self.name} - {self.position}"


class DurgaPujaCountdown(models.Model):
    title = models.CharField(max_length=200, default="দুর্গা পূজা", verbose_name="অনুষ্ঠানের নাম")
    target_date = models.DateTimeField(verbose_name="লক্ষ্য তারিখ")
    background_image = models.ImageField(upload_to='countdown/', blank=True, null=True, verbose_name="ব্যাকগ্রাউন্ড ছবি")
    is_active = models.BooleanField(default=True, verbose_name="সক্রিয়")
    message_before = models.CharField(max_length=100, default="মা আসছে", verbose_name="পূর্বের বার্তা")
    message_after = models.CharField(max_length=100, default="দিন পরে", verbose_name="পরের বার্তা")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="তৈরির তারিখ")
    
    class Meta:
        verbose_name = "দুর্গা পূজা কাউন্টডাউন"
        verbose_name_plural = "দুর্গা পূজা কাউন্টডাউনসমূহ"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.target_date.strftime('%d/%m/%Y')}"
    
    def days_remaining(self):
        from datetime import datetime
        now = timezone.now()
        if self.target_date > now:
            diff = self.target_date - now
            return diff.days
        else:
            return 0
    
    def is_countdown_active(self):
        return self.is_active and self.days_remaining() > 0


class PujaDay(models.Model):
    title = models.CharField(max_length=100, verbose_name="পূজার দিনের নাম")
    date = models.DateField(verbose_name="তারিখ")
    image = models.ImageField(upload_to='puja_days/', verbose_name="ছবি")
    description = models.TextField(blank=True, verbose_name="বিবরণ")
    is_active = models.BooleanField(default=True, verbose_name="সক্রিয়")
    order = models.PositiveIntegerField(default=0, verbose_name="ক্রম")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="তৈরির তারিখ")
    
    class Meta:
        verbose_name = "পূজার দিন"
        verbose_name_plural = "পূজার দিনসমূহ"
        ordering = ['order', 'date']
    
    def __str__(self):
        return f"{self.title} - {self.date.strftime('%d %B')}"
    
    def get_formatted_date(self):
        months = {
            1: 'জানুয়ারি', 2: 'ফেব্রুয়ারি', 3: 'মার্চ', 4: 'এপ্রিল',
            5: 'মে', 6: 'জুন', 7: 'জুলাই', 8: 'আগস্ট',
            9: 'সেপ্টেম্বর', 10: 'অক্টোবর', 11: 'নভেম্বর', 12: 'ডিসেম্বর'
        }
        return f"{self.date.day:02d} {months[self.date.month]}"
    
    def get_formatted_date_with_day(self):
        months = {
            1: 'জানুয়ারি', 2: 'ফেব্রুয়ারি', 3: 'মার্চ', 4: 'এপ্রিল',
            5: 'মে', 6: 'জুন', 7: 'জুলাই', 8: 'আগস্ট',
            9: 'সেপ্টেম্বর', 10: 'অক্টোবর', 11: 'নভেম্বর', 12: 'ডিসেম্বর'
        }
        days = {
            0: 'সোমবার', 1: 'মঙ্গলবার', 2: 'বুধবার', 3: 'বৃহস্পতিবার',
            4: 'শুক্রবার', 5: 'শনিবার', 6: 'রবিবার'
        }
        # Convert date parts to Bengali (no leading zero for single digit dates)
        bangla_digits = {'0': '০', '1': '১', '2': '২', '3': '৩', '4': '৪', 
                        '5': '৫', '6': '৬', '7': '৭', '8': '৮', '9': '৯'}
        
        day_name = days[self.date.weekday()]
        # Don't use leading zero for day
        day = ''.join(bangla_digits.get(d, d) for d in str(self.date.day))
        month = months[self.date.month]
        year = ''.join(bangla_digits.get(d, d) for d in str(self.date.year))
        
        return f"{day_name} | {day} {month}, {year}"


class DonationInfo(models.Model):
    """দান/অনুদান সংক্রান্ত তথ্য"""
    bank_name = models.CharField(max_length=200, verbose_name="ব্যাংকের নাম", blank=True)
    bank_account_name = models.CharField(max_length=200, verbose_name="একাউন্ট নাম", blank=True)
    bank_account_number = models.CharField(max_length=100, verbose_name="ব্যাংক একাউন্ট নাম্বার", blank=True)
    bank_branch = models.CharField(max_length=200, verbose_name="ব্যাংক শাখা", blank=True)
    bank_routing_number = models.CharField(max_length=50, verbose_name="রাউটিং নাম্বার", blank=True)
    
    bkash_number = models.CharField(max_length=20, verbose_name="বিকাশ নাম্বার", blank=True,
                                    help_text="যেমন: ০১৭১১-১২৩৪৫৬")
    nagad_number = models.CharField(max_length=20, verbose_name="নগদ নাম্বার", blank=True,
                                    help_text="যেমন: ০১৭১১-১২৩৪৫৬")
    rocket_number = models.CharField(max_length=20, verbose_name="রকেট নাম্বার", blank=True,
                                     help_text="যেমন: ০১৭১১-১২৩৪৫৬")
    
    other_payment_info = models.TextField(verbose_name="অন্যান্য পেমেন্ট তথ্য", blank=True,
                                         help_text="অন্য কোন পেমেন্ট পদ্ধতি থাকলে এখানে লিখুন")
    
    donation_note = models.TextField(verbose_name="দাতাদের জন্য বিশেষ বার্তা", blank=True,
                                     help_text="যেমন: দানের জন্য ধন্যবাদ বার্তা বা নির্দেশনা")
    
    is_active = models.BooleanField(default=True, verbose_name="সক্রিয়")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="তৈরির তারিখ")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="আপডেটের তারিখ")
    
    class Meta:
        verbose_name = "দান/অনুদান তথ্য"
        verbose_name_plural = "দান/অনুদান তথ্য"
    
    def __str__(self):
        return "দান/অনুদান তথ্য"
