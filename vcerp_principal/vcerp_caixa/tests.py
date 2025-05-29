from django.contrib.auth.models import User
from django.test import TestCase

from .models import Caixa, CaixaLog


class CaixaModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="1234")
        self.caixa = Caixa.objects.create(numero="1", status="disponivel")

    def test_abrir_e_fechar_caixa(self):
        self.caixa.usuario = self.user
        self.caixa.abrir()

        self.assertEqual(self.caixa.status, "ocupado")
        self.assertIsNotNone(self.caixa.data_abertura)

        self.caixa.fechar()
        self.assertEqual(self.caixa.status, "fechado")
        self.assertIsNotNone(self.caixa.data_fechamento)

        logs = CaixaLog.objects.filter(caixa=self.caixa)
        self.assertEqual(logs.count(), 2)
