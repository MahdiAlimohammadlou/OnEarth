from typing import Iterable
from django.db import models
from core.models import AbstractBaseModel
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Min, Max
from account.models import User

class Country(AbstractBaseModel):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=3, unique=True)
    flag_img = models.ImageField(upload_to="country_flags/", null = True, blank = True) 
    country_img = models.ImageField(upload_to="country_images/", null = True, blank = True) 

    def __str__(self):
        return self.name
    
class City(AbstractBaseModel):
    name = models.CharField(max_length=100)
    country = models.ForeignKey('Country', on_delete=models.CASCADE)
    description = models.TextField()
    average_groth = models.DecimalField(max_digits = 6, decimal_places = 2)
    city_img = models.ImageField(upload_to="city_images/", null = True, blank = True)

    @property
    def min_price(self):
        properties = Property.objects.filter(project__city=self)
        if properties:
            return min(property.effective_price for property in properties)
        return None
        
    @property
    def max_price(self):
        properties = Property.objects.filter(project__city=self)
        if properties:
            return max(property.effective_price for property in properties)
        return None

    @property
    def project_count(self):
        return self.projects.count()  

    def __str__(self):
        return self.name


class Neighborhood(AbstractBaseModel):
    name = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='neighborhoods')
    description = models.TextField()
    neighborhood_img = models.ImageField(upload_to="neighborhood_images/", null=True, blank=True)

    def __str__(self):
        return self.name

class Project(AbstractBaseModel):
    #Relations
    neighborhood = models.ForeignKey(Neighborhood, related_name="projects", on_delete=models.CASCADE)
    city = models.ForeignKey(City, related_name="projects", on_delete=models.CASCADE)
    #STR fields
    title = models.CharField(max_length=100)
    description = models.TextField()
    address = models.TextField()
    slug = models.SlugField(unique=True, max_length=150, blank=True)
    #Decimal fields
    average_rating = models.DecimalField(max_digits=2, decimal_places=1, default=5.0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    latitude = models.FloatField(null=True, blank=True, default=1.45648)
    longitude = models.FloatField(null=True, blank=True, default=1.45648)
    offer = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(100)], null=True, blank=True, default=0)
    #Facilities
    security_count = models.IntegerField(default=0)
    theater_count = models.IntegerField(default=0)
    gym_count = models.IntegerField(default=0)
    meeting_room_count = models.IntegerField(default=0)
    pool_count = models.IntegerField(default=0)
    roofed_pool_count = models.IntegerField(default=0)
    music_room_count = models.IntegerField(default=0)
    yoga_room_count = models.IntegerField(default=0)
    party_room_count = models.IntegerField(default=0)
    spa_count = models.IntegerField(default=0)
    parking_count = models.IntegerField(default=0)
    roofed_parking_count = models.IntegerField(default=0)
    landscaped_gardens_count = models.IntegerField(default=0)
    kids_swimming_pool_count = models.IntegerField(default=0)
    retail_areas_count = models.IntegerField(default=0)
    retail_areas_count = models.IntegerField(default=0)
    large_lifts = models.IntegerField(default=0)
    #Image fields
    cover_img = models.ImageField(upload_to = "project_cover_images/", null = True, blank = True)
    #File fields
    brochure = models.FileField(upload_to = "brochure_pdf/", null = True, blank = True)
    
    @property
    def min_price(self):
        properties = self.properties.all()
        if properties:
            return min(property.effective_price for property in properties)
        return None

    @property
    def max_price(self):
        properties = self.properties.all()
        if properties:
            return max(property.effective_price for property in properties)
        return None

    @property
    def property_count(self):
        return self.properties.count()
    
    @property
    def min_bedrooms(self):
        min_bedrooms = self.properties.aggregate(Min('bedrooms'))['bedrooms__min']
        return min_bedrooms if min_bedrooms is not None else 0
    
    @property
    def max_bedrooms(self):
        max_bedrooms = self.properties.aggregate(Max('bedrooms'))['bedrooms__max']
        return max_bedrooms if max_bedrooms is not None else 0
    
    @property
    def min_area(self):
        min_area = self.properties.aggregate(Min('area'))['area__min']
        return min_area if min_area is not None else 0

    @property
    def max_area(self):
        max_area = self.properties.aggregate(Max('area'))['area__max']
        return max_area if max_area is not None else 0
    
    @property
    def country(self):
        return self.neighborhood.city.country.name

    def __str__(self):
        return self.title
    
class ProjectDetails(AbstractBaseModel):
    type = models.CharField(max_length=255)
    plot_area = models.CharField(max_length=255)
    total_height = models.CharField(max_length=255)
    total_construction_area = models.CharField(max_length=255)
    levels = models.CharField(max_length=255)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.project + "|" + self.key + "|" + self.value

class ProjectImage(AbstractBaseModel):
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='project_images/') 

    def __str__(self):
        return self.project.title + ' Image'

class ProjectBuildingPlan(AbstractBaseModel):
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='project_plan_images/') 

    def __str__(self):
        return self.project.title + ' building plan'
    
class ProjectVideo(AbstractBaseModel):
    project = models.ForeignKey(Project, related_name='videos', on_delete=models.CASCADE)
    video_file = models.FileField(upload_to='project_videos/')

    def __str__(self):
        return self.title

class Property(AbstractBaseModel):

    HEATING_OPTIONS = [
        ('none', 'None'),
        ('heating stoves', 'Heating Stoves'),
        ('natural gas stove', 'Natural Gas Stove'),
        ('room heater', 'Room Heater'),
        ('central heating', 'Central Heating'),
        ('central heating (share meter)', 'Central Heating (Share Meter)'),
        ('central heating boiler (electric)', 'Central Heating Boiler (Electric)'),
        ('central heating boilers (natural gas)', 'Central Heating Boilers (Natural Gas)'),
        ('floor heating', 'Floor Heating'),
        ('air conditioning', 'Air Conditioning'),
        ('fan coil unit', 'Fan Coil Unit'),
        ('solar energy', 'Solar Energy'),
        ('elektrikli radyator', 'Elektrikli Radyator'),
    ]

    #Relations
    # category = models.ForeignKey('PropertyCategory', related_name='properties', on_delete=models.SET_NULL)
    project = models.ForeignKey('Project', related_name='properties', on_delete=models.CASCADE, null=True, blank=True)

    #STR fields
    heating_option = models.CharField(max_length=50, choices=HEATING_OPTIONS, default='none')
    #Decimals
    latitude = models.FloatField(null=True, blank=True, default=1.45648)
    longitude = models.FloatField(null=True, blank=True, default=1.45648)
    price_per_nft = models.DecimalField(max_digits=10, decimal_places=2)
    area = models.DecimalField(max_digits=10, decimal_places=2)
    average_rating = models.DecimalField(max_digits=2, decimal_places=1, default=5.0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    offer = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(100)], null=True, blank=True, default=0)
    #Integers
    bedrooms = models.IntegerField(default=0)
    bathrooms = models.IntegerField(default=0)
    tub_count = models.IntegerField(default=0)
    pool_count = models.IntegerField(default=0)
    parking_space_count = models.IntegerField(default=1)
    master_count = models.IntegerField(default=0)
    first_floor = models.IntegerField(null=True, blank=True, default=1)
    last_floor = models.IntegerField(null=True, blank=True, default=1)
    likes = models.IntegerField(default=0)
    first_unit_number = models.IntegerField(null=True, blank=True, default=1)
    last_unit_number = models.IntegerField(null=True, blank=True, default=1)
    living_room_count = models.IntegerField(null=True, blank=True, default=1)
    lundry_count = models.IntegerField(null=True, blank=True, default=1)
    closet_count = models.IntegerField(null=True, blank=True, default=1)
    balcony_count = models.IntegerField(null=True, blank=True, default=1)
    #Booleans
    furnished = models.BooleanField(default=False)
    is_open_kichen = models.BooleanField(default=False)
    #Image
    cover_img = models.ImageField(upload_to = "property_cover_images/", null = True, blank = True)

    @property
    def effective_price(self):
        if self.offer is not None:
            return self.price_per_nft * (1 - self.offer / 100)
        else:
            return self.price_per_nft

    @property
    def country(self):
        return self.project.neighborhood.city.country.name

    @property
    def city(self):
        return self.project.neighborhood.city.name

    def __str__(self):
        return self.name
    
class PropertyImage(AbstractBaseModel):
    property = models.ForeignKey('Property', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='Property_images/')

    def __str__(self):
        return self.property.project.title + ' Image'
    
class PropertyBuildingPlan(AbstractBaseModel):
    property = models.ForeignKey('Property', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='property_plan_images/') 

    def __str__(self):
        return self.property.project.title + ' building plan'
    
class PropertyOutwardView(AbstractBaseModel):
    property = models.ForeignKey('Property', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='property_outward_images/') 

    def __str__(self):
        return self.property.project.title + ' outward view'
    
class PropertyVideo(AbstractBaseModel):
    property = models.ForeignKey(Property, related_name='videos', on_delete=models.CASCADE)
    video_file = models.FileField(upload_to='property_videos/')

    def __str__(self):
        return self.title

class PropertyLike(AbstractBaseModel):
    user = models.ForeignKey(User, related_name='propertylikes', on_delete=models.CASCADE)
    property = models.ForeignKey(Property, related_name='propertylikes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'property')

class Banner(AbstractBaseModel):
    title = models.TextField()
    banner_img = models.ImageField(upload_to="banner_images/", null=True, blank=True)

    def __str__(self) -> str:
        if len(self.title) > 50:
            return self.title[:50] + "..."
        return self.title
    
class LocationFeature(AbstractBaseModel):
    VEHICLE_CHOICES = [
        ("Walk", "walk"),
        ("Car", "car"),
    ]

    project = models.ForeignKey(Project, related_name='location_features', on_delete=models.CASCADE)
    feature_name = models.CharField(max_length=255)
    feature_time_in_minutes = models.IntegerField(default=5, null=True, blank=True)
    type = models.CharField(max_length=50, choices=VEHICLE_CHOICES, null=True, blank=True)

    def __str__(self):
        return f"{self.feature_name}: {self.feature_time_in_minutes} ({self.type})"