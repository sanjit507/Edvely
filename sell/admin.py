from django.contrib import admin
from .models import Course, Tag, Prerequisite, Learning,Video,Profile,Payment,UserCourse


class TagAdmin(admin.TabularInline):
    model=Tag
class PrerequisiteAdmin(admin.TabularInline):
    model=Prerequisite
class LearningAdmin(admin.TabularInline):
    model=Learning
    
class VideoAdmin(admin.TabularInline):
    model=Video    

@admin.register(Course) 
class CourseAdmin(admin.ModelAdmin):
 inlines = [TagAdmin, PrerequisiteAdmin, LearningAdmin, VideoAdmin]
 
admin.site.register(Profile)
admin.site.register(Payment)
admin.site.register(UserCourse)
