from django.test import TestCase
from django.urls import reverse


from .models import Food, FoodSubstitute, FoodsSaved
from .models import User


class TestViewsFood(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='Arthur', last_name='H',
                                        email='arthurH@gmail.com')
        self.user.set_password('1234')
        self.user.save()
        self.product = Food.objects.create(name='nutella', nutriscore='e')
        self.product.save()
        self.product_id = self.product.id
        self.substitute = FoodSubstitute.objects.create(name="confiture",
                                          image="",
                                          nutriscore="e",
                                          url="",
                                          food_id=self.product_id,
                                          nutriments_fat=0,
                                          nutriments_fat_saturated=0,
                                          nutriments_salt=0,
                                          nutriments_sugars=0)
        self.substitute.save()

        self.substitute_saved = FoodsSaved.objects.create(name="confiture",
                                          image="",
                                          nutriscore="e",
                                          url="",
                                          nutriments_fat="0",
                                          nutriments_fat_saturated="0",
                                          nutriments_salt="0",
                                          nutriments_sugars="0",
                                          user_id=self.user.id)
        self.substitute_saved.save()

    def test_index_page_return_200(self):
        """test that the index page returns a 200"""
        response = self.client.get(reverse('food:index'))
        self.assertEqual(response.status_code, 200)

    def test_substitutes_saved_user_return_200_user_logged(self):
        self.client.login(username="Arthur", password="1234")
        response = self.client.get(reverse('food:substitutes_saved_user'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'food/substitutes_saved_user.html')

    def test_substitutes_saved_user_return_300_user_not_logged(self):
        self.client.logout()
        response = self.client.get(reverse('food:substitutes_saved_user'))
        self.assertEqual(response.status_code, 302)

    def test_food_details_return_200(self):
        response = self.client.get(
            reverse('food:details_food', args=(self.substitute.id,)))
        self.assertEqual(response.status_code, 200)

    def test_food_details_return_404(self):
        substitute_id = self.substitute.id + 1
        response = self.client.get(
            reverse('food:details_food', args=(substitute_id,)))
        self.assertEqual(response.status_code, 404)

    def test_food_saved_details_return_200(self):
        response = self.client.get(
            reverse('food:details_food_saved', args=(self.substitute_saved.id,)))
        self.assertEqual(response.status_code, 200)

    def test_food_saved_details_return_404(self):
        substitute_saved_id = self.substitute_saved.id + 1
        response = self.client.get(
            reverse('food:details_food_saved', args=(substitute_saved_id,)))
        self.assertEqual(response.status_code, 404)

    def test_new_food_saved(self):
        self.client.login(username="Arthur", password="1234")
        old_db_food_saved = FoodsSaved.objects.count()
        data = {"food_substitute_pk": self.substitute.id}
        response = self.client.post(reverse('food:save_food'), data)
        new_db_food_saved = FoodsSaved.objects.count()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(old_db_food_saved + 1, new_db_food_saved)

    def test_new_food_saved_not_login(self):
        self.client.logout()
        old_db_food_saved = FoodsSaved.objects.count()
        data = {"food_substitute_pk": self.substitute.id}
        response = self.client.post(reverse('food:save_food'), data)
        new_db_food_saved = FoodsSaved.objects.count()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(old_db_food_saved, new_db_food_saved)

    def test_research(self):
        data = {"food_research": "Cassoulet"}
        response = self.client.post(reverse('food:research'), data)
        self.assertEqual(response.status_code, 200)


