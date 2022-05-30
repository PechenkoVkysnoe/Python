from django.db import models
from django.contrib.contenttypes.models import ContentType

class LatestProductsManager:

    @staticmethod
    def get_products_for_main_page(*args, **kwargs):
        with_respect_to = kwargs.get('with_respect_to')
        products = []
        ct_models = ContentType.objects.filter(model__in=args)

        for ct_model in ct_models:
            model_products = ct_model.model_class()._base_manager.all().order_by('-id')[:2]
            products.extend(model_products)

        if with_respect_to:
            ct_model = ContentType.objects.filter(model=with_respect_to)

            if ct_model.exists():
                if with_respect_to in args:
                    return sorted(products, key=lambda x: x.__class__._meta.model_name.startswith(with_respect_to),
                                  reverse=True)

        return products


#
class LatestProducts:
    objects = LatestProductsManager()


def get_models_for_count(*model_names):
    print([models.Count(model_name) for model_name in model_names])
    return [models.Count(model_name) for model_name in model_names]

class CategoryManager(models.Manager):
    CATEGORY_NAME_COUNT_NAME = {
        'Сукенка': 'dress__count',
        'Кашуля': 'short__count',
        'Рубаха': 'longshort__count'
    }


    def get_categories_for_left_sidebar(self):
        models = get_models_for_count('dress', 'short', 'longshort')
        qs = list(self.get_queryset().annotate(*models))
        data = [
            dict(name=c.name, url=c.get_absolute_url(), count=getattr(c, self.CATEGORY_NAME_COUNT_NAME[c.name]))
            for c in qs
        ]

        return data