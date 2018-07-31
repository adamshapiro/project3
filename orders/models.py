from django.db import models
from django.contrib.auth.models import User
# PolymorphicModel allows referencing all subclasses of an ORM model and treating
# each instance as a member of its real class instead of a member of the parent
# eg the food in an OrderItem would be of type Pizza instead of Food
from polymorphic.models import PolymorphicModel

# Create your models here.

# Food and its subclasses refer to abstractions of menu items
class Food(PolymorphicModel):
    name = models.CharField(max_length=64)
    large_price = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return self.name

class Pizza(Food):
    PIZZA_TYPES = (
        ('R', 'Regular'),
        ('S', 'Sicilian')
    )
    type = models.CharField(max_length=1, choices=PIZZA_TYPES)
    small_price = models.DecimalField(max_digits=4, decimal_places=2)
    toppings_count = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} Pizza"

class Topping(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

class AddOn(models.Model):
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=3, decimal_places=2)

    def __str__(self):
        return self.name

class Sub(Food):
    small_price = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    add_ons = models.ManyToManyField(AddOn)

    @property
    def has_small(self):
        return hasattr(self, 'small_price') and self.small_price is not None

    def __str__(self):
        return f"{self.name} Sub"

class Pasta(Food):
    pass

class Salad(Food):
    pass

class DinnerPlatter(Food):
    small_price = models.DecimalField(max_digits=4, decimal_places=2)

# OrderItem and Order refer to instances of menu items on a customers order
class Order(models.Model):
    STATUS_OPTIONS = (
        ('o', 'ongoing'),
        ('p', 'pending'),
        ('c', 'confirmed')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    status = models.CharField(max_length=1, choices=STATUS_OPTIONS, default='p')

    @property
    def total(self):
        sum = 0
        for item in self.items.all():
            sum = sum + item.price
        return sum

    def __str__(self):
        return f"${self.total} Order for {self.user}"

class OrderItem(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE, related_name="+")
    toppings = models.ManyToManyField(Topping, related_name="+")
    add_ons = models.ManyToManyField(AddOn, related_name="+")
    price = models.DecimalField(max_digits=4, decimal_places=2)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")

    def new_add_on(self, id):
        option = AddOn.objects.get(pk=1)
        self.add_ons.add(option)
        self.price = self.price + option.price

    def get_add_ons(self):
        return self.add_ons.all()

    def new_topping(self, id):
        option = Topping.objects.get(pk=1)
        self.toppings.add(option)

    def get_toppings(self):
        return self.toppings.all()

    def __str__(self):
        if hasattr(self.food, 'type'):
            return f"{self.food} ({self.food.get_type_display()})"
        else:
            return f"{self.food}"

class ShoppingCart(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    order = models.OneToOneField(Order,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+")

    def __str__(self):
        return f"Shopping cart for {self.owner}"
