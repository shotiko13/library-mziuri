# Generated by Django 5.1.7 on 2025-03-13 16:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("book", "0002_genre_alter_book_options_book_author_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="book",
            name="borrow_date",
            field=models.DateTimeField(
                blank=True, null=True, verbose_name="გატანის დრო"
            ),
        ),
        migrations.AddField(
            model_name="book",
            name="borrowed_by",
            field=models.CharField(
                blank=True, max_length=50, null=True, verbose_name="გამოტანილია"
            ),
        ),
        migrations.AddField(
            model_name="borrow",
            name="returned",
            field=models.BooleanField(default=False, verbose_name="დააბრუნა"),
        ),
        migrations.AlterField(
            model_name="borrow",
            name="book",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="borrowed_history",
                to="book.book",
            ),
        ),
    ]
