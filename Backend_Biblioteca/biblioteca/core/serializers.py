from rest_framework import serializers
from .models import Livro, Autor, Categoria

class AutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autor
        fields = ['id', 'nome']

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nome']

class LivroSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    titulo = serializers.CharField(max_length=200)
    autor = serializers.CharField(source='autor.nome', read_only=True)
    categoria = serializers.CharField(source='categoria.nome', read_only=True)
    autor_id = serializers.PrimaryKeyRelatedField(queryset=Autor.objects.all(), write_only=True)
    categoria_id = serializers.PrimaryKeyRelatedField(queryset=Categoria.objects.all(), write_only=True)
    publicado_em = serializers.DateField()

    def create(self, validated_data):
        autor = validated_data.pop('autor_id')
        categoria = validated_data.pop('categoria_id')
        return Livro.objects.create(autor=autor, categoria=categoria, **validated_data)

    def update(self, instance, validated_data):
        instance.titulo = validated_data.get('titulo', instance.titulo)
        instance.autor = validated_data.get('autor_id', instance.autor)
        instance.categoria = validated_data.get('categoria_id', instance.categoria)
        instance.publicado_em = validated_data.get('publicado_em', instance.publicado_em)
        instance.save()
        return instance
