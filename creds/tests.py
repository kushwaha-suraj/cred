from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from creds.models import Creds

# Create your tests here.

class CredsAPITestCase(APITestCase):
    def create_creds(self):
        sample_cred={'title':'title','desc':'description test'}
        response=self.client.post(reverse("creds"), sample_cred)
        return response
        
    
    def authenticate(self):
        self.client.post(reverse("register"),{'username':'username','email':'abc@gmail.com','password':'password@123'})
        response =self.client.post(reverse("login"),{'email':'abc@gmail.com','password':'password@123'})
        self.client.credentials(HTTP_AUTHORIZATION=f"Authorization {response.data['token']}")

class TestListCreateCreds(CredsAPITestCase):
    
    def test_should_not_creates_creds_with_no_auth(self):
        response =self.create_creds()
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
    
    def test_should_creates_creds(self):
        previous_creds_count = Creds.objects.all().count()
        self.authenticate()
        response =self.create_creds()
        self.assertEqual(Creds.objects.all().count(),previous_creds_count+1)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'],'title')
        self.assertEqual(response.data['desc'],'description test')
        
    def test_retrives_all_creds(self):
        self.authenticate()
        response=self.client.get(reverse("creds"))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertIsInstance(response.data['results'],list)
        response =self.create_creds()
        res=self.client.get(reverse("creds"))
        self.assertIsInstance(res.data['count'],int)
        self.assertEqual(res.data['count'],1)
        
class TestCredsDetailAPIView(CredsAPITestCase):
    
    def test_retrives_one_item(self):
        self.authenticate()
        response = self.create_creds()
        
        res=self.client.get(reverse("creds",kwargs={'id':response.data['id']}))

        self.assertEqual(res.status_code,status.HTTP_200_OK)
        
        creds=Creds.objects.get(id=response.data['id'])
        
        self.assertEqual(creds.title, res.data['title'])
    
    def test_updates_one_item(self):
        self.authenticate()
        response = self.create_creds()
        
        res= self.client.patch(reverse("creds",kwargs={'id':response.data['id']}),{"title":"New One","is_complete":True})
        self.assertEqual(res.status_code,status.HTTP_200_OK)
        updated_creds = Creds.objects.get(id=response.data['id'])
        self.assertEqual(updated_creds.is_complete, True)
        self.assertEqual(updated_creds.title,"New One")
        
    def test_deletes_one_item(self):
        self.authenticate()
        res= self.create_creds()
        
        prev_db_count=Creds.objects.all().count()
        
        self.assertGreater(prev_db_count, 0)
        self.assertEqual(prev_db_count, 1)
        
        response = self.client.delete(reverse("creds",kwargs={'id':res.data['id']}))
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)
        
        self.assertEqual(Creds.objects.all().count(),0)