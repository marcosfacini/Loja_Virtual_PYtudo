from rolepermissions.roles import AbstractUserRole

class Gerente(AbstractUserRole):
    available_permissions = {
        'alterar_produto': True,
        'gerenciar_usuarios': True,
    }

class Gestor(AbstractUserRole):
    available_permissions = {
    'alterar_produto': True,
    'gerenciar_usuarios': True,
    }
