from rest_framework import serializers
from .models import (Country, City, Project, ProjectImage,
                      Property, PropertyImage, Banner,
                      ProjectVideo, PropertyVideo, PropertyLike,
                      Neighborhood, ProjectBuildingPlan,
                      PropertyBuildingPlanImages, LocationFeature, ProjectDetails
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
        fields = ['id', 'video_full_url',]
        abstract = True

class LocationFeaturesSerializer(serializers.ModelSerializer):

    class Meta:
        model = LocationFeature
        fields = ['feature_name', 'feature_time_in_minutes', 'type']

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

class PropertyBuildingPlanImagesSerializer(ImageFieldSerializer):
    class Meta(ImageFieldSerializer.Meta):
        model = PropertyBuildingPlanImages

class PropertyVideoSerializer(VideoFieldSerializer):
    class Meta(VideoFieldSerializer.Meta):
        model = PropertyVideo

class ProjectDetailsSerializer(BaseSerializer):
    class Meta:
        model = ProjectDetails
        fields = [
            'type', 'plot_area', 'total_height',
            'total_construction_area', 'levels', 'project'
        ]

class PropertySerializer(BaseSerializer):
    effective_price = serializers.SerializerMethodField()
    cover_img_full_url = serializers.SerializerMethodField()
    country = serializers.SerializerMethodField()
    city = serializers.SerializerMethodField()
    project_title = serializers.SerializerMethodField()
    shipping_info = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    videos = serializers.SerializerMethodField()
    # nfts = serializers.SerializerMethodField()
    plans = serializers.SerializerMethodField()
    
    class Meta:
        model = Property
        fields = ['id', 
                    'project', 
                    'project', 'plan_type', 'heating_option', 'latitude',
                    'longitude', 'price_per_nft', 'area', 'average_rating', 'offer',
                    'bedrooms', 'living_rooms', 'first_floor', 'last_floor', 'likes',
                    'first_unit_number', 'last_unit_number', 'furnished', 'cover_img',
                    'effective_price', 'cover_img_full_url', 'country',
                    'city', 'project_title', 'shipping_info', 'images',
                    'videos', 'plans',
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
        plans_queryset = PropertyBuildingPlanImages.objects.filter(property=obj)
        plans_serializer = PropertyBuildingPlanImagesSerializer(instance=plans_queryset, many=True, context={'url': self.url})
        return plans_serializer.data

    def get_videos(self, obj):
        videos_queryset = PropertyVideo.objects.filter(property=obj)
        videos_serializer = PropertyVideoSerializer(instance=videos_queryset, many=True, context={'url': self.url})
        return videos_serializer.data  
        
    def get_country(self, obj):
        return obj.country
    
    def get_city(self, obj):
        return obj.city


class ProjectSerializer(BaseSerializer):
    min_price = serializers.SerializerMethodField()
    max_price = serializers.SerializerMethodField()
    cover_img_full_url = serializers.SerializerMethodField()
    brochure_full_url = serializers.SerializerMethodField()
    min_area = serializers.SerializerMethodField()
    max_area = serializers.SerializerMethodField()
    min_bedrooms = serializers.SerializerMethodField()
    max_bedrooms = serializers.SerializerMethodField()
    country = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    videos = serializers.SerializerMethodField()
    plans = serializers.SerializerMethodField()
    location_featuers = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = ['id', 
                    'neighborhood', 'city',  'title',  'description',
                    'address', 'slug', 'average_rating', 'latitude',
                    'longitude', 'offer', 'property_count', 'cover_img', 'brochure',
                    'min_price', 'max_price', 'cover_img_full_url', 'min_area',
                    'max_area', 'min_bedrooms', 'max_bedrooms', 'country',
                    'images', 'videos', 'plans', 'location_featuers',
                    ]
    
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
    
    def get_location_featuers(self, obj):
        queryset = obj.location_features.all()
        serializer = LocationFeaturesSerializer(queryset, many=True)
        return serializer.data
    
    def get_cover_img_full_url(self, obj):
        if obj.cover_img:
            return get_full_url(obj, 'cover_img', self.url)
        else:
            return None
    
    def get_brochure_full_url(self, obj):
        if obj.brochure:
            return get_full_url(obj, 'brochure', self.url)
        else:
            return None

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
    img_full_url = serializers.SerializerMethodField()
    project_count = serializers.SerializerMethodField()
    min_price = serializers.SerializerMethodField()
    max_price = serializers.SerializerMethodField()
    
    class Meta:
        model = City
        fields = ['id', 'name', 'country', 'description', 'average_groth', 'img_full_url',
                   'project_count', 'min_price', 'max_price']

    def get_project_count(self, obj):
        return obj.project_count

    def get_min_price(self, obj):
        return obj.min_price

    def get_max_price(self, obj):
        return obj.max_price
    
    def get_img_full_url(self, obj):
        return get_full_url(obj, 'city_img', self.url)
    

class CountrySerializer(BaseSerializer):
    img_full_url = serializers.SerializerMethodField()
    flag_img_full_url = serializers.SerializerMethodField()

    class Meta:
        model = Country
        fields = ['id', 'name', 'code',
                   'img_full_url', 'flag_img_full_url'
                   ]

    def get_img_full_url(self, obj):
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