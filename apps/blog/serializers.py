from rest_framework import serializers
from apps.blog.communication import communication_mail
from apps.blog.models import Blog, Communication, Gallery, Service, PatientStories, Award, Event, Subscription
from apps.blog.subscription import subscription_mail
from breathline.helpers.helper import base64_file_extension, base64_to_file, get_object_or_none, get_token_user_or_none
import uuid


def base64withextension(file):
    extension = base64_file_extension(file)
    converted_file = base64_to_file(file)
    return f'{uuid.uuid4()}.{extension}', converted_file


class CreateOrUpdateBlogSerializer(serializers.ModelSerializer):
    id                              = serializers.IntegerField(required=False, allow_null=True)
    title                           = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    sub_title                       = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    description                     = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    author                          = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    blog_image                      = serializers.CharField(allow_null=True, allow_blank=True, required=False) 

    meta_title                      = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    meta_image_title                = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    meta_description                = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    meta_keywords                   = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    og_image                        = serializers.CharField(allow_null=True, allow_blank=True, required=False)

    class Meta:
        model = Blog
        fields = ['id', 'title', 'sub_title', 'description', 'author', 'blog_image', 'meta_title', 'meta_image_title', 'meta_description', 'meta_keywords', 'og_image']

    def validate(self, attrs):
        max_size = 1 * 1024 * 1024
        if attrs.get('blog_image'):
            _, file = base64withextension(attrs.get('blog_image'))
            if file.size > max_size:
                raise serializers.ValidationError({"blog_image": "Image size must be less than 1 MB."})
        return super().validate(attrs)

    def create(self, validated_data):
        request       = self.context.get('request', None)
        user_instance = get_token_user_or_none(request)

        instance                     = Blog()
        instance.title               = validated_data.get('title')
        instance.sub_title           = validated_data.get('sub_title')
        instance.description         = validated_data.get('description')
        instance.author              = validated_data.get('author')

        if validated_data.get('blog_image'):
            filename, file = base64withextension(validated_data.get('blog_image'))
            instance.blog_image.save(filename, file, save=False)


        instance.meta_title          = validated_data.get('meta_title')
        instance.meta_image_title    = validated_data.get('meta_image_title')
        instance.meta_description    = validated_data.get('meta_description')
        instance.meta_keywords       = validated_data.get('meta_keywords')

        if validated_data.get('og_image'):
            filename, file = base64withextension(validated_data.get('og_image'))
            instance.og_image.save(filename, file, save=False)

        instance.created_by             = user_instance
        instance.modified_by            = user_instance
        instance.save()

        return instance

    def update(self, instance, validated_data):
        request       = self.context.get('request', None)
        user_instance = get_token_user_or_none(request)

        instance.title                = validated_data.get('title', instance.title)
        instance.sub_title            = validated_data.get('sub_title', instance.sub_title)
        instance.description          = validated_data.get('description', instance.description)
        instance.author               = validated_data.get('author', instance.author)

        if validated_data.get('blog_image'):
            filename, file = base64withextension(validated_data.get('blog_image'))
            instance.blog_image.save(filename, file, save=False)


        instance.meta_title          = validated_data.get('meta_title', instance.meta_title)
        instance.meta_image_title    = validated_data.get('meta_image_title', instance.meta_image_title)
        instance.meta_description    = validated_data.get('meta_description', instance.meta_description)
        instance.meta_keywords       = validated_data.get('meta_keywords', instance.meta_keywords)

        if validated_data.get('og_image'):
            filename, file = base64withextension(validated_data.get('og_image'))
            instance.og_image.save(filename, file, save=False)

        instance.modified_by            = user_instance
        instance.save()

        return instance
    


class DeleteBlogSerializer(serializers.ModelSerializer):
    id = serializers.ListField(child=serializers.IntegerField(),required=True)

    class Meta:
        model  = Blog
        fields = ['id'] 


class CreateOrUpdateServiceSerializer(serializers.ModelSerializer):
    id                              = serializers.IntegerField(required=False, allow_null=True)
    service_category                = serializers.ChoiceField(required=False, choices=Service.Service_Category.choices, allow_blank=True, allow_null=True)
    service_video_url               = serializers.URLField(required=False, allow_null=True)

    class Meta:
        model = Service
        fields = ['id', 'service_category', 'service_video_url']

    def validate(self, attrs):
        service_id       = attrs.get("id", None)
        service_category = attrs.get("service_category", None)

        if service_category:
            existing = Service.objects.filter(service_category=service_category)

            if service_id:
                existing = existing.exclude(id=service_id)

            if existing.count() >= 3:
                raise serializers.ValidationError({
                    "service_category": "A service category can only have up to 3 items."
                })

        return attrs

    def create(self, validated_data):
        request = self.context.get('request', None)
        user_instance = get_token_user_or_none(request)

        instance                         = Service()
        instance.service_category        = validated_data.get('service_category')
        instance.service_video_url       = validated_data.get('service_video_url')

        instance.created_by              = user_instance
        instance.modified_by             = user_instance
        instance.save()
        return instance

    def update(self, instance, validated_data):
        request = self.context.get('request', None)
        user_instance = get_token_user_or_none(request)

        instance.service_category        = validated_data.get('service_category', instance.service_category)
        instance.service_video_url       = validated_data.get('service_video_url', instance.service_video_url)

        instance.modified_by             = user_instance
        instance.save()
        return instance
    


class DeleteServiceSerializer(serializers.ModelSerializer):
    id = serializers.ListField(child=serializers.IntegerField(),required=True)

    class Meta:
        model  = Service
        fields = ['id'] 
    


class CreateOrUpdatePatientStoriesSerializer(serializers.ModelSerializer):
    id                              = serializers.IntegerField(required=False, allow_null=True)
    name                            = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    rating                          = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    description                     = serializers.CharField(allow_null=True, allow_blank=True, required=False) 

    class Meta:
        model = PatientStories
        fields = ['id', 'name', 'rating', 'description']

    def validate(self, attrs):
        return super().validate(attrs)

    def create(self, validated_data):
        request       = self.context.get('request', None)
        user_instance = get_token_user_or_none(request)

        instance                     = PatientStories()
        instance.name                = validated_data.get('name')
        instance.rating              = validated_data.get('rating')
        instance.description         = validated_data.get('description')

        instance.created_by             = user_instance
        instance.modified_by            = user_instance
        instance.save()

        return instance

    def update(self, instance, validated_data):
        request       = self.context.get('request', None)
        user_instance = get_token_user_or_none(request)

        instance.name                = validated_data.get('name', instance.name)
        instance.rating              = validated_data.get('rating',instance.rating)
        instance.description         = validated_data.get('description', instance.description)


        instance.modified_by            = user_instance
        instance.save()

        return instance
    

class DeletePatientStoriesSerializer(serializers.ModelSerializer):
    id = serializers.ListField(child=serializers.IntegerField(),required=True)

    class Meta:
        model  = PatientStories
        fields = ['id']
    

"""Gallery"""
class CreateOrUpdateGallerySerializer(serializers.ModelSerializer):
    id                              = serializers.IntegerField(required=False, allow_null=True)
    image                           = serializers.CharField(allow_null=True, allow_blank=True, required=False) 

    class Meta:
        model = Gallery
        fields = ['id', 'image']

    def validate(self, attrs):
        max_size = 1 * 1024 * 1024
        if attrs.get('image'):
            _, file = base64withextension(attrs.get('image'))
            if file.size > max_size:
                raise serializers.ValidationError({"image": "Image size must be less than 1 MB."})
        return super().validate(attrs)

    def create(self, validated_data):
        request       = self.context.get('request', None)
        user_instance = get_token_user_or_none(request)

        instance                     = Gallery()

        if validated_data.get('image'):
            filename, file = base64withextension(validated_data.get('image'))
            instance.image.save(filename, file, save=False)

        instance.created_by             = user_instance
        instance.modified_by            = user_instance
        instance.save()

        return instance

    def update(self, instance, validated_data):
        request       = self.context.get('request', None)
        user_instance = get_token_user_or_none(request)

        if validated_data.get('image'):
            filename, file = base64withextension(validated_data.get('image'))
            instance.image.save(filename, file, save=False)


        instance.modified_by            = user_instance
        instance.save()

        return instance
    

class DeleteGallerySerializer(serializers.ModelSerializer):
    id = serializers.ListField(child=serializers.IntegerField(),required=True)

    class Meta:
        model  = Gallery
        fields = ['id']
    


class CreateOrUpdateAwardSerializer(serializers.ModelSerializer):
    id                              = serializers.IntegerField(required=False, allow_null=True)
    award_image                     = serializers.CharField(allow_null=True, allow_blank=True, required=False) 

    class Meta:
        model = Award
        fields = ['id', 'award_image']

    def validate(self, attrs):
        max_size = 1 * 1024 * 1024
        if attrs.get('award_image'):
            _, file = base64withextension(attrs.get('award_image'))
            if file.size > max_size:
                raise serializers.ValidationError({"award_image": "Image size must be less than 1 MB."})
        return super().validate(attrs)

    def create(self, validated_data):
        request       = self.context.get('request', None)
        user_instance = get_token_user_or_none(request)

        instance                     = Award()

        if validated_data.get('award_image'):
            filename, file = base64withextension(validated_data.get('award_image'))
            instance.award_image.save(filename, file, save=False)

        instance.created_by             = user_instance
        instance.modified_by            = user_instance
        instance.save()

        return instance

    def update(self, instance, validated_data):
        request       = self.context.get('request', None)
        user_instance = get_token_user_or_none(request)

        if validated_data.get('award_image'):
            filename, file = base64withextension(validated_data.get('award_image'))
            instance.award_image.save(filename, file, save=False)


        instance.modified_by            = user_instance
        instance.save()

        return instance
    

class DeleteAwardSerializer(serializers.ModelSerializer):
    id = serializers.ListField(child=serializers.IntegerField(),required=True)

    class Meta:
        model  = Award
        fields = ['id']


class CreateOrUpdateEventSerializer(serializers.ModelSerializer):
    id                              = serializers.IntegerField(required=False, allow_null=True)
    description                     = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    event_image                     = serializers.CharField(allow_null=True, allow_blank=True, required=False) 

    class Meta:
        model = Event
        fields = ['id', 'description', 'event_image']

    def validate(self, attrs):
        max_size = 1 * 1024 * 1024
        if attrs.get('event_image'):
            _, file = base64withextension(attrs.get('event_image'))
            if file.size > max_size:
                raise serializers.ValidationError({"event_image": "Image size must be less than 1 MB."})
        return super().validate(attrs)

    def create(self, validated_data):
        request       = self.context.get('request', None)
        user_instance = get_token_user_or_none(request)

        instance                     = Event()
        instance.description         = validated_data.get('description')

        if validated_data.get('event_image'):
            filename, file = base64withextension(validated_data.get('event_image'))
            instance.event_image.save(filename, file, save=False)

        instance.created_by             = user_instance
        instance.modified_by            = user_instance
        instance.save()

        return instance

    def update(self, instance, validated_data):
        request       = self.context.get('request', None)
        user_instance = get_token_user_or_none(request)

        instance.description         = validated_data.get('description', instance.description)

        if validated_data.get('event_image'):
            filename, file = base64withextension(validated_data.get('event_image'))
            instance.event_image.save(filename, file, save=False)

        instance.modified_by            = user_instance
        instance.save()

        return instance
    

class DeleteEventSerializer(serializers.ModelSerializer):
    id = serializers.ListField(child=serializers.IntegerField(),required=True)

    class Meta:
        model  = Event
        fields = ['id']


"""Subscription"""
class CreateOrUpdateSubscriptionSerializer(serializers.ModelSerializer):
    id                              = serializers.IntegerField(required=False, allow_null=True)
    email                           = serializers.EmailField(required=True)

    class Meta:
        model = Subscription
        fields = ['id', 'email']

    def validate(self, attrs):
        email = attrs.get("email", None)

        if email:
            email = email.lower()
            attrs["email"] = email  

            existing = Subscription.objects.filter(email=email, is_subscribe=True).first()
            if existing:
                raise serializers.ValidationError({"email": "This email is already subscribed."})

        return super().validate(attrs)

    def create(self, validated_data):
        request       = self.context.get('request', None)
        user_instance = get_token_user_or_none(request)

        instance                     = Subscription()
        instance.email               = validated_data.get('email', None)

        instance.created_by             = user_instance
        instance.modified_by            = user_instance
        instance.save()

        subscription_mail(request, instance)

        return instance
    
    def update(self, instance, validated_data):
        request       = self.context.get('request', None)
        user_instance = get_token_user_or_none(request)

        instance.email               = validated_data.get('email', None)
        instance.is_subscribe        = True

        instance.created_by             = user_instance
        instance.modified_by            = user_instance
        instance.save()

        subscription_mail(request, instance)
        
        return instance
    



"""Communication"""
class CreateOrUpdateCommunicationSerializer(serializers.ModelSerializer):

    id                        = serializers.IntegerField(required=False,allow_null=True)
    name                      = serializers.CharField(allow_null=True,allow_blank=True,required=False)
    email                     = serializers.EmailField(required=False, allow_null=True, allow_blank=True)
    phonenumber               = serializers.CharField(allow_null=True,allow_blank=True,required=False)
    service_category          = serializers.ChoiceField(required=False, choices=Service.Service_Category.choices, allow_blank=True, allow_null=True)
    message                   = serializers.CharField(allow_null=True,allow_blank=True,required=False)

    class Meta:
        model  = Communication
        fields = ['id','name','email','phonenumber','service_category','message']

    def validate(self,attrs):
        return super().validate(attrs)

    def create(self,validated_data):
        request         = self.context.get('request',None)
        user_instance   = get_token_user_or_none(request)

        name = validated_data.get('name', None)
        if name:
            name = name.capitalize()

        instance                      = Communication()
        instance.name                 = name
        instance.email                = validated_data.get('email',None)
        instance.phonenumber          = validated_data.get('phonenumber',None)
        instance.service_category     = validated_data.get('service_category',None)
        instance.message              = validated_data.get('message',None)
        

        instance.created_by       = user_instance
        instance.modified_by      = user_instance

        instance.save()
            
        name             = instance.name if instance.name else None
        email            = instance.email if instance.email else None
        message          = instance.message if instance.message else None
        phonenumber      = instance.phonenumber if instance.phonenumber else None
        service_category = instance.service_category if instance.service_category else None

        communication_mail(
            request, 
            name, 
            email, 
            message,
            phonenumber,
            service_category,
            instance
        )

        return instance