from .models import Food, FoodSubstitute, FoodsSaved
from .api_openfoodfact import DataApi


class ResearchFood:
    def __init__(self):
        pass

    def delete_database(self):
        countdb = FoodSubstitute.objects.count()
        if countdb >= 1000:
            Food.objects.all().delete()

    def get_context_food(self, food_choose):
        data_api_openfoodfact = DataApi(food_choose)
        data_products_category = data_api_openfoodfact.select_key_test()

        name_food_nutriscore = data_api_openfoodfact.get_nutriscore_food_choose()
        name_food_category = data_api_openfoodfact.get_categories_name_food()

        if Food.objects.filter(name=food_choose).exists():
            name_food = Food.objects.get(name=food_choose)
        else:
            name_food = Food(name=food_choose,
                             nutriscore=name_food_nutriscore,
                             category=name_food_category)

            name_food.save()

            for data_product_category in data_products_category:
                name = (data_product_category[0])
                image = (data_product_category[1])
                nutriscore = (data_product_category[2])
                url = (data_product_category[3])
                fat = (data_product_category[4])
                fat_saturated = (data_product_category[5])
                sugar = (data_product_category[6])
                salt = (data_product_category[7])

                food_substitutes = FoodSubstitute(name=name,
                                                  image=image,
                                                  nutriscore=nutriscore,
                                                  url=url,
                                                  food_id=name_food.pk,
                                                  nutriments_fat=fat,
                                                  nutriments_fat_saturated=fat_saturated,
                                                  nutriments_salt=salt,
                                                  nutriments_sugars=sugar)
                food_substitutes.save()

        food_id = name_food.pk

        if name_food.nutriscore == "e":
            foods_substitutes = FoodSubstitute.objects.filter(
                food_id=int(food_id)).exclude(nutriscore="e")
        if name_food.nutriscore == "d":
            foods_substitutes = FoodSubstitute.objects.filter(
                food_id=int(food_id)).exclude(nutriscore="e").exclude(
                nutriscore="d")
        if name_food.nutriscore == "c":
            foods_substitutes = FoodSubstitute.objects.filter(
                food_id=int(food_id)).exclude(nutriscore="e").exclude(
                nutriscore="d").exclude(nutriscore="c")
        if name_food.nutriscore == "b":
            foods_substitutes = FoodSubstitute.objects.filter(
                food_id=int(food_id)).exclude(nutriscore="e").exclude(
                nutriscore="d").exclude(nutriscore="c").exclude(nutriscore="b")
        if name_food.nutriscore == "a":
            foods_substitutes = FoodSubstitute.objects.filter(
                food_id=int(food_id)).filter(nutriscore="a")

        context = {
            'foods_substitutes': foods_substitutes,
            'name_food': name_food
        }

        return context


class DatabaseSaveFood:
    def __init__(self):
        pass

    def save_food(self, food_substitute_choose, current_user):
        food_substitute_choose_save = FoodsSaved(
            name=food_substitute_choose.name,
            image=food_substitute_choose.image,
            nutriscore=food_substitute_choose.nutriscore,
            url=food_substitute_choose.url,
            user_id=current_user.id,
            nutriments_fat=food_substitute_choose.nutriments_fat,
            nutriments_fat_saturated=food_substitute_choose.nutriments_fat_saturated,
            nutriments_salt=food_substitute_choose.nutriments_salt,
            nutriments_sugars=food_substitute_choose.nutriments_sugars
        )
        food_substitute_choose_save.save()