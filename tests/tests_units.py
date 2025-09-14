import unittest

from cnpjalfanum.validator import (
    gerar_cnpj_alfanum,
    validar_cnpj,
    formatar_cnpj,
    completar_dv,
    reconstruir_cnpj,
    é_formatado,
    normalizar,
    é_valido_parcial,
    gerar_cnpj_invalido,
    calcular_dv
)


# ==========================
# TESTES UNITÁRIOS
# ==========================


class TestCNPJAlfanumerico(unittest.TestCase):
    def test_geracao_valida(self):
        cnpj = gerar_cnpj_alfanum()
        self.assertTrue(validar_cnpj(cnpj))

    def test_formatacao(self):
        cnpj = gerar_cnpj_alfanum()
        formatado = formatar_cnpj(cnpj)
        self.assertEqual(len(formatado), 18)
        self.assertTrue(validar_cnpj(formatado))

    def test_validacao_falsa(self):
        cnpj = gerar_cnpj_alfanum()
        base = cnpj[:12]
        dv_real = calcular_dv(base)
        
        # Gera um DV falso diferente do real
        dv_falso = "00" if dv_real != "00" else "ZZ"
        cnpj_falso = base + dv_falso
        
        self.assertFalse(validar_cnpj(cnpj_falso))


    def test_completar_dv(self):
        cnpj = gerar_cnpj_alfanum()
        base = cnpj[:12]
        dv = completar_dv(base)
        self.assertEqual(cnpj[12:], dv)

    def test_reconstruir_cnpj(self):
        cnpj = gerar_cnpj_alfanum()
        base = cnpj[:12]
        reconstruido = reconstruir_cnpj(base)
        self.assertEqual(cnpj, reconstruido)

    def test_formatado(self):
        cnpj = gerar_cnpj_alfanum()
        formatado = formatar_cnpj(cnpj)
        self.assertTrue(é_formatado(formatado))

    def test_normalizar(self):
        cnpj = gerar_cnpj_alfanum()
        formatado = formatar_cnpj(cnpj)
        self.assertEqual(normalizar(formatado), cnpj)

    def test_valido_parcial(self):
        cnpj = gerar_cnpj_alfanum()
        self.assertTrue(é_valido_parcial(cnpj[:12]))

    def test_geracao_invalida(self):
        cnpj_invalido = gerar_cnpj_invalido()
        self.assertFalse(validar_cnpj(cnpj_invalido))
