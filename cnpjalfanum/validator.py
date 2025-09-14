import random
import string
import re

# ==========================
# CONSTANTES
# ==========================

CHAR_MAP = {
    **{str(i): i for i in range(10)},  # 0–9 → 0–9
    **{chr(i): i - 48 for i in range(65, 91)}  # A–Z → 17–42
}

# ==========================
# FORMATADOR
# ==========================

def remover_formatacao(cnpj):
    return ''.join(filter(str.isalnum, cnpj.upper()))

def formatar_cnpj(cnpj):
    cnpj = remover_formatacao(cnpj)
    return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"

def é_formatado(cnpj):
    return bool(re.match(r'^[A-Z0-9]{2}\.[A-Z0-9]{3}\.[A-Z0-9]{3}/[A-Z0-9]{4}-\d{2}$', cnpj))

def normalizar(cnpj):
    return remover_formatacao(cnpj)

# ==========================
# VALIDADOR
# ==========================

def calcular_dv(cnpj12):
    def soma_pesos(valores, pesos):
        return sum(v * p for v, p in zip(valores, pesos))

    def valores_para_dv(cnpj):
        return [CHAR_MAP[c] for c in cnpj]

    def gerar_dv(cnpj):
        valores = valores_para_dv(cnpj)
        pesos = list(range(2, 10)) * ((len(valores) // 8) + 1)
        pesos = pesos[:len(valores)][::-1]
        soma = soma_pesos(valores, pesos)
        resto = soma % 11
        return str(0 if resto < 2 else 11 - resto)

    dv1 = gerar_dv(cnpj12)
    dv2 = gerar_dv(cnpj12 + dv1)
    return dv1 + dv2

def validar_cnpj(cnpj):
    cnpj = remover_formatacao(cnpj)
    base, dv = cnpj[:12], cnpj[12:]
    return calcular_dv(base) == dv

def é_valido_parcial(cnpj):
    cnpj = remover_formatacao(cnpj)
    return len(cnpj) >= 12 and all(c in CHAR_MAP for c in cnpj[:12])

# ==========================
# GERADOR
# ==========================

def gerar_cnpj_alfanum():
    base = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
    dv = calcular_dv(base)
    return base + dv

def completar_dv(cnpj_sem_dv):
    cnpj_sem_dv = remover_formatacao(cnpj_sem_dv)
    if len(cnpj_sem_dv) != 12:
        raise ValueError("CNPJ base deve ter 12 caracteres")
    return calcular_dv(cnpj_sem_dv)

def reconstruir_cnpj(cnpj_sem_dv):
    return cnpj_sem_dv + completar_dv(cnpj_sem_dv)

def gerar_cnpj_invalido():
    base = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
    dv_real = calcular_dv(base)

    # Gera um DV incorreto diferente do real
    while True:
        dv_falso = ''.join(random.choices(string.digits, k=2))
        if dv_falso != dv_real:
            break

    return base + dv_falso

# ==========================
# KEYWORDS PARA ROBOT FRAMEWORK
# ==========================

class CNPJAlfanumKeywords:
    def gerar_cnpj(self):
        return gerar_cnpj_alfanum()

    def validar_cnpj(self, cnpj):
        return validar_cnpj(cnpj)

    def formatar_cnpj(self, cnpj):
        return formatar_cnpj(cnpj)

    def completar_dv(self, cnpj_sem_dv):
        return completar_dv(cnpj_sem_dv)

    def reconstruir_cnpj(self, cnpj_sem_dv):
        return reconstruir_cnpj(cnpj_sem_dv)

    def é_formatado(self, cnpj):
        return é_formatado(cnpj)

    def normalizar(self, cnpj):
        return normalizar(cnpj)

    def é_valido_parcial(self, cnpj):
        return é_valido_parcial(cnpj)
    
    def gerar_cnpj_invalido(self):
        return gerar_cnpj_invalido()

# ==========================
# MODO DE USO MANUAL
# ==========================

if __name__ == "__main__":
    print("🔧 Gerando CNPJ alfanumérico...")
    cnpj = gerar_cnpj_alfanum()
    print(f"CNPJ gerado: {cnpj}")

    formatado = formatar_cnpj(cnpj)
    print(f"CNPJ formatado: {formatado}")

    print(f"É válido? {'✅ Sim' if validar_cnpj(cnpj) else '❌ Não'}")

    print("🔍 Reconstruindo a partir da base...")
    base = cnpj[:12]
    print(f"Base: {base}")
    print(f"DV calculado: {completar_dv(base)}")
    print(f"CNPJ reconstruído: {reconstruir_cnpj(base)}")

    print("\n🧪 Executando testes unitários...\n")