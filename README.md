# 📦 cnpjalfanum

Biblioteca **Python** para geração, validação e formatação de **CNPJ alfanumérico**, conforme o novo padrão da Receita Federal do Brasil.  
Ideal para uso em **testes automatizados** com **Robot Framework**.

Confira a biblioteca no [PyPI](https://pypi.org/project/robotframework-cnpjalfanum/).

---

## 🚀 Instalação

Recomenda-se o uso de ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate.bat  # Windows

pip install .

```

Para instalar a biblioteca via PyPI, execute:

```bash
pip install robotframework-cnpjalfanum

```

---

## 🤖 Integração com Robot Framework

No seu arquivo `.robot`:

```robot
*** Settings ***
Library    cnpjalfanum.validator.CNPJAlfanumKeywords
```

---

## 🔑 Keywords disponíveis

| Keyword               | Descrição                                                                 |
|------------------------|---------------------------------------------------------------------------|
| `Gerar Cnpj`           | Gera um CNPJ alfanumérico válido com 14 caracteres.                       |
| `Validar Cnpj`         | Verifica se o CNPJ é válido conforme os dígitos verificadores.            |
| `Formatar Cnpj`        | Aplica a máscara `XX.XXX.XXX/XXXX-XX` ao CNPJ.                            |
| `Completar DV`         | Calcula os dois dígitos verificadores a partir dos 12 primeiros caracteres. |
| `Reconstruir Cnpj`     | Retorna o CNPJ completo (14 caracteres) a partir da base.                 |
| `É Formatado`          | Verifica se o CNPJ está no formato com máscara.                           |
| `Normalizar`           | Remove a formatação e converte para maiúsculas.                           |
| `É Valido Parcial`     | Verifica se os 12 primeiros caracteres são válidos para cálculo de DV.    |
| `Gerar Cnpj Invalido`  | Gera um CNPJ com estrutura válida, mas com DV incorreto.                  |

---

## 🧪 Exemplo de uso em Robot Framework

```robot
*** Test Cases ***
Gerar CNPJ Válido
    ${cnpj}=    Gerar Cnpj
    Log    CNPJ gerado: ${cnpj}
    Should Be Equal As Integers    ${len(${cnpj})}    14

Validar CNPJ Gerado
    ${cnpj}=    Gerar Cnpj
    ${valido}=  Validar Cnpj    ${cnpj}
    Should Be True    ${valido}

Formatar CNPJ
    ${cnpj}=    Gerar Cnpj
    ${formatado}=    Formatar Cnpj    ${cnpj}
    Log    CNPJ formatado: ${formatado}
    Should Match Regexp    ${formatado}    ^[A-Z0-9]{2}\.[A-Z0-9]{3}\.[A-Z0-9]{3}/[A-Z0-9]{4}-\d{2}$

Completar Dígito Verificador
    ${cnpj}=    Gerar Cnpj
    ${base}=    Set Variable    ${cnpj[:12]}
    ${dv}=      Completar DV    ${base}
    Log    DV calculado: ${dv}
    Should Be Equal    ${cnpj[12:]}    ${dv}

Reconstruir CNPJ
    ${cnpj}=    Gerar Cnpj
    ${base}=    Set Variable    ${cnpj[:12]}
    ${reconstruido}=    Reconstruir Cnpj    ${base}
    Should Be Equal    ${cnpj}    ${reconstruido}

Verificar Formatação
    ${cnpj}=    Gerar Cnpj
    ${formatado}=    Formatar Cnpj    ${cnpj}
    ${resultado}=    É Formatado    ${formatado}
    Should Be True    ${resultado}

Normalizar CNPJ
    ${cnpj}=    Gerar Cnpj
    ${formatado}=    Formatar Cnpj    ${cnpj}
    ${limpo}=    Normalizar    ${formatado}
    Should Be Equal    ${limpo}    ${cnpj}

Verificar Validade Parcial
    ${cnpj}=    Gerar Cnpj
    ${base}=    Set Variable    ${cnpj[:12]}
    ${parcial}=    É Valido Parcial    ${base}
    Should Be True    ${parcial}

Gerar CNPJ Inválido
    ${cnpj_invalido}=    Gerar Cnpj Invalido
    ${valido}=    Validar Cnpj    ${cnpj_invalido}
    Log    CNPJ inválido gerado: ${cnpj_invalido}
    Should Be Not True    ${valido}
```
---

🧪 Como executar os testes com Robot Framework (Windows)
Para validar o funcionamento da biblioteca e garantir que os keywords estão operando corretamente, você pode rodar os testes automatizados usando o Robot Framework. Certifique-se de estar na raiz do projeto e que o Python reconheça o pacote da biblioteca. Para isso, é necessário configurar a variável de ambiente PYTHONPATH apontando para o diretório atual.

```bash
$env:PYTHONPATH = "."
robot .\examples\example_keywords.robot
```
---

## 🔍 Diferença entre `Completar DV` e `Reconstruir Cnpj`

Ambas as keywords trabalham com os **dígitos verificadores (DV)** do CNPJ alfanumérico, mas têm propósitos distintos:

- **`Completar DV`**  
  Recebe os **12 primeiros caracteres** do CNPJ e retorna apenas os **dois dígitos verificadores** calculados.  
  🔧 Ideal para validar ou comparar DVs separadamente.

- **`Reconstruir Cnpj`**  
  Recebe os **12 primeiros caracteres** e retorna o **CNPJ completo (14 caracteres)**, já com os DVs anexados.  
  📦 Útil para gerar o CNPJ final a partir da base.

Essas funções são especialmente úteis em:
- Testes de **preenchimento parcial**  
- **Validação de campos**  
- **Reconstrução de dados** em sistemas que adotam o novo padrão alfanumérico.


## 🧠 Sobre o CNPJ Alfanumérico

A partir de **julho de 2026**, o CNPJ passará a aceitar **letras e números** nas 12 primeiras posições, aumentando a capacidade de identificação de empresas.  
Esta biblioteca já está **preparada para o novo padrão**.

---

## 🛠️ Testes unitários

Execute os testes com:

```bash
python -m unittest tests.tests_units

```

---

## 📜 Licença

**Apache 2.0** — Livre para uso, modificação e distribuição, com proteção de patentes e exigência de manter avisos de copyright e alterações.