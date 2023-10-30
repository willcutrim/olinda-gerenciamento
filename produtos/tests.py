from django.test import TestCase
from .models import Produto, Fornecedor

class FornecedorTestCase(TestCase):
    
    def set_character(self, email):
        if '@' in email and '.com' in email:
            return True
        else:
            return False

    def teste_validation_email_fornecedor(self):
        fornecedor = Fornecedor.objects.create(nome_fornecedor='Casos Bahio', contato=99991919906, email='willyam894@gmail.com')
        false_or_true = self.set_character(fornecedor.email)

        self.assertEqual(false_or_true, True)
        
        