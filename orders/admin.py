from django.contrib import admin
from .models import Pizza, Topping, Sub, AddOn, Pasta, Salad, DinnerPlatter

# Register your models here.
admin.site.register(Pizza)
admin.site.register(Topping)
admin.site.register(Sub)
admin.site.register(AddOn)
admin.site.register(Pasta)
admin.site.register(Salad)
admin.site.register(DinnerPlatter)

## Note that OrderItem in models.py is used to wrap info for each entry in an
## order, and should never be manually created by an admin
