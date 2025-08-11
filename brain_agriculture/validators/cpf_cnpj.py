# brain_agriculture/validators/cpf_cnpj.py
import re

def validate_cpf_cnpj(value: str) -> bool:
    digits = re.sub(r"\D", "", value or "")
    if len(digits) == 11:
        return validate_cpf(digits)
    if len(digits) == 14:
        return validate_cnpj(digits)
    return False

def validate_cpf(cpf: str) -> bool:
    if not cpf or cpf == cpf[0] * 11:
        return False
    s = sum(int(cpf[i]) * (10 - i) for i in range(9))
    d1 = (s * 10) % 11
    d1 = 0 if d1 == 10 else d1
    if d1 != int(cpf[9]):
        return False
    s = sum(int(cpf[i]) * (11 - i) for i in range(10))
    d2 = (s * 10) % 11
    d2 = 0 if d2 == 10 else d2
    return d2 == int(cpf[10])

def validate_cnpj(cnpj: str) -> bool:
    if not cnpj or cnpj == cnpj[0] * 14:
        return False

    def calc_digit(nums, weights):
        s = sum(int(n) * w for n, w in zip(nums, weights))
        r = s % 11
        return '0' if r < 2 else str(11 - r)

    d1 = calc_digit(cnpj[:12], [5,4,3,2,9,8,7,6,5,4,3,2])
    d2 = calc_digit(cnpj[:12] + d1, [6,5,4,3,2,9,8,7,6,5,4,3,2])
    return cnpj[-2:] == d1 + d2
