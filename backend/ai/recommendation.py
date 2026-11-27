from models.customer import Customer
from models.product import Product


def recommend_product(customer_id):

    customer = Customer.query.get(customer_id)

    if not customer:
        return None

    # Get customer's preferred category
    preferred_category = customer.preferred_category

    if not preferred_category:
        return None

    # Find products from the preferred category
    products = (
        Product.query
        .filter(
            Product.category.ilike(preferred_category),
            Product.stock > 0
        )
        .order_by(Product.price.asc())
        .all()
    )

    if not products:
        return None

    # Recommend the first available product
    product = products[0]

    return {
        "customer_id": customer_id,
        "product_id": product.id,
        "product_name": product.product_name,
        "category": product.category,
        "price": product.price
    }