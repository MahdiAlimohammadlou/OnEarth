from django.contrib import admin
from .models import (Country, City, Facility, Project,
                      ProjectImage, Property, PropertyImage,
                      Banner, Category, ProjectVideo, PropertyVideo)

admin.site.register(Country)
admin.site.register(City)
admin.site.register(Facility)
admin.site.register(Project)
admin.site.register(ProjectImage)
admin.site.register(Property)
admin.site.register(PropertyImage)
admin.site.register(Banner)
admin.site.register(Category)
admin.site.register(ProjectVideo)
admin.site.register(PropertyVideo)

