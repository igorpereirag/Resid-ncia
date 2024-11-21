from rest_framework import serializers
from .models import Livro, Autor, Categoria, Colecao

class AutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autor
        fields = ['id', 'nome']

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nome']

class LivroSerializer(serializers.ModelSerializer):
    autor = AutorSerializer(read_only=True)  
    categoria = CategoriaSerializer(read_only=True)  
    autor_id = serializers.PrimaryKeyRelatedField(queryset=Autor.objects.all(), write_only=True)
    categoria_id = serializers.PrimaryKeyRelatedField(queryset=Categoria.objects.all(), write_only=True)

    class Meta:
        model = Livro
        fields = [
            'id', 'titulo', 'autor', 'autor_id', 
            'categoria', 'categoria_id', 'publicado_em'
        ]

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

class ColecaoSerializer(serializers.ModelSerializer):
    livros = LivroSerializer(many=True, read_only=True)  
    livros_ids = serializers.PrimaryKeyRelatedField(
        queryset=Livro.objects.all(), write_only=True, many=True
    )  
    colecionador = serializers.StringRelatedField(read_only=True)  

    class Meta:
        model = Colecao
        fields = ['id', 'nome', 'descricao', 'livros', 'livros_ids', 'colecionador']

    def create(self, validated_data):
        livros_ids = validated_data.pop('livros_ids')
        colecao = Colecao.objects.create(**validated_data)
        colecao.livros.set(livros_ids) 
        return colecao

    def update(self, instance, validated_data):
        livros_ids = validated_data.pop('livros_ids', None)
        instance.nome = validated_data.get('nome', instance.nome)
        instance.descricao = validated_data.get('descricao', instance.descricao)
        if livros_ids is not None:
            instance.livros.set(livros_ids)  
        instance.save()
        return instance
