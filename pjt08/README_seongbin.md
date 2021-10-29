# README_seongbin

A. 프로젝트 구조 

driver: 윤성빈

페어 프로젝트를 하면서 계속 A 단계를 맡아서 했었는데 오늘은 깃이그노어 파일을 만들기도 전에 

가상환경을 만들어서 페어와 push, pull 하는 과정에서 계속 가상환경 오류가 생겼었다.

매번 가상환경을 지우고 다시 설치하는 번거로움이 있었다. 다시한번 프로젝트 초기셋팅 단계를 

단계화해서 공부해야겠다고 느꼈다.



E . Serializer & View

1.  Actor

```python
class ActorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ('id', 'name',)

class ActorSerializer(serializers.ModelSerializer):

    class MovieSerializer(serializers.ModelSerializer):
        class Meta:
            model = Movie
            fields = ('id', 'title','overview','release_date','poster_path')
        
    name = serializers.CharField(min_length=1, max_length=100)
    movies = MovieSerializer(many=True, read_only=True)

    class Meta:
        model = Actor
        fields = ('id', 'name', 'movies')
```



2.  Movie

```python
class MovieListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Movie
        fields = ('pk', 'title',)

class MovieSerializer(serializers.ModelSerializer):

    class ActorSerializer(serializers.ModelSerializer):
        class Meta:
            model = Actor
            fields = ('pk', 'name',)

    class ReviewSerializer(serializers.ModelSerializer):
        class Meta:
            model = Review
            fields = ('pk', 'title',)

    title = serializers.CharField(min_length=2, max_length=100)
    actors = ActorSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)

    actor_pks = serializers.ListField(write_only=True)

    class Meta:
        model = Movie
        fields = ('id', 'title', 'actors', 'reviews', 'actor_pks')
```



3. Review

```python
class TopReviewListSerializer(serializers.ModelSerializer):

    class MovieSerializer(serializers.ModelSerializer):
        class Meta:
            model = Review
            fields = ('pk', 'title',)

    movie = MovieSerializer(many=True)

    class Meta:
        model = Review
        fields = ('pk', 'title', 'movie')

class ReviewSerializer(serializers.ModelSerializer):

    class MovieSerializer(serializers.ModelSerializer):
        class Meta:
            model = Movie
            fields = '__all__'

    content = serializers.CharField(required=False)
    movie = MovieSerializer(many=True, read_only=True)

    class Meta:
        model = Review
        fields = ('pk', 'title', 'movie', 'content')

    def create(self, validated_data):
        actor_pks = validated_data.pop('actor_pks')
        review = Review.objects.create(**validated_data)
        for actor_pk in actor_pks:
            review.actors.add(actor_pk)
        return review

    def update(self, review, validated_data):
        actor_pks = validated_data.pop('actor_pks')
        for attr, value in validated_data.items():
            setattr(review, attr, value)
        review.save()

        review.artists.clear()
        for actor_pk in actor_pks:
            review.artists.add(actor_pk)
        return review
```

오전에 유튜브 강의를 보지않았다면 절대 코드를 작성하지 못했을 것 같다. 지금까지 했던 페어프로젝트 중에서 가장 난이도가 높았다. 각 모델 별로 db가 어떻게 연결되어있는지, 그걸 어떻게 나타낼건지 페어와 함께 생각해보면서 겨우겨우 코드를 작성해나갔다. 시간은 오래 걸렸지만 다 작성하고 동작하는 서버를 보니 뿌듯했다.



전체적으로 코드를 다 짜고 서버를 실행시켜보니 다른 url들은 접속이 잘 되는데 top_review 접속에서 타입에러가 발생했다. 어느 부분에서 정확히 에러가 났는지 장고가 알려주지않아서 에러를 30분간 페어와 같이 찾다가 포기했다. 