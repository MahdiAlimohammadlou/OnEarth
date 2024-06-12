from django.contrib import admin
from .models import (Country, City, Facility, Project,
                      ProjectImage, Property, PropertyImage,
                      Banner, ProjectVideo, PropertyVideo,
                      Neighborhood, ProjectBuildingPlan, PropertyBuildingPlan, PropertyOutwardView)

admin.site.register(Country)
admin.site.register(City)
admin.site.register(Neighborhood)
admin.site.register(Facility)
admin.site.register(Project)
admin.site.register(ProjectImage)
admin.site.register(ProjectBuildingPlan)
admin.site.register(Property)
admin.site.register(PropertyImage)
admin.site.register(PropertyBuildingPlan)
admin.site.register(PropertyOutwardView)
admin.site.register(Banner)
admin.site.register(ProjectVideo)
admin.site.register(PropertyVideo)

