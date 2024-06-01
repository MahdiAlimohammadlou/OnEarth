from rest_framework import serializers
from .models import (Country, City, Project, ProjectImage, Facility,
                      Property, PropertyImage, Banner, Category,
                      ProjectVideo, PropertyVideo, PropertyLike
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
        fields = ['id', 'image', 'image_full_url']
        abstract = True

class VideoFieldSerializer(BaseSerializer):
    video_full_url = serializers.SerializerMethodField()

    def get_video_full_url(self, obj):
        return get_full_url(obj, 'video_file', self.url)

    class Meta:
        fields = ['id', 'video_file', 'video_full_url', 'title', 'description',]
        abstract = True


class FacilitySerializer(BaseSerializer):
    facility_icon_full_url = serializers.SerializerMethodField()

    class Meta:
        model = Facility
        fields = ['id', 'name', 'facility_icon', 'facility_icon_full_url']

    def get_facility_icon_full_url(self, obj):
        return get_full_url(obj, 'facility_icon', self.url)


class ProjectImageSerializer(BaseSerializer):
    image_full_url = serializers.SerializerMethodField()
    image_2d_full_url = serializers.SerializerMethodField()
    image_3d_full_url = serializers.SerializerMethodField()

    class Meta:
        model = ProjectImage
        fields = ['id', 'image', 'image_2d', 'image_3d', 'image_full_url', 'image_2d_full_url', 'image_3d_full_url']

    def get_image_full_url(self, obj):
        return get_full_url(obj, 'image', self.url)

    def get_image_2d_full_url(self, obj):
        return get_full_url(obj, 'image_2d', self.url)

    def get_image_3d_full_url(self, obj):
        return get_full_url(obj, 'image_3d', self.url)

class ProjectVideoSerializer(VideoFieldSerializer):
    class Meta(VideoFieldSerializer.Meta):
        model = ProjectVideo      

class PropertyImageSerializer(ImageFieldSerializer):
    class Meta(ImageFieldSerializer.Meta):
        model = PropertyImage

class PropertyVideoSerializer(VideoFieldSerializer):
    class Meta(VideoFieldSerializer.Meta):
        model = PropertyVideo


class PropertySerializer(BaseSerializer):
    images = serializers.SerializerMethodField()
    videos = serializers.SerializerMethodField()
    cover_img_full_url = serializers.SerializerMethodField()
    country = serializers.SerializerMethodField()
    city = serializers.SerializerMethodField()
    project_title = serializers.SerializerMethodField()
    shipping_info = serializers.SerializerMethodField()
    nfts = serializers.SerializerMethodField()
    effective_price = serializers.SerializerMethodField()
    
    class Meta:
        model = Property
        fields = ['id', 'name', 'project', 'project_title', 'latitude',
                    'longitude', 'description', 'price_per_nft', 'offer', 'effective_price',
                    'area', 'bedrooms', 'bathrooms', 'purpose', 'parking_space_count', 'has_maid_room',
                    'has_swimming_pool','has_steam_room', 'average_rating', 'cover_img',
                    'cover_img_full_url', 'country', 'city', "master_count",
                      "heating_option", "floor", "unit_number", 'videos', 'images',
                       'shipping_info', 'nfts'
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
        
    def get_nfts(self, obj):
        nfts = NFT.objects.filter(property=obj)
        serializer = NFTSerializer(instance=nfts, many=True)
        return serializer.data  
        
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
    
    class Meta:
        model = Project
        fields = ['id', 'title', 'city', 'description',
                   'average_rating', 'address', 'property_count',
                    'min_bedrooms', 'max_bedrooms', 'min_area',
                    'max_area', 'cover_img', 'cover_img_full_url', 'slug',
                    'country', 'min_price', 'max_price', 'latitude',
                    'longitude', 'images', 'facilities', 'videos']
        
    def get_facilities(self, obj):
        facilities_queryset = obj.facilities.all()
        serializer = FacilitySerializer(instance=facilities_queryset, many=True, context={'url': self.url})
    
    def get_images(self, obj):
        try:
            images_queryset = ProjectImage.objects.get(project=obj)
        except ProjectImage.DoesNotExist:
            return []
        images_serializer = ProjectImageSerializer(instance=images_queryset, context={'url': self.url})
        return images_serializer.data
    
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


class CitySerializer(BaseSerializer):
    city_img_full_url = serializers.SerializerMethodField()
    project_count = serializers.SerializerMethodField()
    min_price = serializers.SerializerMethodField()
    max_price = serializers.SerializerMethodField()
    
    class Meta:
        model = City
        fields = ['id', 'name', 'country', 'description', 'city_img', 'city_img_full_url',
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
        fields = ['id', 'name', 'code', 'country_img', 'flag_img', 'country_img_full_url', 'flag_img_full_url']

    def get_country_img_full_url(self, obj):
        return get_full_url(obj, 'country_img', self.url)
        
    def get_flag_img_full_url(self, obj):
        return get_full_url(obj, 'flag_img', self.url)

        
        
class BannerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Banner
        fields = ['title', 'banner_img']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return {'data': data}
        

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['title', 'category_icon']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return {'data': data}
    
class PropertyLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyLike
        fields = ['property']