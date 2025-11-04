# Create sample data for testing
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from durga.models import (
    SiteSettings, Page, Event, Gallery, Slider
)
from datetime import datetime, timedelta
from django.utils import timezone

class Command(BaseCommand):
    help = 'Create sample data for the website'

    def handle(self, *args, **options):
        # Create or get admin user
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@durgamondir.com',
                'is_staff': True,
                'is_superuser': True,
            }
        )

        # Create site settings
        site_settings, created = SiteSettings.objects.get_or_create(
            defaults={
                'site_title': 'শ্রীশ্রী দুর্গা মন্দির',
                'site_tagline': 'হরে কৃষ্ণ হরে কৃষ্ণ কৃষ্ণ কৃষ্ণ হরে হরে। হরে রাম হরে রাম রাম রাম হরে হরে।।',
                'site_description': 'এই ধাম/আশ্রমটি হইল এমন একটি আধ্যাত্মিক কেন্দ্র যেখানে যে কোনো ধর্মবিশ্বাসী বা একেবারেই বিশ্বাস নাই এমন মানুষও প্রতিফলিত হইতে, প্রশ্ন করিতে, আলোচনা শুনিতে, প্রার্থনা করিতে, হরিনাম করিতে / শুনিতে, ধ্যান, জ্ঞান এবং নিজেকে পরের সেবায় উৎসর্গ করিতে আসেন।',
                'contact_email': 'contact@durgamondir.com',
                'contact_phone': '+88012345678',
                'address': 'দুর্গা মন্দির, ঢাকা, বাংলাদেশ',
                'facebook_url': 'https://www.facebook.com/durgamondir',
                'youtube_url': 'https://www.youtube.com/@durgamondir',
                'footer_text': 'সর্ব্বপ্রথমে সেই শ্রীগুরুর শ্রীপাদপদ্মে সাষ্টাঙ্গে প্রণিপাত করিতেছি।'
            }
        )



        # Create pages
        pages_data = [
            {
                'title': 'শ্রীশ্রী গুরুদেব',
                'slug': 'sri-sri-gurudev',
                'content': '''শ্রীশ্রীঠাকুর রামচন্দ্রদেব হইলেন এই আশ্রমের অভিভাবক। মরভূমের বিষম বিপাক হইতে স্বগণকে উদ্ধার করিয়া লইবার জন্যই লোকালয়ে প্রকট হইয়াছিলেন ভগবানের অবতার পরম দয়াল শ্রীশ্রী রামঠাকুর।

নরদেহে আবির্ভূত হইয়া জীবের পরম হিতৈষীর মূর্ত্তিতে স্বগণের গৃহে গৃহে, নিকটে নিকটে ঘুরিয়া সকলকে একান্ত আপন জন হিসাবে আকর্ষণ করিয়া প্রাণের ডোরে নিত্য সত্য ভগবৎপদে গাঁথিয়া নিয়াছেন।

অনিত্য সংসারের ভ্রান্ত আসক্তি হইতে উদ্ধারের পথে টানিয়া লইয়াছেন।''',
                'show_in_menu': True,
                'menu_order': 1
            },
            {
                'title': 'মন্দিরের ইতিহাস',
                'slug': 'temple-history',
                'content': '''আমাদের মন্দিরের একটি সমৃদ্ধ ইতিহাস রয়েছে যা শতাব্দীর পর শতাব্দী ধরে বিস্তৃত। এই পবিত্র স্থানটি আধ্যাত্মিক সাধনা এবং ভক্তিমূলক কার্যকলাপের কেন্দ্রবিন্দু হিসেবে কাজ করেছে।

মন্দিরটি স্থানীয় সম্প্রদায়ের দ্বারা প্রতিষ্ঠিত হয়েছিল এবং কয়েক দশক ধরে এটি ধর্মপ্রাণ মানুষদের আকর্ষণ করেছে।''',
                'show_in_menu': True,
                'menu_order': 2
            },
            {
                'title': 'সেবা কার্যক্রম',
                'slug': 'seva-programs',
                'content': '''আমাদের মন্দিরে বিভিন্ন ধরনের সেবা কার্যক্রম পরিচালিত হয়:

১. দৈনিক পূজা ও আরতি
২. ধর্মীয় শিক্ষা কার্যক্রম  
৩. দাতব্য কার্যক্রম
৪. সামাজিক সেবা
৫. আধ্যাত্মিক আলোচনা সভা

সবাইকে এই সেবা কার্যক্রমে অংশগ্রহণের জন্য আমন্ত্রণ জানানো হচ্ছে।''',
                'show_in_menu': True,
                'menu_order': 3
            }
        ]

        for page_data in pages_data:
            page, created = Page.objects.get_or_create(
                slug=page_data['slug'],
                defaults={
                    'title': page_data['title'],
                    'content': page_data['content'],
                    'show_in_menu': page_data['show_in_menu'],
                    'menu_order': page_data['menu_order'],
                    'author': admin_user,
                    'is_published': True
                }
            )



        # Create events
        events_data = [
            {
                'title': 'দুর্গা পূজা ২০২৫',
                'description': 'আমাদের মন্দিরে পালিত হবে পবিত্র দুর্গা পূজা। পাঁচদিনব্যাপী এই উৎসবে সকলকে স্বাগত জানানো হচ্ছে।',
                'date_time': timezone.now() + timedelta(days=30),
                'location': 'মূল মন্দির প্রাঙ্গণ',
                'is_featured': True
            },
            {
                'title': 'সাপ্তাহিক সৎসঙ্গ',
                'description': 'প্রতি শুক্রবার সন্ধ্যায় অনুষ্ঠিত হয় আধ্যাত্মিক আলোচনা ও হরিনাম সংকীর্তন।',
                'date_time': timezone.now() + timedelta(days=5),
                'location': 'সৎসঙ্গ হল',
                'is_featured': False
            },
            {
                'title': 'গীতা পাঠ অনুষ্ঠান',
                'description': 'ভগবদ্গীতার নিয়মিত পাঠ ও আলোচনা। সবার জন্য উন্মুক্ত।',
                'date_time': timezone.now() + timedelta(days=7),
                'location': 'পাঠাগার',
                'is_featured': False
            }
        ]

        for event_data in events_data:
            event, created = Event.objects.get_or_create(
                title=event_data['title'],
                defaults={
                    'description': event_data['description'],
                    'date_time': event_data['date_time'],
                    'location': event_data['location'],
                    'is_featured': event_data['is_featured'],
                    'is_active': True
                }
            )

        # Create gallery items
        gallery_data = [
            {
                'title': 'দুর্গা পূজার মূহূর্ত',
                'description': 'গত বছরের দুর্গা পূজার কিছু স্মৃতিময় মূহূর্ত',
                'gallery_type': 'photo',
                'is_featured': True
            },
            {
                'title': 'হরিনাম সংকীর্তন',
                'description': 'সাপ্তাহিক হরিনাম সংকীর্তনের দৃশ্য',
                'gallery_type': 'photo',
                'is_featured': True
            },
            {
                'title': 'আরতি অনুষ্ঠান',
                'description': 'দৈনন্দিন আরতি অনুষ্ঠানের ভিডিও',
                'gallery_type': 'video',
                'video_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
                'is_featured': False
            }
        ]

        for gallery_item in gallery_data:
            item, created = Gallery.objects.get_or_create(
                title=gallery_item['title'],
                defaults={
                    'description': gallery_item['description'],
                    'gallery_type': gallery_item['gallery_type'],
                    'video_url': gallery_item.get('video_url', ''),
                    'is_featured': gallery_item['is_featured']
                }
            )

        # Create slider items
        slider_data = [
            {
                'title': 'স্বাগতম শ্রীশ্রী দুর্গা মন্দিরে',
                'subtitle': 'হরে কৃষ্ণ হরে কৃষ্ণ কৃষ্ণ কৃষ্ণ হরে হরে। হরে রাম হরে রাম রাম রাম হরে হরে।।',
                'description': 'আমাদের পবিত্র মন্দিরে আপনাদের স্বাগত জানাই। এখানে আপনি পাবেন আধ্যাত্মিক শান্তি ও মানসিক প্রশান্তি।',
                'button_text': 'আরও জানুন',
                'button_link': '/page/sri-sri-gurudev/',
                'order': 1
            },
            {
                'title': 'শ্রীশ্রী গুরুদেবের আশীর্বাদ',
                'subtitle': 'ওঁ অজ্ঞান-তিমিরান্দ্বস্য জ্ঞানাঞ্জনশলাকায়া',
                'description': 'শ্রীগুরুর কৃপায় আমরা পাই আধ্যাত্মিক জ্ঞান এবং জীবনের সঠিক পথ নির্দেশনা।',
                'button_text': 'গুরুদেব সম্পর্কে',
                'button_link': '/page/sri-sri-gurudev/',
                'order': 2
            },
            {
                'title': 'দৈনন্দিন পূজা ও সেবা',
                'subtitle': 'প্রতিদিনের আরতি ও হরিনাম সংকীর্তন',
                'description': 'আমাদের মন্দিরে নিয়মিত পূজা-অর্চনা এবং আধ্যাত্মিক কার্যক্রম পরিচালিত হয়।',
                'button_text': 'সময়সূচী দেখুন',
                'button_link': '/page/seva-programs/',
                'order': 3
            }
        ]

        for slider_item in slider_data:
            slider, created = Slider.objects.get_or_create(
                title=slider_item['title'],
                defaults={
                    'subtitle': slider_item['subtitle'],
                    'description': slider_item['description'],
                    'button_text': slider_item['button_text'],
                    'button_link': slider_item['button_link'],
                    'order': slider_item['order'],
                    'is_active': True
                }
            )

        # Create Gallery Albums
        from durga.models import GalleryAlbum, GalleryPhoto
        
        albums_data = [
            {
                'title': 'দুর্গাপূজা ২০২৪',
                'description': 'এবারের দুর্গাপূজার সুন্দর মুহূর্তগুলি।'
            },
            {
                'title': 'আশ্রমের দৈনন্দিন কার্যক্রম',
                'description': 'প্রতিদিনের পূজা-অর্চনা ও আধ্যাত্মিক কার্যক্রমের ছবি।'
            },
            {
                'title': 'বিশেষ অনুষ্ঠান',
                'description': 'বিভিন্ন উৎসব ও বিশেষ আধ্যাত্মিক অনুষ্ঠানের স্মৃতি।'
            },
            {
                'title': 'সেবামূলক কার্যক্রম',
                'description': 'সমাজসেবা ও দাতব্য কার্যক্রমের ছবি।'
            }
        ]

        for album_data in albums_data:
            album, created = GalleryAlbum.objects.get_or_create(
                title=album_data['title'],
                defaults={
                    'description': album_data['description'],
                    'is_featured': True
                }
            )
            
            if created:
                self.stdout.write(f"Created album: {album.title}")

        # Create Committee Members
        from durga.models import CommitteeMember, DurgaSangha
        
        committee_members = [
            {
                'name': 'শ্রী রামেশ চন্দ্র শর্মা',
                'position': 'সভাপতি', 
                'phone': '০১৭১১-২৩৪৫৬১',
                'order': 1
            },
            {
                'name': 'শ্রী সুরেশ কুমার দাস',
                'position': 'সহ-সভাপতি',
                'phone': '০১৮১২-৩৪৫৬৭২', 
                'order': 2
            },
            {
                'name': 'শ্রী অমিত কুমার রায়',
                'position': 'সাধারণ সম্পাদক',
                'phone': '০১৯১৩-৪৫৬৭৮৩',
                'order': 3
            },
            {
                'name': 'শ্রী বিমল চন্দ্র ঘোষ',
                'position': 'কোষাধ্যক্ষ',
                'phone': '০১৬১৪-৫৬৭৮৯৪',
                'order': 4
            },
            {
                'name': 'শ্রী অরুণ কুমার পাল',
                'position': 'যুগ্ম সম্পাদক',
                'phone': '০১৫১৫-৬৭৮৯০৫',
                'order': 5
            },
            {
                'name': 'শ্রী প্রদীপ কুমার সেন',
                'position': 'সংগঠক',
                'phone': '০১৪১৬-৭৮৯০১৬',
                'order': 6
            },
            {
                'name': 'শ্রী সুব্রত কুমার মুখার্জী',
                'position': 'উপদেষ্টা',
                'phone': '০১৩১৭-৮৯০১২৭',
                'order': 7
            },
            {
                'name': 'শ্রী দেবব্রত চৌধুরী',
                'position': 'সদস্য',
                'phone': '০১২১৮-৯০১২৩৮',
                'order': 8
            }
        ]
        
        for member_data in committee_members:
            member, created = CommitteeMember.objects.get_or_create(
                name=member_data['name'],
                defaults={
                    'position': member_data['position'],
                    'phone': member_data['phone'],
                    'order': member_data['order'],
                    'is_active': True
                }
            )
            
            if created:
                self.stdout.write(f"Created committee member: {member.name}")

        # Create Durga Sangha Members
        durga_sangha_members = [
            {
                'name': 'শ্রী কৃষ্ণচন্দ্র ভট্টাচার্য',
                'position': 'মুখ্য পুরোহিত',
                'phone': '০১৯২১-১২৩৪৫৬',
                'description': 'দীর্ঘ ২৫ বছর ধরে মন্দিরের সেবায় নিয়োজিত। বেদশাস্ত্র ও পুরাণে গভীর জ্ঞান রয়েছে।',
                'order': 1
            },
            {
                'name': 'শ্রী গোপাল কৃষ্ণ গোস্বামী',
                'position': 'সহকারী পুরোহিত',
                'phone': '০১৮২২-২৩৪৫৬৭',
                'description': 'হরিনাম সংকীর্তন ও আধ্যাত্মিক শিক্ষার বিশেষজ্ঞ। ভক্তদের আধ্যাত্মিক পথ প্রদর্শন করেন।',
                'order': 2
            },
            {
                'name': 'শ্রী রাধিকাপ্রসাদ দাস',
                'position': 'কীর্তনীয়া',
                'phone': '০১৭২৩-৩৪৫৬৭৮',
                'description': 'সুমধুর কণ্ঠে কীর্তন পরিবেশন করেন। মন্দিরের সকল অনুষ্ঠানে কীর্তন পরিচালনা করেন।',
                'order': 3
            },
            {
                'name': 'শ্রী ভক্তিবিনোদ ঠাকুর',
                'position': 'ধর্মীয় শিক্ষক',
                'phone': '০১৬২৪-৪৫৬৭৮৯',
                'description': 'গীতা, পুরাণ ও বৈষ্ণব শাস্ত্রের উপর নিয়মিত ক্লাস নিয়ে থাকেন। আধ্যাত্মিক জ্ঞানের ভাণ্ডার।',
                'order': 4
            },
            {
                'name': 'শ্রী নিত্যানন্দ চৈতন্য দাস',
                'position': 'সেবাইত',
                'phone': '০১৫২৫-৫৬৭৮৯০',
                'description': 'মন্দিরের দৈনন্দিন পরিচর্যা ও ঠাকুর সেবার দায়িত্বে রয়েছেন। অত্যন্ত নিষ্ঠাবান সেবক।',
                'order': 5
            },
            {
                'name': 'শ্রী হরিদাস ঠাকুর',
                'position': 'নাম-প্রচারক',
                'phone': '০১৪২৬-৬৭৮৯০১',
                'description': 'হরিনাম প্রচারে বিশেষ ভূমিকা পালন করেন। সমাজে ধর্মীয় মূল্যবোধ প্রচারে সক্রিয়।',
                'order': 6
            },
            {
                'name': 'শ্রী গৌরাঙ্গ মহাপ্রভু দাস',
                'position': 'যুব সংগঠক',
                'phone': '০১৩২৭-৭৮৯০১২',
                'description': 'তরুণ প্রজন্মকে ধর্মের পথে আকৃষ্ট করার কাজ করেন। যুব সমাজের মধ্যে আধ্যাত্মিকতার প্রসার ঘটাচ্ছেন।',
                'order': 7
            },
            {
                'name': 'শ্রী রামানন্দ রায়',
                'position': 'গ্রন্থ রক্ষক',
                'phone': '০১২২৮-৮৯০১২৩',
                'description': 'মন্দিরের পুস্তকালয় ও ধর্মীয় গ্রন্থাদির রক্ষণাবেক্ষণের দায়িত্বে আছেন।',
                'order': 8
            }
        ]

        for member_data in durga_sangha_members:
            member, created = DurgaSangha.objects.get_or_create(
                name=member_data['name'],
                defaults={
                    'position': member_data['position'],
                    'phone': member_data['phone'],
                    'description': member_data['description'],
                    'order': member_data['order'],
                    'is_active': True
                }
            )
            
            if created:
                self.stdout.write(f"Created durga sangha member: {member.name}")

        self.stdout.write(
            self.style.SUCCESS('Sample data created successfully!')
        )