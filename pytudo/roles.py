from rolepermissions.roles import AbstractUserRole

class Gerente(AbstractUserRole):
    available_permissions = {
        'cadastrar_produto': True,
        'atualizar_cadastro': False,
    }

class Cliente(AbstractUserRole):
    available_permissions = {
        'atualizar_cadastro': True,
    }

class Gestor(AbstractUserRole):
    available_permissions = {
    'cadastrar_produto': True,
    'atualizar_cadastro': True,
    'criar_gerente': True,
    }
