from django.db import models
from decimal import Decimal, ROUND_DOWN
from django.contrib.auth.models import User


class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    discount = models.IntegerField()
    active = models.BooleanField(default=True)
    thumbnail = models.ImageField(upload_to='media/courses/thumbnails', blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    resource = models.FileField(upload_to='media/courses/resources', blank=True, null=True)
    length_in_minutes = models.PositiveIntegerField()
    slug=models.CharField(max_length=100, null=False, blank=False, unique=True)

    @property
    def discounted_price(self):
        # calculate using Decimal and return whole number (no decimals)
        percent = Decimal(100 - int(self.discount))
        result = (self.price * percent) / Decimal(100)
        # drop fractional cents, return as int
        return int(result.quantize(Decimal('1'), rounding=ROUND_DOWN))

    def __str__(self):
        return self.name


class CourseProperty(models.Model):
    description = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        abstract = True


    def __str__(self):
        return self.description


class Tag(CourseProperty):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='tags'
    )


class Prerequisite(CourseProperty):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='prerequisites'
    )


class Learning(CourseProperty):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='learnings'
    )



class Video(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='videos')
    title = models.CharField(max_length=100)
    url = models.URLField()
    serial_number = models.PositiveIntegerField()
    is_preview = models.BooleanField(default=False)

    @property
    def embed_url(self):
        if 'youtube.com' in self.url or 'youtu.be' in self.url:
            video_id = None
            if 'v=' in self.url:
                video_id = self.url.split('v=')[1].split('&')[0]
            elif 'youtu.be/' in self.url:
                video_id = self.url.split('youtu.be/')[1].split('?')[0]
            elif 'youtube.com/embed/' in self.url:
                return self.url
            elif 'youtube.com/shorts/' in self.url:
                video_id = self.url.split('youtube.com/shorts/')[1].split('?')[0]
            
            if video_id:
                # Add rel=0 and origin for better compatibility
                return f"https://www.youtube.com/embed/{video_id}?rel=0"
        return self.url

    def __str__(self):
        return self.title
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    profile_image = models.ImageField(upload_to='courses/profiles', blank=True, null=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    


class UserCourse(models.Model):
    user=models.ForeignKey(User,null=False,on_delete=models.CASCADE)
    Course=models.ForeignKey(Course,null=False,on_delete=models.CASCADE)
    data=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.user.username} - {self.Course.name}' 



class Payment(models.Model):
    order_id=models.CharField(max_length=50,null=False)
    payment_id=models.CharField(max_length=50)
    user_course=models.ForeignKey(UserCourse,null=True,blank=True,on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now_add=True)
    status=models.BooleanField(default=False)
    Course=models.ForeignKey(Course,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.user.username} - {self.Course.name}' 
