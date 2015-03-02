import psutil
from django.test import TestCase
from django.http import HttpRequest
from django.core.urlresolvers import resolve
from django.template.loader import render_to_string
from django.db import models
from socket import gethostname
from getpass import getuser

from views import home
from memoryconsumer.views import memcon_home
from memoryconsumer.models import Memloadstat, Experiment

# Create your tests here.

class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home)
        
    def test_home_returns_correct_html(self):
        request = HttpRequest()
        response = home(request)
        #expected_home_html = render_to_string('homepage.html')
        #self.assertEqual(response.content.decode(), expected_home_html)
        self.assertContains(response, "Host:")
        self.assertContains(response, "Gear:")
        
    def test_root_url_returns_correct_host_name(self):
        request = HttpRequest()
        response = home(request)
        expected_home_html = render_to_string('homepage.html')
        hostnm = gethostname()
        gearnm = getuser()
        self.assertContains(response, hostnm)
        self.assertContains(response, gearnm)
        
class MemoryconsumerPageTest(TestCase):
    def test_memcon_url_resolves_to_memcon_view(self):
        found =resolve('/memoryconsumer/')
        self.assertEqual(found.func, memcon_home)
        
    def test_memcon_home_returns_correct_html(self):
        request = HttpRequest()
        response = memcon_home(request)
        expected_memoryconsumer_html = render_to_string('memoryconsumer.html')
        self.assertEqual(response.content.decode(), expected_memoryconsumer_html)
                        
    def test_memcon_page_saves_items_only_when_necessary(self):
        request = HttpRequest()
        memcon_home(request)
        self.assertEqual(Memloadstat.objects.count(), 0)
      
 
class ExpViewTest(TestCase):
    def test_uses_exp_page_template(self):
        exp_ = Experiment.objects.create()
        response = self.client.get("/memoryconsumer/exp_page/%d/" % (exp_.id,))
        self.assertTemplateUsed(response, 'exp_page.html')
        
    def test_displays_only_memory_load_stats_for_this_user(self):
        first_exp = Experiment.objects.create()
        Memloadstat.objects.create(memload='1001', exp = first_exp )
        Memloadstat.objects.create(memload='1002', exp = first_exp )
        
        second_exp = Experiment.objects.create()
        Memloadstat.objects.create(memload='2001', exp = second_exp )
        Memloadstat.objects.create(memload='2002', exp = second_exp )
        
        response = self.client.get("/memoryconsumer/exp_page/%d/" % (first_exp.id,))
        
        self.assertContains(response, "1001")
        self.assertContains(response, "1002")
        self.assertNotContains(response, "2001")
        self.assertNotContains(response, "2002")
        
    def test_passes_correct_exp_to_template(self):
        other_exp = Experiment.objects.create()
        correct_exp = Experiment.objects.create()
        response = self.client.get("/memoryconsumer/exp_page/%d/" % (correct_exp.id,))
        self.assertEqual(response.context["exp"], correct_exp)

class NewMemloadstatTest(TestCase):
    def test_can_save_a_POST_request_to_an_existing_exp(self):
        other_exp = Experiment.objects.create()
        correct_exp = Experiment.objects.create()
        
        avail_mem_before = int(psutil.virtual_memory().available / 2**20)
        
        self.client.post(
            "/memoryconsumer/exp_page/%d/add_memloadstat" % (correct_exp.id,),
            data={"mem_load_text": "1000"}
        )
        
        avail_mem_after = int(psutil.virtual_memory().available / 2**20)
        
        self.assertEqual(Memloadstat.objects.count(), 1)
        new_memloadstat = Memloadstat.objects.first()
        
        self.assertEqual(new_memloadstat.memload, 1000)
        
        avail_delta = 96 #MB from established test of 1000 10KB elements
        
        self.assertEqual(
            new_memloadstat.availdelta, 
            avail_delta
        )
        
        self.assertEqual(new_memloadstat.exp, correct_exp)
        
    def test_redirects_to_exp_view(self):
        other_exp = Experiment.objects.create()
        correct_exp = Experiment.objects.create()
        
        response = self.client.post(
            "/memoryconsumer/exp_page/%d/add_memloadstat" % (correct_exp.id,),
            data={"mem_load_text": "1000"}
        )    
        
        self.assertRedirects(response, "/memoryconsumer/exp_page/%d/"  % (correct_exp.id,))
        
class NewUserPageTest(TestCase):
    def test_saving_a_POST_request(self):
        self.client.post(
            '/memoryconsumer/exp_page/new',
            data={"mem_load_text": "3000"}
        )
        self.assertEqual(Memloadstat.objects.count(), 1)
        new_memloadstat = Memloadstat.objects.first()
        self.assertEqual(new_memloadstat.memload, 3000)
        
    def test_redirects_after_POST(self):
        response = self.client.post(
            '/memoryconsumer/exp_page/new',
            data={"mem_load_text": "1000"}
        )
        new_exp = Experiment.objects.first()
        self.assertRedirects(response, '/memoryconsumer/exp_page/%d/' % (new_exp.id,))
        
class ExperimentAndMemloadstatModelTest(TestCase):
    def test_saving_and_retrieving_memloadstats(self):
        exp_ = Experiment()
        exp_.save()
        
        first_memloadstat = Memloadstat()
        first_memloadstat.memload = '100'
        first_memloadstat.exp = exp_
        first_memloadstat.save()
                
        second_memloadstat = Memloadstat()
        second_memloadstat.memload = "200"
        second_memloadstat.exp = exp_
        second_memloadstat.save()
        
        saved_exp = Experiment.objects.first()
        self.assertEqual(saved_exp, exp_)
        
        saved_memloadstats = Memloadstat.objects.all()
        self.assertEqual(saved_memloadstats.count(), 2)
        
        first_saved_memloadstat = saved_memloadstats[0]
        second_saved_memloadstat = saved_memloadstats[1]
        self.assertEqual(first_saved_memloadstat.memload, 100)
        self.assertEqual(first_saved_memloadstat.exp, exp_)
        self.assertEqual(second_saved_memloadstat.memload, 200)
        self.assertEqual(first_saved_memloadstat.exp, exp_)
        
        