from rest_framework import serializers
from accounts.models import Profile
from ...models import Post, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class PostSerializer(serializers.ModelSerializer):
    # content = serializers.ReadOnlyField()
    # content = serializers.CharField(read_only=True)
    snippet = serializers.ReadOnlyField(source='get_snippet')
    relative_url = serializers.URLField(source='get_absolute_api_url', read_only=True)
    absolute_url = serializers.SerializerMethodField()
    # category = serializers.SlugRelatedField(many=False, read_only=False, slug_field='name', queryset=Category.objects.all())
    # category = CategorySerializer()
    
    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'image', 'category', 'content', 'snippet', 'status', 'created_dt', 'published_dt', 'relative_url', 'absolute_url']
        read_only_fields = ['author']
    
    def get_absolute_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.pk)
    
    def to_representation(self, instance):
        request = self.context.get('request')
        rep = super().to_representation(instance)
        if request.parser_context.get('kwargs').get('pk'):
            rep.pop('snippet', None)
            rep.pop('relative_url', None)
            rep.pop('absolute_url', None)
        else:
            rep.pop('content', None)
        
        rep['category'] = CategorySerializer(instance.category).data
        return rep
    
    def create(self, validated_data):
        validated_data['author'] = Profile.objects.get(user=self.context.get('request').user)
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
    
    def is_valid(self, *, raise_exception=False):
        return super().is_valid(raise_exception=raise_exception)
