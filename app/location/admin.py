from django.contrib import admin
from .models import (
    Country, City, Neighborhood, Project, ProjectImage, ProjectBuildingPlan, ProjectVideo, Property,
    PropertyImage, PropertyBuildingPlan, PropertyOutwardView, PropertyVideo, PropertyLike, PropertyCategory, Banner
)

class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')

class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'average_groth', 'project_count', 'min_price', 'max_price')
    list_filter = ('country',)
    search_fields = ('name', 'country__name')
    raw_id_fields = ('country',)

class NeighborhoodAdmin(admin.ModelAdmin):
    list_display = ('name', 'city')
    search_fields = ('name', 'city__name')
    raw_id_fields = ('city',)

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'neighborhood', 'city', 'average_rating', 'offer', 'has_pool', 'roofed_pool')
    list_filter = ('has_security', 'has_theater', 'has_gym', 'has_meeting_room', 'has_pool', 'roofed_pool', 'has_music_room', 'has_yoga_room', 'has_party_room', 'has_spa', 'has_parking', 'roofed_parking')
    search_fields = ('title', 'neighborhood__name', 'city__name')
    raw_id_fields = ('neighborhood', 'city')

class ProjectImageAdmin(admin.ModelAdmin):
    list_display = ('project',)
    raw_id_fields = ('project',)

class ProjectBuildingPlanAdmin(admin.ModelAdmin):
    list_display = ('project',)
    raw_id_fields = ('project',)

class ProjectVideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'project')
    search_fields = ('title', 'project__title')
    raw_id_fields = ('project',)

class PropertyAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'project', 'price_per_nft', 'effective_price', 'bedrooms', 'bathrooms', 'likes', 'furnished')
    list_filter = ('category', 'project__city', 'furnished', 'has_maid_room', 'has_swimming_pool', 'has_steam_room')
    search_fields = ('name', 'category__name', 'project__title', 'project__neighborhood__name', 'project__city__name')
    raw_id_fields = ('category', 'project')

class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ('property',)
    raw_id_fields = ('property',)

class PropertyBuildingPlanAdmin(admin.ModelAdmin):
    list_display = ('property',)
    raw_id_fields = ('property',)

class PropertyOutwardViewAdmin(admin.ModelAdmin):
    list_display = ('property',)
    raw_id_fields = ('property',)

class PropertyVideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'property')
    search_fields = ('title', 'property__name')
    raw_id_fields = ('property',)

class PropertyLikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'property', 'created_at')
    search_fields = ('user__username', 'user__email', 'property__name')
    raw_id_fields = ('user', 'property')

class PropertyCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class BannerAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)

admin.site.register(Country, CountryAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Neighborhood, NeighborhoodAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectImage, ProjectImageAdmin)
admin.site.register(ProjectBuildingPlan, ProjectBuildingPlanAdmin)
admin.site.register(ProjectVideo, ProjectVideoAdmin)
admin.site.register(Property, PropertyAdmin)
admin.site.register(PropertyImage, PropertyImageAdmin)
admin.site.register(PropertyBuildingPlan, PropertyBuildingPlanAdmin)
admin.site.register(PropertyOutwardView, PropertyOutwardViewAdmin)
admin.site.register(PropertyVideo, PropertyVideoAdmin)
admin.site.register(PropertyLike, PropertyLikeAdmin)
admin.site.register(PropertyCategory, PropertyCategoryAdmin)
admin.site.register(Banner, BannerAdmin)
