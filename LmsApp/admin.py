from django.contrib import admin

# Register your models here.
from .models import *

class what_will_you_learn_tabularInline(admin.TabularInline):
    model: What_Learn
class Requirements_tabularInline(admin.TabularInline):
    model: Requirements

class Video_tabularInline(admin.TabularInline):
    model: Video

class course_admin(admin.ModelAdmin):
    Inlines=(what_will_you_learn_tabularInline,Requirements_tabularInline,Video_tabularInline)

admin.site.register(Categories)
admin.site.register(Author)
admin.site.register(Course,course_admin)
admin.site.register(Level)
admin.site.register(Language)
admin.site.register(What_Learn)
admin.site.register(Requirements)
admin.site.register(Lesson)
admin.site.register(Video)
admin.site.register(UserCourse)
admin.site.register(Payments)