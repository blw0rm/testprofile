from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from models import UserProfile

class ModelTest(TestCase):
    def test_fixtures_loaded(self):
        users_count = User.objects.count()
        profiles_count = UserProfile.objects.count()
        self.assertEqual(users_count, 2)
        self.assertEqual(profiles_count,2)
    
    def test_existance_profiles(self):
        ivan = User.objects.get(username='ivan')
        petr = User.objects.get(username='petr')
        try:
            ivan.get_profile()
        except UserProfile.DoesNotExist:
            self.fail() 
        try:
            petr.get_profile()
        except UserProfile.DoesNotExist:
            self.fail()
            
class ViewTest(TestCase):
    def test_login_page(self):
        client =Client()
        response = client.post("/accounts/login/?next=/", {'username':'ivan',
                                                'password':'passwd'})
        self.assertRedirects(response,'/',status_code=302, target_status_code=200)

        

class GeneralTests(TestCase):
    def test_context_processor(self):
        client = Client()
        client.login(username='ivan', password='passwd')
        response = client.get('/')
        if isinstance(response.context, dict):
            contexts = [response.context,]
        else:
            contexts = response.context
        
        for item in contexts:
            if item.has_key('settings'):
                return True
        return False

