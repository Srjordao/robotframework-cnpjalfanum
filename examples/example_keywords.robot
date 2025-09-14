*** Settings ***
Library    cnpjalfanum.validator.CNPJAlfanumKeywords



*** Test Cases ***

Gerar CNPJ Válido
    [Documentation]     Gera um CNPJ alfanumérico válido e verifica se possui 14 caracteres.
    ${cnpj}=    Gerar Cnpj
    Log    CNPJ gerado: ${cnpj}
    Length Should Be    ${cnpj}    14

Validar CNPJ Gerado
    [Documentation]     Gera um CNPJ e valida se os dígitos verificadores estão corretos.
    ${cnpj}=    Gerar Cnpj
    ${valido}=  Validar Cnpj    ${cnpj}
    Should Be True    ${valido}

Formatar CNPJ
    [Documentation]     Gera um CNPJ e aplica a máscara padrão, verificando o formato e o comprimento.
    ${cnpj}=    Gerar Cnpj
    ${formatado}=    Formatar Cnpj    ${cnpj}
    Log    CNPJ formatado: ${formatado}
    Should Match Regexp    ${formatado}    ^[A-Z0-9]{2}\.[A-Z0-9]{3}\.[A-Z0-9]{3}/[A-Z0-9]{4}-[A-Z0-9]{2}$
    Length Should Be    ${formatado}    18

Completar Dígito Verificador
    [Documentation]     Gera um CNPJ, extrai os 12 primeiros caracteres e calcula os dígitos verificadores.
    ${cnpj}=    Gerar Cnpj
    ${base}=    Set Variable    ${cnpj[:12]}
    ${dv}=      Completar DV    ${base}
    Log    DV calculado: ${dv}
    Should Be Equal    ${cnpj[12:]}    ${dv}

Reconstruir CNPJ
    [Documentation]     Gera um CNPJ, extrai a base e reconstrói o CNPJ completo com os dígitos verificadores.
    ${cnpj}=    Gerar Cnpj
    ${base}=    Set Variable    ${cnpj[:12]}
    ${reconstruido}=    Reconstruir Cnpj    ${base}
    Should Be Equal    ${cnpj}    ${reconstruido}

Verificar Formatação
    [Documentation]     Verifica se o CNPJ formatado está no padrão esperado com máscara.
    ${cnpj}=    Gerar Cnpj
    ${formatado}=    Formatar Cnpj    ${cnpj}
    ${resultado}=    É Formatado    ${formatado}
    Should Be True    ${resultado}

Normalizar CNPJ
    [Documentation]     Remove a formatação do CNPJ e verifica se o valor corresponde ao original.
    ${cnpj}=    Gerar Cnpj
    ${formatado}=    Formatar Cnpj    ${cnpj}
    ${limpo}=    Normalizar    ${formatado}
    Should Be Equal    ${limpo}    ${cnpj}

Verificar Validade Parcial
    [Documentation]     Verifica se os 12 primeiros caracteres de um CNPJ são válidos para cálculo de DV.
    ${cnpj}=    Gerar Cnpj
    ${base}=    Set Variable    ${cnpj[:12]}
    ${parcial}=    É Valido Parcial    ${base}
    Should Be True    ${parcial}

Gerar CNPJ Inválido
    [Documentation]     Gera um CNPJ com dígitos verificadores incorretos e valida que ele é rejeitado.
    ${cnpj_invalido}=    Gerar Cnpj Invalido
    ${valido}=    Validar Cnpj    ${cnpj_invalido}
    Log    CNPJ inválido gerado: ${cnpj_invalido}
    Should Not Be True    ${valido}