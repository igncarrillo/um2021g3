import json
from unittest.mock import MagicMock
from unittest.mock import patch

from django.test import TestCase, RequestFactory
from rest_framework import status

from .models import Usuario, Publicacion
from .views import UserController, LoginController, PublicacionDetalleController


class UserControllerTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user_data_valid = {
            "nombre_usuario": "test_user",
            "contraseña": "test_password",
            "nombre": "test name",
            "apellido": "test last name",
        }
        self.user_data_invalid = {
            "nombre_usuario": "test_user",
            "email": "invalid_email",
            "contraseña": "test_password"
        }

    def test_post_invalid_data(self):
        request = self.factory.post('/some-url/', data=self.user_data_invalid, content_type='application/json')
        controller = UserController()
        response = controller.post(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_valid_data(self):
        request = self.factory.post('/some-url/', data=self.user_data_valid, content_type='application/json')
        controller = UserController()
        response = controller.post(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class LoginControllerTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_post_login_successful(self):
        data = {
            'nombre_usuario': 'usuario_prueba',
            'contraseña': 'contraseña_prueba'
        }
        request = self.factory.post('/some-url/', data=json.dumps(data), content_type='application/json')

        usuario_mock = MagicMock(spec=Usuario)
        usuario_mock.login.return_value = True

        with patch('twitter.views.Usuario.objects.filter') as filter_mock:
            filter_mock.return_value.first.return_value = usuario_mock

            controller = LoginController()
            response = controller.post(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, b'{"msg": "Login successful"}')

    def test_post_incorrect_credentials(self):
        data = {
            'nombre_usuario': 'usuario_prueba',
            'contraseña': 'contraseña_incorrecta'
        }
        request = self.factory.post('/some-url/', data=json.dumps(data), content_type='application/json')

        usuario_mock = MagicMock(spec=Usuario)
        usuario_mock.login.return_value = False

        with patch('twitter.views.Usuario.objects.filter') as filter_mock:
            filter_mock.return_value.first.return_value = usuario_mock

            controller = LoginController()
            response = controller.post(request)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.content, b'{"msg": "Incorrect credentials"}')


class PublicacionControllerTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @patch('twitter.views.Publicacion.objects.get')
    def test_delete_publicacion_exitosa(self, mock_get):
        mock_publicacion = mock_get.return_value
        mock_publicacion.delete.return_value = None

        request = self.factory.delete('/some-url/1/')
        controller = PublicacionDetalleController()
        response = controller.delete(request, id=1)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, b'{"message": "Publicacion eliminada exitosamente."}')

    @patch('twitter.views.Publicacion.objects.get')
    def test_delete_publicacion_inexistente(self, mock_get):
        mock_get.side_effect = Publicacion.DoesNotExist()

        request = self.factory.delete('/some-url/1/')
        controller = PublicacionDetalleController()
        response = controller.delete(request, id=1)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.content, b'{"Error": "No existe ninguna publicacion"}')
