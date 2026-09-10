from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)            # Stores the category name, which must be unique.
    slug = models.SlugField(unique=True)                            # URL-friendly version of the category name. Used for clean and readable URLs.
    description = models.TextField(blank=True)                      # blank=True allows this field to be empty in forms and admin.
    created_at = models.DateTimeField(auto_now_add=True)            # Automatically stores the date and time when the category is created.

    def __str__(self):                                              # Returns the category name when the object is displayed as a string.
        return self.name
    
class Book(models.Model):
    category = models.ForeignKey(                                   # Links each book to a category.
        Category,                                                   # A book must belong to a category.
        on_delete=models.PROTECT,
        related_name="books"
    )

    name = models.CharField(max_length=200)                         # Stores the book name.
    slug = models.SlugField(unique=True)                            # URL-friendly version of the book name. Must be unique to avoid duplicate URLs.
    author = models.CharField(max_length=200)                       # Stores the name of author.
    isbn = models.CharField(max_length=13, unique=True)             # Stores the isb number of the book.
    publisher = models.CharField(max_length=200, blank=True)        # Stores the publisher of the book.
    publication_date = models.DateField(blank=True, null=True)      # Stores the publication date of the book.
    description = models.TextField()                                # Stores the full description of the book.
    price = models.DecimalField(max_digits=10, decimal_places=2)    # Stores the book price with exact decimal precision. DecimalField is preferred over FloatField for monetary values.
    stock = models.PositiveIntegerField(default=0)                  # Stores the number of books currently in stock. PositiveIntegerField prevents negative values.
    image = models.ImageField(                                      # Stores an optional book cover image.
        upload_to="books/",                                         # Images are uploaded to the "books/" directory.
        blank=True,
    )


    # Determines whether the book is available in the store. Inactive books can be hidden without deleting them.
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)            # Automatically stores when the book is created.
    updated_at = models.DateTimeField(auto_now=True)                # Automatically updates whenever the book is modified.

    def __str__(self):                                              # Returns the book name when the object is displayed as a string.
        return self.name