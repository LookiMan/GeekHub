from django.conf import settings


class Cart(object):
    def __init__(self, request):
        self.request = request
        self.session = request.session
        self.cart = self.session.setdefault(settings.CART_SESSION_ID, {})

    @property
    def keys(self):
        return tuple(map(int, self.cart.keys()))

    @property
    def products(self):
        return tuple(self.cart.values())

    def add(self, product, quantity=1):
        item = self.cart.setdefault(str(product.pk), {})

        if item:
            item["quantity"] += quantity
        else:
            item.update({
                'pk': product.pk,
                'name': product.name,
                'quantity': quantity,
                'price': str(product.price),
            })
        self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, product):
        pk = str(product.pk)
        if pk in self.cart:
            del self.cart[pk]
            self.save()

    def clear(self):
        self.session[settings.CART_SESSION_ID] = {}
        self.session.modified = True

    @property
    def amount_products(self):
        return len(self.cart)
