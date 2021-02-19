from shlex import join

from woocommerce import API

from tahaApp.models import Product, Shop


def get_products(shop: Shop):
    wcapi = API(
        url=shop.url,
        consumer_key=shop.consumer_key,
        consumer_secret=shop.consumer_secret,
        version="wc/v3"
    )
    fields = ["id", "name", "images", "description", "categories", "permalink",
              "date_created_gmt", "date_modified_gmt"]
    r = wcapi.get("products", params={"fields": {{fields | join: ","}}, "per_page": "1"})

    # products = r.json()
    # for product in products:
    #     p = Product()
    #     p.name = product['name']
    #     p.save()
    #     return p.id
    return r.json()
