#para criar uma classe das oções de serviços a serem executados, usando o Textchoices do django
from django.db.models import TextChoices

class ChoicesCategoriaManutencao(TextChoices):
    TROCAR_VALVULA_MOTOR = "TVM", "Trocar valvula do motor"
    TROCAR_OLEO = "TO", "Troca de oleo"
    BALANCEAMENTO = "BL", "Balanceamento"