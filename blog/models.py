from django.db import models


class Post(models.Model):
    title = models.CharField('TITLE', max_length=50)
    request = models.CharField('Request', max_length=20)
    price1 = models.CharField('Price1', max_length=20)
    price2 = models.CharField('Price2', max_length=20, blank=True, null=True)
    price3 = models.CharField('Price3', max_length=20, blank=True, null=True)
    kind = models.CharField('Kind', max_length=20)
    spec = models.CharField('Spec', max_length=50)
    description = models.CharField('DESCRIPTION', max_length=100, blank=True, null=True, help_text='simple one-line text.')
    agent = models.CharField('Agent', max_length=30, blank=True, null=True)
    register = models.CharField('Register', max_length=30)
    image = models.ImageField('IMAGE', upload_to='blog/%Y/%m/', blank=True, null=True)
    image1 = models.ImageField('IMAGE1', upload_to='blog/%Y/%m/', blank=True, null=True)

    category = models.ForeignKey('Category', on_delete=models.SET_NULL, blank=True, null=True)
    tags = models.ManyToManyField('Tag', blank=True)
    content = models.TextField('CONTENT')
    like = models.PositiveSmallIntegerField('LIKE', default=0)

    create_dt = models.DateTimeField('CREATE DT', auto_now_add=True)
    update_dt = models.DateTimeField('UPDATE DT', auto_now=True)
    class Meta:
        ordering = ('update_dt',)

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField('DESCRIPTION', max_length=100, blank=True, help_text='simple one-line text.')

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)
    content = models.TextField('CONTENT')
    create_dt = models.DateTimeField('CREATE DT', auto_now_add=True)
    update_dt = models.DateTimeField('UPDATE DT', auto_now=True)

    @property
    def short_content(self):
        return self.content[:10]

    def __str__(self):
        return self.short_content