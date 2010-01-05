from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.contrib.admin import widgets
from models import UserProfile
from forms import UserProfileForm
from django.core.urlresolvers import reverse
import datetime
from django.template import Template, Context


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
    def __init__(self, *args):
        super(ViewTest, self).__init__(*args)
        self.client = Client()
        
    def test_login_page(self):
        response = self.client.post(reverse('auth_login')+"?next=/", {'username':'ivan',
                                                'password':'passwd'})
        self.assertRedirects(response,'/',status_code=302, target_status_code=200)
        
    def test_object_modifying_logging(self):
        ''' Test for logging of create, update, delete object actions'''
        from django.contrib.admin.models import LogEntry
        log_entry_count = LogEntry.objects.count() # saving number of log entries
        self.test_profile_change() # modifying model object
        new_count_entries = LogEntry.objects.count()
        self.assertNotEqual(log_entry_count, new_count_entries)

    def test_profile_change(self):
        ''' Tests wether profile changing is working '''
        changed_form_data = {"first_name": "Ivan", 
                        "last_name": "Ivanov",
                        "birthday": "1980-01-12", 
                        "biography": "changed biography",
                        "contacts": "ivan2@gmail.com"
                        }
        self.client.login(username='ivan', password='passwd')
        response = self.client.get(reverse('main_page'))
        user = response.context['user']
        profile = user.get_profile()
        form = UserProfileForm(data=changed_form_data, instance=profile)
        self.failIf(not form.is_valid())
        form.save()
        self.assertEqual(profile.biography, changed_form_data['biography'])
        self.assertEqual(user.email,"ivan2@gmail.com")

        
class GeneralTests(TestCase):
    def __init__(self, *args):
        super(GeneralTests, self).__init__(*args)
        self.client = Client()
        
    def test_context_processor(self):
        ''' Tests wether context processor works fine and puts settings to template context '''
        self.client.login(username='ivan', password='passwd')
        response = self.client.get(reverse('main_page'))
        if isinstance(response.context, dict):
            contexts = [response.context,]
        else:
            contexts = response.context
        
        for item in contexts:
            if item.has_key('settings'):
                settings = item['settings']
                # checks the access to params of settings
                if hasattr(settings,'TIME_ZONE'):
                    return True

        return False
    
    def test_form_widget(self):
        ''' Test for calendar widget existance in the profile form '''
        form = UserProfileForm()
        if isinstance(form.fields['birthday'].widget, widgets.AdminDateWidget):
            return True
        return False
    
    def test_tag(self):
        rendered = Template('{% load adminurl %}{% admin_url "profile" %}')
        
        self.client.login(username='ivan', password='passwd')
        response = self.client.get(reverse('main_page'))
        user = response.context['user']
        profile = user.get_profile()
        
        context = Context({"profile":profile,})
        tag_url = rendered.render(context)
        url = "/admin/%s/%s/%s/" % (profile._meta.app_label,
                                        profile._meta.module_name,
                                        profile.id)
        
        self.assertEqual(tag_url, url)
        response = self.client.get(tag_url)
        self.assertEqual(response.status_code, 200)
        

        
class TestCommand(TestCase):
    class Output():
        def __init__(self):
            self.text=''
            
        def write(self, string):
            self.text = self.text + string
            
        def writelines(self, lines):
            for line in lines:
                self.write(line)
                
    def test_command(self):
        ''' Test for command that lists all models and number objects in it '''
        import sys
        from django.core.management import call_command
        savedstreams = sys.stdin, sys.stdout
        sys.stdout = self.Output()
        call_command('listmodels')
        response = sys.stdout.text
        # restore stdin and stdout streams
        sys.stdin, sys.stdout = savedstreams
        if response:
            # If command return some text, test passed successfull
            return True
        return False
        
