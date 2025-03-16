from django.db import models

from datetime import datetime

# Create your models here.

class Book(models.Model):
    title = models.CharField("სათაური", max_length=20, null=False, blank=False)
    author = models.CharField("ავტორი", max_length=30, null=False, blank=False)
    published_date = models.DateField("გამოცემულია", blank=True, null=True)
    genres = models.ManyToManyField("Genre", blank=False)
    borrowed_by = models.CharField("გამოტანილია", max_length=50, blank=True, null=True)
    borrow_date = models.DateTimeField("გატანის დრო", blank=True, null=True)


    def borrow(self, person_name):
        if self.borrowed_by:
            return {"message": "book is already borrowed"}
        
        self.borrowed_by = person_name
        self.borrow_date = datetime.now()

        Borrow.objects.create(
            person=person_name,
            book=self,
            returned=False,
        )
        self.save()

    def return_book(self):
        if not self.borrowed_by:
            raise ValueError("Book is not currently borrowed")

        borrow_record = Borrow.objects.filter(book=self, returned=False).first()
        if borrow_record:
            borrow_record.returned = True
            borrow_record.save()

        self.borrowed_by = None
        self.borrow_date = None
        self.save()

    @staticmethod
    def list_book_by_genre(genre):
        raise NotImplementedError
    
    @staticmethod
    def available_books():
        raise NotImplementedError
    
    @staticmethod
    def borrowed_books():
        raise NotImplementedError
    
    @staticmethod
    def get_by_title(title):
        raise NotImplementedError
    
    def __str__(self):
        return f"{self.title} by {self.author}"
    
    class Meta:
        verbose_name = "წიგნი"
        verbose_name_plural = "წიგნები"

class Genre(models.Model):
    name = models.CharField("ჟანრი", max_length=15, null=False, blank=False)
    description = models.TextField("აღწერა", null=False, blank=False)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "ჟანრი"
        verbose_name_plural = "ჟანრები"

class Borrow(models.Model):
    person = models.CharField("სახელი და გვარი", max_length=50, null=False, blank=False)
    book = models.ForeignKey(
        Book, 
        null=False, 
        blank=False, 
        related_name="borrowed_history", 
        on_delete=models.DO_NOTHING,
    )

    date = models.DateField("გატანის დრო", auto_now_add=True)

    returned = models.BooleanField("დააბრუნა", default=False)

    def __str__(self):
        return f"გატანილია {self.person}-ის მიერ, {self.date}-ში"

    class Meta:
        verbose_name = "გატანა"
        verbose_name_plural = "გატანები"
