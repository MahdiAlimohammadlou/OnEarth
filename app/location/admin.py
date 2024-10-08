from django.contrib import admin
from .models import (
    Country, City, Neighborhood, Project, ProjectDetails, 
    ProjectImage, ProjectBuildingPlan, ProjectVideo, ProjectFacilities, 
    Property, PropertyImage, PropertyBuildingPlanImages, PropertyVideo, 
    PropertyLike, PropertyFacilities, Banner, LocationFeature
)

class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'flag_img', 'country_img')
    search_fields = ('name', 'code')

class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'average_groth', 'min_price', 'max_price', 'project_count')
    search_fields = ('name',)
    list_filter = ('country',)

class NeighborhoodAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'neighborhood_img')
    search_fields = ('name', 'city__name')
    list_filter = ('city',)

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'neighborhood', 'city', 'average_rating', 'min_price', 'max_price', 'min_bedrooms', 'max_bedrooms', 'min_area', 'max_area', 'country')
    search_fields = ('title', 'neighborhood__name', 'city__name')
    list_filter = ('neighborhood', 'city')

class ProjectDetailsAdmin(admin.ModelAdmin):
    list_display = ('project', 'type', 'plot_area', 'total_height', 'total_construction_area', 'levels')
    search_fields = ('project__title', 'type')
    list_filter = ('project',)

class ProjectImageAdmin(admin.ModelAdmin):
    list_display = ('project', 'image')
    search_fields = ('project__title',)
    list_filter = ('project',)

class ProjectBuildingPlanAdmin(admin.ModelAdmin):
    list_display = ('project', 'image')
    search_fields = ('project__title',)
    list_filter = ('project',)

class ProjectVideoAdmin(admin.ModelAdmin):
    list_display = ('project', 'video_file')
    search_fields = ('project__title',)
    list_filter = ('project',)

class ProjectFacilitiesAdmin(admin.ModelAdmin):
    list_display = ('title', 'count', 'project')
    search_fields = ('title', 'project__title')
    list_filter = ('project',)

class PropertyAdmin(admin.ModelAdmin):
    list_display = ('plan_type', 'project', 'heating_option', 'price_per_nft', 'area', 'average_rating', 'offer', 'bedrooms', 'effective_price', 'country', 'city', 'cover_img')
    search_fields = ('plan_type', 'project__title')
    list_filter = ('project', 'heating_option')
    list_filter = ('project',)

class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ('property', 'image')
    search_fields = ('property__project__title',)
    list_filter = ('property',)

class PropertyBuildingPlanImagesAdmin(admin.ModelAdmin):
    list_display = ('property', 'image')
    search_fields = ('property__project__title',)
    list_filter = ('property',)

class PropertyVideoAdmin(admin.ModelAdmin):
    list_display = ('property', 'video_file')
    search_fields = ('property__project__title',)
    list_filter = ('property',)

class PropertyLikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'property', 'created_at')
    search_fields = ('user__username', 'property__project__title')
    list_filter = ('user', 'property')
    list_filter = ('property',)

class PropertyFacilitiesAdmin(admin.ModelAdmin):
    list_display = ('title', 'count')
    search_fields = ('title', 'properties__project__title')

class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'banner_img')
    search_fields = ('title',)

class LocationFeatureAdmin(admin.ModelAdmin):
    list_display = ('project', 'feature_name', 'feature_time_in_minutes', 'type')
    search_fields = ('project__title', 'feature_name')
    list_filter = ('type', 'project')

admin.site.register(Country, CountryAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Neighborhood, NeighborhoodAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectDetails, ProjectDetailsAdmin)
admin.site.register(ProjectImage, ProjectImageAdmin)
admin.site.register(ProjectBuildingPlan, ProjectBuildingPlanAdmin)
admin.site.register(ProjectVideo, ProjectVideoAdmin)
admin.site.register(ProjectFacilities, ProjectFacilitiesAdmin)
admin.site.register(Property, PropertyAdmin)
admin.site.register(PropertyImage, PropertyImageAdmin)
admin.site.register(PropertyBuildingPlanImages, PropertyBuildingPlanImagesAdmin)
admin.site.register(PropertyVideo, PropertyVideoAdmin)
admin.site.register(PropertyLike, PropertyLikeAdmin)
admin.site.register(PropertyFacilities, PropertyFacilitiesAdmin)
admin.site.register(Banner, BannerAdmin)
admin.site.register(LocationFeature, LocationFeatureAdmin)
