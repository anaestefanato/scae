import json
from repo.inscricao_repo import obter_inscricoes_para_analise

inscricoes, total = obter_inscricoes_para_analise(pagina=1, limite=5)
print('total:', total)
if inscricoes:
    print(json.dumps(inscricoes[0], indent=2, ensure_ascii=False))
else:
    print('Nenhuma inscricao retornada')
