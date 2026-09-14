from django.core.paginator import Paginator
from django.db.models import Count, Sum, Q, Prefetch
from store.models import Product, Category


class ProductService:

    @staticmethod
    def get_filtered_products(request):
        # ===== فقط فیلدهای مورد نیاز را انتخاب کن (کاهش بار دیتابیس) =====
        products = (
            Product.objects
            .select_related("seller")  # برای جلوگیری از کوئری اضافی seller
            .prefetch_related(
                Prefetch("categories", queryset=Category.objects.only("name"))
            )
            .only(
                "id", "name", "price", "digital", "description", "image",
                "date_added", "is_available", "seller__name", "seller__id"
            )
        )

        # ===== فیلترها =====
        search_query = request.GET.get("q")
        if search_query:
            products = products.filter(name__icontains=search_query)

        max_price = request.GET.get("max_price")
        if max_price and max_price.isdigit():
            products = products.filter(price__lte=int(max_price))

        selected_categories = request.GET.getlist("category")
        if selected_categories:
            products = products.filter(categories__name__in=selected_categories).distinct()

        # ===== مرتب‌سازی =====
        sort_by = request.GET.get("sort")
        if sort_by == "price_asc":
            products = products.order_by("price")
        elif sort_by == "price_desc":
            products = products.order_by("-price")
        elif sort_by == "newest":
            products = products.order_by("-date_added")
        elif sort_by == "most_sold":
            products = products.annotate(
                total_sold=Sum(
                    "orderitem__quantity",
                    filter=Q(orderitem__order__complete=True),
                )
            ).order_by("-total_sold")
        elif sort_by == "most_liked":
            products = products.annotate(like_count=Count("productlike")).order_by("-like_count")
        else:
            products = products.order_by("-date_added")

        # ===== صفحه‌بندی =====
        paginator = Paginator(products, 10)
        page_number = request.GET.get("page")
        return paginator.get_page(page_number)