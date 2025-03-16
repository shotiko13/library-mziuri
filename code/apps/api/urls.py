from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from ninja import NinjaAPI

from apps.book.api import router as BookRouter


# from apps.module.api import router as ModuleRouter
# from apps.user.api import router as UserRouter
# from apps.calculator.api import router as CalculatorRouter


def superuser_required(
    view_func=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url="/"
):
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_superuser,
        login_url=login_url,
        redirect_field_name=redirect_field_name,
    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator


api = NinjaAPI(
    csrf=False,
    docs_url="/docs",
    title="Library API",
    docs_decorator=superuser_required,
    urls_namespace="api"
)


api.add_router("/library/", BookRouter, tags=["Books & Borrowing"])
