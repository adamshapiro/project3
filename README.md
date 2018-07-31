# Project 3

### Web Programming with Python and JavaScript

This website allows visitors, after signing up, to view the menu for Pinocchio's,
add menu items to a personal shopping cart, and finally confirm their order. Users
can then view past orders, including whether they have been confirmed by a
staff member.
The following files are used:

### HTML
---
* [index.html](/orders/templates/orders/index.html): The menu page where users can add
    food to their cart.

* [cart.html](/orders/templates/orders/cart.html): A view of all items in a users
    cart, where they can confirm their order.

* [orders.html](/orders/templates/orders/orders.html): A view of past orders with
    pending status.

* [all_orders.html](/orders/templates/orders/all_orders.html): A staff-only display
    of every users orders, where a staff member can confirm the order.

* [login.html](/orders/templates/orders/login.html): A login/register form.

* [layout.html](/orders/templates/orders/layout.html): The basic layout extended
    by all other HTML pages. Includes the JS scripts and navbar.

### CSS
---
* This project uses Bootstrap and JQuery almost entirely for styling elements and
    does not have its own CSS file.

### JavaScript
---
* [index.js](/orders/static/orders/index.js): Controls menu functionality for
    adding orders to a user's cart.

* [all_orders.js](/orders/static/orders/all_orders.js): Controls functionality for
    staff to update an order's status from pending to confirmed.

* [login.js](/orders/static/orders/login.js): Assists display functionality for
    the login and register forms.

### Python
---
* [urls.py](/orders/urls.py): Controls rules for connecting URL routes to views.

* [views.py](/orders/views.py): Controls server side functionality of rendering
    HTML pages and submitting data to the database.

* [forms.py](/orders/forms.py): Form information for the register and login views.

* [models.py](/orders/models.py): Django ORM models for DB tables. includes:
    * Food: Menu items are all subclasses of the Food model.
    * Topping and AddOn: Toppings and Sub add-ons are their own models.
    * Order and OrderItem: Models for mapping menu items to user orders.
    * ShoppingCart: Model mapping an ongoing order to a user.

* [admins.py](/orders/admins.py): File that determines which models an admin can
    create instances for via the /admin url route.

### MISC
---
* [requirements.txt](/requirements.txt): A list of python modules that must be
    installed before running the application. Django-polymorphic is added to
    make the Food model polymorphic, meaning that querying the Food model will
    return a list of instances of subclasses, rather than being cast to Food.

### Notes
---
* The personal touch in this project is the allowance for users to view past orders
    and whether they are pending or confirmed, and allowing staff to view all past
    orders and confirm pending orders.
