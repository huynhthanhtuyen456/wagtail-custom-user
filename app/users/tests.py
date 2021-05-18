# from django.urls import include, path, reverse
# from rest_framework.test import APITestCase, URLPatternsTestCase
# from rest_framework.test import APIClient
# from rest_framework import status
# from rest_framework.authtoken.models import Token
# from users.models import User, UserRole, ConfirmCode
# from datetime import datetime, timedelta
#
# import pytz
#
#
#
# class JobsTests(APITestCase, URLPatternsTestCase):
#     urlpatterns = [
#         path('v1/', include('config.api')),
#     ]
#
#     def setUp(self):
#         self.data_user_role = [UserRole(name='Employer', role='employer'),
#                                UserRole(name='Talent', role='talent')]
#
#         UserRole.objects.bulk_create(self.data_user_role)
#
#         self.user_role_talent = UserRole.objects.filter(role='talent').first()
#
#         self.user_role_employer = UserRole.objects.filter(role='employer').first()
#
#         self.user = User(username="userunittest", email="userunittest@mail.com", password="123456@aA")
#
#         self.user.role = self.user_role_employer
#
#         self.user.save()
#         token = Token(user=self.user)
#         token.save()
#
#         self.client = APIClient()
#         self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(token.key))
#
#     def test_get_user_detail_200(self):
#         """
#         attach header Token
#         valid data body
#         :return:
#         status HTTP_401
#         """
#
#         self.url = reverse('me')
#         response = self.client.get(self.url, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#     def test_update_user_detail_204(self):
#         """
#         attach header Token
#         valid data body
#         :return:
#         status HTTP_401
#         """
#
#         self.url = reverse('me')
#         response = self.client.get(self.url, format='json')
#         data = {"id": response.data['user_id'],
#                 "phone_number": 12312312321,
#                 "youtube_url": "null",
#                 "cv_url": "null",
#                 "academic_document_url": "null",
#                 "profile_video_url": "null",
#                 "avatar_url": "null"}
#         self.url = reverse('update-user')
#         response = self.client.patch(self.url, data=data, format='multipart')
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#
#     def test_update_user_detail_200(self):
#         """
#         attach header Token
#         valid data body
#         :return:
#         status HTTP_401
#         """
#
#         self.url = reverse('me')
#         response = self.client.get(self.url, format='json')
#         data = {"id": response.data['user_id'],
#                 "phone_number": 12312312321,
#                 }
#         self.url = reverse('update-user')
#         response = self.client.patch(self.url, data=data, format='multipart')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#     def test_get_user_role_200(self):
#         """
#         attach header Token
#         valid data body
#         :return:
#         status HTTP_401
#         """
#
#         self.url = reverse('user-roles')
#         response = self.client.get(self.url, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#     def test_send_code_confirm_409(self):
#         """
#         attach header Token
#         valid data body
#         :return:
#         status HTTP_401
#         """
#
#         self.url = reverse('send_confirm_code')
#         data = {"email": self.user.email}
#
#         response = self.client.post(self.url, data=data, format='multipart')
#
#         print("_____________________________________ \n")
#         print(response.data)
#         print("_____________________________________ \n")
#
#         self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
#
#     def test_send_code_confirm_400(self):
#         """
#         attach header Token
#         valid data body
#         :return:
#         status HTTP_401
#         """
#
#         self.url = reverse('send_confirm_code')
#         data = {"email2": self.user.email}
#
#         response = self.client.post(self.url, data=data, format='multipart')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#
#     def test_send_code_confirm_200(self):
#         """
#         attach header Token
#         valid data body
#         :return:
#         status HTTP_401
#         """
#         self.url = reverse('send_confirm_code')
#         data = {"email": "usertest@mailniator.com"}
#         self.client.post(self.url, data=data, format='multipart')
#         response = self.client.post(self.url, data=data, format='multipart')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#     def test_compare_code_confirm_200(self):
#         """
#         attach header Token
#         valid data body
#         :return:
#         status HTTP_401
#         """
#         self.url = reverse('send_confirm_code')
#         data = {"email": "usertest@mailniator.com"}
#         self.client.post(self.url, data=data, format='multipart')
#
#         code = ConfirmCode.objects.filter(email=data['email']).first()
#
#         self.url = reverse('compare_confirm_code')
#         data_confirm = {"email": data['email'],
#                         "code": code.code}
#
#         response = self.client.post(self.url, data=data_confirm, format='multipart')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#     def test_compare_code_confirm_400(self):
#         """
#         attach header Token
#         valid data body
#         :return:
#         status HTTP_401
#         """
#         # self.url = reverse('send_confirm_code')
#         # data = {"email": "usertest@mailniator.com"}
#         # self.client.post(self.url, data=data, format='multipart')
#         #
#         # code = ConfirmCode.objects.filter(email=data['email']).first()
#
#         self.url = reverse('compare_confirm_code')
#         data_confirm = {"email2": 'email'
#                         }
#
#         response = self.client.post(self.url, data=data_confirm, format='multipart')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#
#     def test_compare_code_confirm_400_1(self):
#         """
#         attach header Token
#         valid data body
#         :return:
#         status HTTP_401
#         """
#         self.url = reverse('send_confirm_code')
#         data = {"email": "usertest@mailniator.com"}
#         self.client.post(self.url, data=data, format='multipart')
#
#         code = ConfirmCode.objects.filter(email=data['email']).first()
#
#         self.url = reverse('compare_confirm_code')
#         data_confirm = {"email": 'email',
#                         "code": code.code + '123'}
#
#         response = self.client.post(self.url, data=data_confirm, format='multipart')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#
#     def test_compare_code_confirm_400_2(self):
#         """
#         attach header Token
#         valid data body
#         :return:
#         status HTTP_401
#         """
#         self.url = reverse('send_confirm_code')
#         data = {"email": "usertest@mailniator.com"}
#         self.client.post(self.url, data=data, format='multipart')
#
#         code = ConfirmCode.objects.filter(email=data['email']).first()
#         code.expire_date = pytz.utc.localize(datetime.now() - timedelta(days=2))
#         code.save()
#         now = pytz.utc.localize(datetime.now())
#         self.url = reverse('compare_confirm_code')
#         data_confirm = {"email": data['email'],
#                         "code": code.code}
#
#         response = self.client.post(self.url, data=data_confirm, format='multipart')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
