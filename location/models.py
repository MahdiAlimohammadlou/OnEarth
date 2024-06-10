from django.db import models
from core.models import AbstractBaseModel
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Min, Max
from account.models import User
from decimal import Decimal
from django.db.models import F, Case, When, DecimalField

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


class Neighborhood(models.Model):
    name = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='neighborhoods')
    description = models.TextField()
    neighborhood_img = models.ImageField(upload_to="neighborhood_images/", null=True, blank=True)

    def __str__(self):
        return self.name


class Facility(AbstractBaseModel):
    name = models.CharField(max_length=100)
    facility_icon = models.ImageField(upload_to="facility_icons/", null = True, blank = True) 

    def __str__(self):
        return self.name

class Project(AbstractBaseModel):
    title = models.CharField(max_length=100)
    neighborhood = models.ForeignKey(Neighborhood, related_name="projects", on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField()
    average_rating = models.DecimalField(max_digits=2, decimal_places=1, default=5.0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    address = models.TextField()
    facilities = models.ManyToManyField(Facility, related_name="projects")
    cover_img = models.ImageField(upload_to = "project_cover_images/", null = True, blank = True)
    slug = models.SlugField(unique=True, max_length=150, blank=True)
    latitude = models.FloatField(null=True, blank=True, default=1.45648)
    longitude = models.FloatField(null=True, blank=True, default=1.45648)
    offer = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(100)], null=True, blank=True, default=0)
    
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
    

class ProjectImage(AbstractBaseModel):
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='image')
    image = models.ImageField(upload_to='project_images/', null = True, blank = True) 

    def __str__(self):
        return self.project.title + ' Image'
    
class ProjectVideo(models.Model):
    project = models.ForeignKey(Project, related_name='videos', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    video_file = models.FileField(upload_to='project_videos/')
    description = models.TextField(null=True, blank=True)

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

    name = models.CharField(max_length=100)
    description = models.TextField()
    project = models.ForeignKey('Project', related_name='properties', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', related_name='categories', on_delete=models.CASCADE)
    latitude = models.FloatField(null=True, blank=True, default=1.45648)
    longitude = models.FloatField(null=True, blank=True, default=1.45648)
    price_per_nft = models.DecimalField(max_digits=10, decimal_places=2)
    area = models.DecimalField(max_digits=10, decimal_places=2)
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    purpose = models.CharField(max_length = 255)
    furnished = models.BooleanField()
    parking_space_count = models.IntegerField()
    master_count = models.IntegerField()
    heating_option = models.CharField(max_length=50, choices=HEATING_OPTIONS, default='none')
    has_maid_room = models.BooleanField()
    has_swimming_pool = models.BooleanField()
    has_steam_room = models.BooleanField()
    average_rating = models.DecimalField(max_digits=2, decimal_places=1, default=5.0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    cover_img = models.ImageField(upload_to = "property_cover_images/", null = True, blank = True)
    floor = models.IntegerField(null=True, blank=True, default=1)
    unit_number = models.IntegerField(null=True, blank=True, default=1)
    likes = models.IntegerField(default=0)
    offer = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(100)], null=True, blank=True, default=0)

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
    image = models.ImageField(upload_to='Property_images/', null = True, blank = True)

    def __str__(self):
        return self.property.project.title + ' Image'
    
class PropertyVideo(models.Model):
    property = models.ForeignKey(Property, related_name='videos', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    video_file = models.FileField(upload_to='property_videos/')
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title

class PropertyLike(models.Model):
    user = models.ForeignKey(User, related_name='propertylikes', on_delete=models.CASCADE)
    property = models.ForeignKey(Property, related_name='propertylikes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'property')
    
class Category(AbstractBaseModel):
    title = models.CharField(max_length=100)
    category_icon = models.ImageField(upload_to="category_images/", null=True, blank=True)

    def __str__(self) -> str:
        if len(self.title) > 50:
            return self.title[:50] + "..."
        return self.title


class Banner(AbstractBaseModel):
    title = models.TextField()
    banner_img = models.ImageField(upload_to="banner_images/", null=True, blank=True)

    def __str__(self) -> str:
        if len(self.title) > 50:
            return self.title[:50] + "..."
        return self.title