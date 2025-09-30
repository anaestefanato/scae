"""
Utilitários para formatação de datas
"""
from datetime import datetime, timedelta
import locale

def calcular_tempo_relativo(data_str: str) -> str:
    """
    Calcula o tempo relativo baseado na data fornecida
    
    Args:
        data_str: Data no formato ISO ou similar
    
    Returns:
        String formatada com tempo relativo (ex: "há 2 horas", "há 1 dia")
    """
    if not data_str:
        return "Data não informada"
    
    try:
        # Converter string para datetime
        if isinstance(data_str, str):
            # Lidar com diferentes formatos de data
            if 'T' in data_str:
                data = datetime.fromisoformat(data_str.replace('Z', '+00:00'))
            else:
                data = datetime.strptime(data_str, '%Y-%m-%d %H:%M:%S')
        else:
            data = data_str
            
        agora = datetime.now()
        diferenca = agora - data
        
        # Calcular tempo relativo
        if diferenca.days > 0:
            if diferenca.days == 1:
                return "há 1 dia"
            elif diferenca.days < 7:
                return f"há {diferenca.days} dias"
            elif diferenca.days < 30:
                semanas = diferenca.days // 7
                if semanas == 1:
                    return "há 1 semana"
                else:
                    return f"há {semanas} semanas"
            else:
                meses = diferenca.days // 30
                if meses == 1:
                    return "há 1 mês"
                else:
                    return f"há {meses} meses"
        else:
            # Menos de um dia
            horas = diferenca.seconds // 3600
            minutos = (diferenca.seconds % 3600) // 60
            
            if horas > 0:
                if horas == 1:
                    return "há 1 hora"
                else:
                    return f"há {horas} horas"
            elif minutos > 0:
                if minutos == 1:
                    return "há 1 minuto"
                else:
                    return f"há {minutos} minutos"
            else:
                return "agora mesmo"
                
    except Exception as e:
        print(f"Erro ao calcular tempo relativo: {e}")
        return "Data inválida"

def formatar_data_brasileira(data_str: str) -> str:
    """
    Formata data no padrão brasileiro (DD/MM/YYYY)
    
    Args:
        data_str: Data no formato ISO ou similar
    
    Returns:
        String formatada no padrão brasileiro
    """
    if not data_str:
        return "Data não informada"
    
    try:
        if isinstance(data_str, str):
            if 'T' in data_str:
                data = datetime.fromisoformat(data_str.replace('Z', '+00:00'))
            else:
                data = datetime.strptime(data_str, '%Y-%m-%d %H:%M:%S')
        else:
            data = data_str
            
        return data.strftime('%d/%m/%Y às %H:%M')
        
    except Exception as e:
        print(f"Erro ao formatar data: {e}")
        return "Data inválida"