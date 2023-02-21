from django.core.management.base import BaseCommand
from faker import Faker
from blog.models import Category, Post
from django.contrib.auth import get_user_model


User = get_user_model()


class Command(BaseCommand):
    help = 'Inserting 100 dummy data!'
    
    def __init__(self):
        super(Command, self).__init__()
        self.f = Faker()
    
    def handle(self, *args, **options):
        for _ in range(10):
            user = User.objects.create(email=self.f.email(), password=self.f.password)
            profile = user.profile_set.all()[0]
            profile.first_name = self.f.first_name()
            profile.last_name = self.f.last_name()
            profile.description = self.f.sentence(5)
            profile.image = self.f.image_url()
            profile.save()
            category = Category.objects.create(name=self.f.last_name())
            for __ in range(10):
                post = Post.objects.create(
                    author=profile,
                    title=self.f.paragraph(),
                    content=self.f.paragraph(5),
                    status=bool(self.f.random_int(0, 1)),
                    published_dt=self.f.date_time(),
                    category=category
                )
                print(profile, post)
        print(Post.objects.count())
