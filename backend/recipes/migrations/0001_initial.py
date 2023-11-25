# Generated by Django 3.2.16 on 2023-11-25 06:12

import colorfield.fields
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Favorites',
                'verbose_name_plural': 'Favorites',
                'ordering': ('recipe',),
                'abstract': False,
                'default_related_name': 'favorites',
            },
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, help_text='Enter a unique ingredient name.', max_length=200, verbose_name='Ingredient name')),
                ('measurement_unit', models.CharField(help_text='Enter the unit of measurement for the ingredient.', max_length=256, verbose_name='Measurement unit')),
            ],
            options={
                'verbose_name': 'Ingredient',
                'verbose_name_plural': 'Ingredients',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='IngredientInRecipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveSmallIntegerField(default=1, help_text='Please indicate the quantity of ingredients.', validators=[django.core.validators.MinValueValidator(1, {'ingredient min': 'The number of ingredients must be >=1.'}), django.core.validators.MaxValueValidator(9000, {'ingredient max': 'Too many ingredients'})], verbose_name='Amount of ingredients')),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='amount', to='recipes.ingredient', verbose_name='Ingredient')),
            ],
            options={
                'verbose_name': 'Ingredient in recipe',
                'verbose_name_plural': 'Ingredients in recipes',
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Enter a unique recipe name.', max_length=200, verbose_name='Recipe name')),
                ('image', models.ImageField(blank=True, upload_to='recipes/', verbose_name='Recipe image')),
                ('text', models.TextField(help_text='Add a recipe description.', verbose_name='Recipe description')),
                ('cooking_time', models.IntegerField(default=1, help_text='Enter the cooking time for the recipe in minutes.', validators=[django.core.validators.MinValueValidator(1, {'Cooking time': 'Cooking time must be >=1 minute.'}), django.core.validators.MaxValueValidator(9000, {'Cooking time': 'Cooking time exceeds all norms!'})], verbose_name='Recipe preparation time in minutes.')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Recipe publication date.')),
                ('author', models.ForeignKey(help_text='Enter the unique name of the recipe author.', on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to=settings.AUTH_USER_MODEL, verbose_name='Recipe author')),
                ('ingredients', models.ManyToManyField(help_text='Add ingredients to recipe.', related_name='recipes', through='recipes.IngredientInRecipe', to='recipes.Ingredient', verbose_name='Ingredients in the recipe.')),
            ],
            options={
                'verbose_name': 'Recipe',
                'verbose_name_plural': 'Recipes',
                'ordering': ('name', 'pub_date'),
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Enter a unique tag name.', max_length=200, unique=True, verbose_name='Tag name')),
                ('color', colorfield.fields.ColorField(default='#FF0000', help_text='Select a tag color.', image_field=None, max_length=18, samples=None, unique=True, verbose_name='Hex color')),
                ('slug', models.SlugField(help_text='Enter a unique tag slug.', max_length=64, unique=True, verbose_name='Tag slug')),
            ],
            options={
                'verbose_name': 'Tag',
                'verbose_name_plural': 'Tags',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='ShoppingCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shopping_cart', to='recipes.recipe', verbose_name='Recipe')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shopping_cart', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Shopping cart',
                'verbose_name_plural': 'Shopping carts.',
                'ordering': ('recipe',),
                'abstract': False,
                'default_related_name': 'shopping_cart',
            },
        ),
        migrations.AddField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(db_index=True, help_text='Add recipe tags.', related_name='recipes', to='recipes.Tag', verbose_name='Recipe tags'),
        ),
        migrations.AddField(
            model_name='ingredientinrecipe',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='amount', to='recipes.recipe', verbose_name='Recipe'),
        ),
        migrations.AddConstraint(
            model_name='ingredient',
            constraint=models.UniqueConstraint(fields=('name', 'measurement_unit'), name='unique_ingredient_measurement_unit'),
        ),
        migrations.AddField(
            model_name='favorite',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to='recipes.recipe', verbose_name='Recipe'),
        ),
        migrations.AddField(
            model_name='favorite',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.AddConstraint(
            model_name='shoppingcart',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='unique_shopping_cart'),
        ),
        migrations.AddConstraint(
            model_name='favorite',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='unique_favorite'),
        ),
    ]
