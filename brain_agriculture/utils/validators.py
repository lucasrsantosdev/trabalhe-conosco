import re
from pydantic import ValidationError

def validate_cpf_cnpj(value: str) -> str:
    # Remove tudo que não for número
    value = re.sub(r'\D', '', value)

    # Verifica se tem 11 dígitos (CPF) ou 14 dígitos (CNPJ)
    if len(value) == 11 and value.isdigit():
        return value  # CPF válido
    elif len(value) == 14 and value.isdigit():
        return value  # CNPJ válido

    # Se não for nenhum dos dois, lança erro
    raise ValidationError(f"Documento inválido: {value}")
