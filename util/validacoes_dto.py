import re
from typing import Optional
from decimal import Decimal

from util.exceptions import ValidacaoError

def validar_texto_obrigatorio(
    texto: str,
    campo: str = "Campo",
    min_chars: int = 1,
    max_chars: int = 255
) -> str:
    """
    Valida texto obrigatório com limites de tamanho

    Args:
        texto: Texto a ser validado
        campo: Nome do campo (para mensagens de erro)
        min_chars: Tamanho mínimo
        max_chars: Tamanho máximo

    Returns:
        Texto validado e limpo

    Raises:
        ValidacaoError: Se validação falhar
    """
    if not texto or not texto.strip():
        raise ValidacaoError(f'{campo} é obrigatório')

    texto_limpo = texto.strip()

    if len(texto_limpo) < min_chars:
        raise ValidacaoError(f'{campo} deve ter pelo menos {min_chars} caracteres')

    if len(texto_limpo) > max_chars:
        raise ValidacaoError(f'{campo} deve ter no máximo {max_chars} caracteres')

    return texto_limpo


def validar_texto_opcional(
    texto: Optional[str],
    max_chars: int = 500
) -> Optional[str]:
    """
    Valida texto opcional

    Args:
        texto: Texto a ser validado (pode ser None)
        max_chars: Tamanho máximo

    Returns:
        Texto validado ou None

    Raises:
        ValidacaoError: Se texto exceder tamanho máximo
    """
    if not texto or not texto.strip():
        return None

    texto_limpo = texto.strip()

    if len(texto_limpo) > max_chars:
        raise ValidacaoError(f'Texto deve ter no máximo {max_chars} caracteres')

    return texto_limpo


def validar_cpf(cpf: Optional[str]) -> Optional[str]:
    """
    Valida CPF brasileiro com dígitos verificadores

    Args:
        cpf: CPF a ser validado (pode conter máscaras)

    Returns:
        CPF limpo (apenas números) ou None se vazio

    Raises:
        ValidacaoError: Se CPF for inválido
    """
    if not cpf:
        return None

    # Remover caracteres especiais
    cpf_limpo = re.sub(r'[^0-9]', '', cpf)

    if len(cpf_limpo) != 11:
        raise ValidacaoError('CPF deve ter 11 dígitos')

    # Verificar se todos os dígitos são iguais
    if cpf_limpo == cpf_limpo[0] * 11:
        raise ValidacaoError('CPF inválido')

    # Validar dígito verificador
    def calcular_digito(cpf_parcial):
        soma = sum(int(cpf_parcial[i]) * (len(cpf_parcial) + 1 - i)
                   for i in range(len(cpf_parcial)))
        resto = soma % 11
        return 0 if resto < 2 else 11 - resto

    if int(cpf_limpo[9]) != calcular_digito(cpf_limpo[:9]):
        raise ValidacaoError('CPF inválido')

    if int(cpf_limpo[10]) != calcular_digito(cpf_limpo[:10]):
        raise ValidacaoError('CPF inválido')

    return cpf_limpo


def validar_telefone(telefone: str) -> Optional[str]:
    """
    Valida telefone brasileiro (celular ou fixo)

    Args:
        telefone: Telefone a ser validado

    Returns:
        Telefone limpo (apenas números)

    Raises:
        ValidacaoError: Se telefone for inválido
    """
    if not telefone:
        raise ValidacaoError('Telefone é obrigatório')

    # Remover caracteres especiais
    telefone_limpo = re.sub(r'[^0-9]', '', telefone)

    # Telefone deve ter 10 (fixo) ou 11 (celular) dígitos
    if len(telefone_limpo) not in [10, 11]:
        return None

    # Validar DDD (11 a 99)
    ddd = int(telefone_limpo[:2])
    if ddd < 11 or ddd > 99:
        return None

    return telefone_limpo


def validar_valor_monetario(
    valor: Optional[Decimal],
    campo: str = "Valor",
    obrigatorio: bool = True,
    min_valor: Optional[Decimal] = None
) -> Optional[Decimal]:
    """
    Valida valor monetário

    Args:
        valor: Valor a ser validado
        campo: Nome do campo
        obrigatorio: Se o valor é obrigatório
        min_valor: Valor mínimo permitido

    Returns:
        Valor validado

    Raises:
        ValidacaoError: Se validação falhar
    """
    if valor is None:
        if obrigatorio:
            raise ValidacaoError(f'{campo} é obrigatório')
        return None

    if not isinstance(valor, Decimal):
        try:
            valor = Decimal(str(valor))
        except:
            raise ValidacaoError(f'{campo} deve ser um valor numérico válido')

    if min_valor is not None and valor < min_valor:
        raise ValidacaoError(f'{campo} deve ser maior ou igual a {min_valor}')

    return valor


def validar_enum_valor(valor: any, enum_class, campo: str = "Campo"):
    """
    Valida se valor está em um enum

    Args:
        valor: Valor a ser validado
        enum_class: Classe do enum
        campo: Nome do campo

    Returns:
        Valor do enum validado

    Raises:
        ValidacaoError: Se valor não estiver no enum
    """
    if isinstance(valor, str):
        try:
            return enum_class(valor.upper())
        except ValueError:
            valores_validos = [item.value for item in enum_class]
            raise ValidacaoError(
                f'{campo} deve ser uma das opções: {", ".join(valores_validos)}'
            )

    if valor not in enum_class:
        valores_validos = [item.value for item in enum_class]
        raise ValidacaoError(
            f'{campo} deve ser uma das opções: {", ".join(valores_validos)}'
        )

    return valor

class ValidadorWrapper:
    """
    Classe para facilitar o uso de validadores em field_validators.
    Reduz código repetitivo e padroniza tratamento de erros.
    """

    @staticmethod
    def criar_validador(funcao_validacao, campo_nome: str = None, **kwargs):
        """
        Cria um validador pronto para usar com @field_validator.

        Args:
            funcao_validacao: Função de validação a ser chamada
            campo_nome: Nome do campo para mensagens de erro
            **kwargs: Argumentos adicionais para a função

        Returns:
            Função validador pronta para usar

        Exemplo:
            validar_nome = ValidadorWrapper.criar_validador(
                validar_texto_obrigatorio, "Nome", min_chars=2, max_chars=100
            )
        """
        def validador(valor):
            try:
                if campo_nome:
                    return funcao_validacao(valor, campo_nome, **kwargs)
                else:
                    return funcao_validacao(valor, **kwargs)
            except ValidacaoError as e:
                raise ValueError(str(e))
        return validador