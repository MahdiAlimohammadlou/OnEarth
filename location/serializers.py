from rest_framework import serializers
from .models import (Country, City, Project, ProjectImage, Facility,
                      Property, PropertyImage, Banner,
                      ProjectVideo, PropertyVideo, PropertyLike,
                      Neighborhood, ProjectBuildingPlan,
                      PropertyBuildingPlan, PropertyOutwardView,
                      PropertyCategory
                      )
from core.serializers import BaseSerializer
from financial.models import ShippingInfo, NFT
from financial.serializers import ShippingInfoSerializer, NFTSerializer
from core.utils import get_full_url

class ImageFieldSerializer(BaseSerializer):
    image_full_url = serializers.SerializerMethodField()

    def get_image_full_url(self, obj):
        return get_full_url(obj, 'image', self.url)

    class Meta:
        fields = ['id', 'image_full_url']
        abstract = True

class VideoFieldSerializer(BaseSerializer):
    video_full_url = serializers.SerializerMethodField()

    def get_video_full_url(self, obj):
        return get_full_url(obj, 'video_file', self.url)

    class Meta:
        fields = ['id', 'video_full_url', 'title', 'description',]
        abstract = True


class FacilitySerializer(BaseSerializer):
    facility_icon_full_url = serializers.SerializerMethodField()

    class Meta:
        model = Facility
        fields = ['id', 'name', 'facility_icon_full_url']

    def get_facility_icon_full_url(self, obj):
        return get_full_url(obj, 'facility_icon', self.url)


class ProjectImageSerializer(ImageFieldSerializer):
    class Meta(ImageFieldSerializer.Meta):
        model = ProjectImage

class ProjectBuildingPlanSerializer(ImageFieldSerializer):
    class Meta(ImageFieldSerializer.Meta):
        model = ProjectBuildingPlan

class ProjectVideoSerializer(VideoFieldSerializer):
    class Meta(VideoFieldSerializer.Meta):
        model = ProjectVideo      

class PropertyImageSerializer(ImageFieldSerializer):
    class Meta(ImageFieldSerializer.Meta):
        model = PropertyImage

class PropertyBuildingPlanSerializer(ImageFieldSerializer):
    class Meta(ImageFieldSerializer.Meta):
        model = PropertyBuildingPlan

class PropertyOutwardViewSerializer(ImageFieldSerializer):
    class Meta(ImageFieldSerializer.Meta):
        model = PropertyOutwardView

class PropertyVideoSerializer(VideoFieldSerializer):
    class Meta(VideoFieldSerializer.Meta):
        model = PropertyVideo

class PropertyCategorySerializer(BaseSerializer):
    class Meta:
        model = PropertyCategory
        fields = [
            'id', 'name'
        ]

class PropertySerializer(BaseSerializer):
    images = serializers.SerializerMethodField()
    videos = serializers.SerializerMethodField()
    cover_img_full_url = serializers.SerializerMethodField()
    country = serializers.SerializerMethodField()
    city = serializers.SerializerMethodField()
    project_title = serializers.SerializerMethodField()
    shipping_info = serializers.SerializerMethodField()
    # nfts = serializers.SerializerMethodField()
    effective_price = serializers.SerializerMethodField()
    plans = serializers.SerializerMethodField()
    outward_views = serializers.SerializerMethodField()
    
    class Meta:
        model = Property
        fields = ['id', 'name', 'project', 'project_title', 'latitude',
                    'longitude', 'description', 'price_per_nft', 'offer', 'effective_price',
                    'area', 'bedrooms', 'bathrooms', 'purpose', 'parking_space_count', 'has_maid_room',
                    'has_swimming_pool','has_steam_room', 'average_rating',
                    'cover_img_full_url', 'country', 'city', 'master_count',
                    'heating_option', 'floor', 'unit_number', 'videos', 'images',
                    'shipping_info', 'plans', 'outward_views',
                    'tub_count', 'pool_count',
                    #   'nfts'
                       ]
        
    def get_effective_price(self, obj):
        return obj.effective_price

    def get_shipping_info(self, obj):
        try:      
            shipping_info = ShippingInfo.objects.get(property=obj)
        except ShippingInfo.DoesNotExist:
            return []
        serializer = ShippingInfoSerializer(instance=shipping_info)
        return serializer.data  
        
    # def get_nfts(self, obj):
    #     nfts = NFT.objects.filter(property=obj)
    #     serializer = NFTSerializer(instance=nfts, many=True)
    #     return serializer.data  
        
    def get_project_title(self, obj):
        return obj.project.title

    def get_cover_img_full_url(self, obj):
        if obj.cover_img != "":
            return self.url + obj.cover_img.url
        else:
            return ""

    def get_images(self, obj):
        images_queryset = PropertyImage.objects.filter(property=obj)
        images_serializer = PropertyImageSerializer(instance=images_queryset, many=True, context={'url': self.url})
        return images_serializer.data  

    def get_plans(self, obj):
        plans_queryset = PropertyBuildingPlan.objects.filter(property=obj)
        plans_serializer = PropertyBuildingPlanSerializer(instance=plans_queryset, many=True, context={'url': self.url})
        return plans_serializer.data

    def get_outward_views(self, obj):
        queryset = PropertyOutwardView.objects.filter(property=obj)
        serializer = PropertyOutwardViewSerializer(instance=queryset, many=True, context={'url': self.url})
        return serializer.data

    def get_videos(self, obj):
        videos_queryset = PropertyVideo.objects.filter(property=obj)
        videos_serializer = PropertyVideoSerializer(instance=videos_queryset, many=True, context={'url': self.url})
        return videos_serializer.data  
        
    def get_country(self, obj):
        return obj.country
    
    def get_city(self, obj):
        return obj.city


class ProjectSerializer(BaseSerializer):
    images = serializers.SerializerMethodField()
    videos = serializers.SerializerMethodField()
    cover_img_full_url = serializers.SerializerMethodField()
    facilities = serializers.SerializerMethodField()
    property_count = serializers.SerializerMethodField()
    min_bedrooms = serializers.SerializerMethodField()
    max_bedrooms = serializers.SerializerMethodField()
    min_area = serializers.SerializerMethodField()
    max_area = serializers.SerializerMethodField()
    country = serializers.SerializerMethodField()
    min_price = serializers.SerializerMethodField()
    max_price = serializers.SerializerMethodField()
    plans = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = ['id', 'title', 'neighborhood', 'description',
                   'average_rating', 'address', 'property_count',
                    'min_bedrooms', 'max_bedrooms', 'min_area',
                    'max_area', 'cover_img_full_url', 'slug',
                    'country', 'min_price', 'max_price', 'latitude',
                    'longitude', 'images', 'facilities', 'videos', 'plans',
                    'has_security', 'has_theater', 'has_gym', 'has_meeting_room',
                    'has_pool', 'roofed_pool', 'has_music_room', 'has_yoga_room',
                    'has_party_room', 'has_spa', 'has_parking', 'roofed_parking',
                    ]
        
    def get_facilities(self, obj):
        facilities_queryset = obj.facilities.all()
        serializer = FacilitySerializer(instance=facilities_queryset, many=True, context={'url': self.url})
        return serializer.data
    
    def get_images(self, obj):
        try:
            images_queryset = ProjectImage.objects.filter(project=obj)
        except ProjectImage.DoesNotExist:
            return []
        images_serializer = ProjectImageSerializer(instance=images_queryset, many=True, context={'url': self.url})
        return images_serializer.data
    
    def get_plans(self, obj):
        palns_queryset = ProjectBuildingPlan.objects.filter(project=obj)
        palns_serializer = ProjectBuildingPlanSerializer(instance=palns_queryset, many=True, context={'url': self.url})
        return palns_serializer.data
    
    def get_videos(self, obj):
        videos_queryset = ProjectVideo.objects.filter(project=obj)
        videos_serializer = ProjectVideoSerializer(instance=videos_queryset, many=True, context={'url': self.url})
        return videos_serializer.data  
    
    def get_cover_img_full_url(self, obj):
        return get_full_url(obj, 'cover_img', self.url)

    def get_property_count(self, obj):
        return obj.property_count

    def get_min_bedrooms(self, obj):
        return obj.min_bedrooms

    def get_max_bedrooms(self, obj):
        return obj.max_bedrooms

    def get_min_area(self, obj):
        return obj.min_area

    def get_max_area(self, obj):
        return obj.max_area

    def get_country(self, obj):
        return obj.country

    def get_min_price(self, obj):
        return obj.min_price

    def get_max_price(self, obj):
        return obj.max_price


class NeighborhoodSerializer(BaseSerializer):
    full_neighborhood_img_url = serializers.SerializerMethodField()

    class Meta:
        model = Neighborhood
        fields = [
         "name", "city", "description",
         "full_neighborhood_img_url"
        ]

    def get_full_neighborhood_img_url(self, obj):
        return get_full_url(obj, "neighborhood_img", self.url)



class CitySerializer(BaseSerializer):
    city_img_full_url = serializers.SerializerMethodField()
    project_count = serializers.SerializerMethodField()
    min_price = serializers.SerializerMethodField()
    max_price = serializers.SerializerMethodField()
    
    class Meta:
        model = City
        fields = ['id', 'name', 'country', 'description', 'average_groth', 'city_img_full_url',
                   'project_count', 'min_price', 'max_price']

    def get_project_count(self, obj):
        return obj.project_count

    def get_min_price(self, obj):
        return obj.min_price

    def get_max_price(self, obj):
        return obj.max_price
    
    def get_city_img_full_url(self, obj):
        return get_full_url(obj, 'city_img', self.url)
    

class CountrySerializer(BaseSerializer):
    country_img_full_url = serializers.SerializerMethodField()
    flag_img_full_url = serializers.SerializerMethodField()

    class Meta:
        model = Country
        fields = ['id', 'name', 'code', 'country_img_full_url', 'flag_img_full_url']

    def get_country_img_full_url(self, obj):
        return get_full_url(obj, 'country_img', self.url)
        
    def get_flag_img_full_url(self, obj):
        return get_full_url(obj, 'flag_img', self.url)

        
        
class BannerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Banner
        fields = ['title',]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return {'data': data}
    
class PropertyLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyLike
        fields = ['property']