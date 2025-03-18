from rolepermissions.roles import AbstractUserRole

class PROFESSOR(AbstractUserRole):
    available_permissions = {}
    
class ALUNO(AbstractUserRole):
    available_permissions = {}