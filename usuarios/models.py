from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField
from cpf_field.models import CPFField
from django.utils import timezone
from datetime import date

class Usuarios(models.Model):
    ESTADOS_BRASILEIROS = (
        ('AC', 'Acre'),
        ('AL', 'Alagoas'),
        ('AP', 'Amapá'),
        ('AM', 'Amazonas'),
        ('BA', 'Bahia'),
        ('CE', 'Ceará'),
        ('DF', 'Distrito Federal'),
        ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'),
        ('MA', 'Maranhão'),
        ('MT', 'Mato Grosso'),
        ('MS', 'Mato Grosso do Sul'),
        ('MG', 'Minas Gerais'),
        ('PA', 'Pará'),
        ('PB', 'Paraíba'),
        ('PR', 'Paraná'),
        ('PE', 'Pernambuco'),
        ('PI', 'Piauí'),
        ('RJ', 'Rio de Janeiro'),
        ('RN', 'Rio Grande do Norte'),
        ('RS', 'Rio Grande do Sul'),
        ('RO', 'Rondônia'),
        ('RR', 'Roraima'),
        ('SC', 'Santa Catarina'),
        ('SP', 'São Paulo'),
        ('SE', 'Sergipe'),
        ('TO', 'Tocantins'),
    )

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nome = models.CharField(max_length=40)
    cpf = CPFField('CPF')
    data_de_nascimento = models.DateField() 
    celular = PhoneNumberField(null=False, blank=False)
    endereco = models.CharField(max_length=50)
    numero_endereco = models.CharField(max_length=10)
    complemento = models.CharField(max_length=50, blank=True, null= True)
    bairro = models.CharField(max_length=30)
    cidade = models.CharField(max_length=30)
    estado = models.CharField(max_length=2, choices=ESTADOS_BRASILEIROS)
    data_atualizacao = models.DateTimeField(auto_now=True, null=True) 


    def __str__(self):
        return str(self.usuario)
    
    def delete(self, *args, **kwargs):
        registro = RegistroAlteracaoUsuario(
            usuario=self,
            detalhes=f'Usuario {self.nome} excluído.',
        )
        registro.save()
        super().delete(*args, **kwargs)
        
    
    def save(self, *args, **kwargs):
        is_new = self._state.adding
        if not is_new:
            old_obj = Usuarios.objects.get(pk=self.pk)
            old_nome = old_obj.nome
            old_cpf = old_obj.cpf
            old_data_de_nascimento = old_obj.data_de_nascimento
            old_celular = old_obj.celular
            old_endereco = old_obj.endereco
            old_numero_endereco = old_obj.numero_endereco
            old_complemento = old_obj.complemento
            old_bairro = old_obj.bairro
            old_cidade = old_obj.cidade
            old_estado = old_obj.estado
            detalhes = f"Usuario atualizado - {self.comparar_alteracoes_usuario(old_nome, old_cpf, old_data_de_nascimento, old_celular, old_endereco, old_numero_endereco, old_complemento, old_bairro, old_cidade, old_estado)}"
        else:
            detalhes = f"Usuario {self.nome} criado"

        super().save(*args, **kwargs)
            
        registro = RegistroAlteracaoUsuario(
            usuario=self,
            detalhes=detalhes,
        )
        registro.save()

    def comparar_alteracoes_usuario(self, old_nome, old_cpf, old_data_de_nascimento, old_celular, old_endereco, old_numero_endereco, old_complemento, old_bairro, old_cidade, old_estado):
        alteracoes = []

        if old_nome != self.nome:
            alteracoes.append(f"Nome alterado de '{old_nome}' para '{self.nome}'")

        if old_cpf != self.cpf:
            alteracoes.append(f"CPF alterado de '{old_cpf}' para '{self.cpf}'")

        if old_data_de_nascimento != self.data_de_nascimento.date():
            alteracoes.append(f"Data de nascimento alterada de '{old_data_de_nascimento}' para '{self.data_de_nascimento.date()}'")

        if old_celular != self.celular:
            alteracoes.append(f"Celular alterado de '{old_celular}' para '{self.celular}'")

        if old_endereco != self.endereco:
            alteracoes.append(f"Endereço alterado de '{old_endereco}' para '{self.endereco}'")

        if old_numero_endereco != self.numero_endereco:
            alteracoes.append(f"Número de endereço alterado de '{old_numero_endereco}' para '{self.numero_endereco}'")

        if old_complemento != self.complemento:
            alteracoes.append(f"Complemento alterado de '{old_complemento}' para '{self.complemento}'")

        if old_bairro != self.bairro:
            alteracoes.append(f"Bairro alterado de '{old_bairro}' para '{self.bairro}'")

        if old_cidade != self.cidade:
            alteracoes.append(f"Cidade alterada de '{old_cidade}' para '{self.cidade}'")

        if old_estado != self.estado:
            alteracoes.append(f"Estado alterado de '{old_estado}' para '{self.estado}'")

        return ", ".join(alteracoes)
    
class RegistroAlteracaoUsuario(models.Model):
    usuario = models.ForeignKey(Usuarios, on_delete=models.SET_NULL, null=True)
    data_atualizacao = models.DateTimeField(default=timezone.now)
    detalhes = models.TextField()

    def __str__(self):
        return f"{self.usuario.nome} - {self.data_atualizacao}"


    
    

   


