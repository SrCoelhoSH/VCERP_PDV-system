import logging
from django.test import TestCase
from django.contrib.auth.models import User
from .models import PessoaFisica, PessoaJuridica, Produto
from datetime import date

# Configuração básica do logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PessoaFisicaTestCase(TestCase):
    def setUp(self):
        logger.info("Configurando teste para PessoaFisica")
        self.pessoa_fisica = PessoaFisica.objects.create(
            nome="João Silva",
            cpf="12345678901",
            email="joao@example.com",
            telefone="123456789",
            rua="Rua Exemplo",
            cep="12345678",
            ponto_referencia="Perto do mercado",
            penalizado=False
        )

    def test_pessoa_fisica_creation(self):
        try:
            pessoa = PessoaFisica.objects.get(cpf="12345678901")
            self.assertEqual(pessoa.nome, "João Silva")
            self.assertEqual(pessoa.email, "joao@example.com")
            self.assertFalse(pessoa.penalizado)
            logger.info("Teste de criação de PessoaFisica passou.")
        except Exception as e:
            logger.error(f"Teste de criação de PessoaFisica falhou: {e}")
            raise e


class PessoaJuridicaTestCase(TestCase):
    def setUp(self):
        logger.info("Configurando teste para PessoaJuridica")
        self.pessoa_juridica = PessoaJuridica.objects.create(
            razao_social="Empresa XYZ",
            cnpj="12345678000195",
            email="empresa@example.com",
            telefone="987654321",
            rua="Avenida Exemplo",
            cep="87654321",
            ponto_referencia="Ao lado do shopping",
            penalizado=False
        )

    def test_pessoa_juridica_creation(self):
        try:
            empresa = PessoaJuridica.objects.get(cnpj="12345678000195")
            self.assertEqual(empresa.razao_social, "Empresa XYZ")
            self.assertEqual(empresa.email, "empresa@example.com")
            self.assertFalse(empresa.penalizado)
            logger.info("Teste de criação de PessoaJuridica passou.")
        except Exception as e:
            logger.error(f"Teste de criação de PessoaJuridica falhou: {e}")
            raise e


class ProdutoTestCase(TestCase):
    def setUp(self):
        logger.info("Configurando teste para Produto")
        self.produto = Produto.objects.create(
            nome="Celular",
            tipo="eletronico",
            descricao="Smartphone de última geração",
            codigo_barra="1234567890123",
            data_cadastro=date.today(),
            quantidade=10
        )

    def test_produto_creation(self):
        try:
            produto = Produto.objects.get(nome="Celular")
            self.assertEqual(produto.tipo, "eletronico")
            self.assertEqual(produto.quantidade, 10)
            logger.info("Teste de criação de Produto passou.")
        except Exception as e:
            logger.error(f"Teste de criação de Produto falhou: {e}")
            raise e


# class ProfileTestCase(TestCase):
#     def setUp(self):
#         logger.info("Configurando teste para Profile")
#         self.user = User.objects.create_user(username="usuario_teste", password="12345")
#         self.profile = Profile.objects.create(
#             user=self.user,
#             profile_image="path/to/image.jpg"
#         )

#     def test_profile_creation(self):
#         try:
#             profile = Profile.objects.get(user=self.user)
#             self.assertEqual(profile.user.username, "usuario_teste")
#             self.assertEqual(profile.profile_image, "path/to/image.jpg")
#             logger.info("Teste de criação de Profile passou.")
#         except Exception as e:
#             logger.error(f"Teste de criação de Profile falhou: {e}")
#             raise e
