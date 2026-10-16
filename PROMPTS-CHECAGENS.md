# Prompts das checagens de jobs

Quatro checagens que a rotina faz em cada job de vídeo da pauta. Cada prompt funciona sozinho: cole no Claude com o navegador integrado logado no iClips (somente leitura). Substitua `<ID>` pelo número do job (6 dígitos). Tarefas (ids pequenos: Estudos, DAILY, reuniões) não são jobs e ficam de fora.

Como ler os dados no iClips (trechos prontos em `snippets_iclips.js`):
- Histórico: `Auditoria/Listar` (quem alterou, o quê, quando).
- Etapas: `DashTrafego/CarregaWorflowJobPeca` (nome, concluída, responsável, fim).
- Briefing e comentários: página `JobPeca/Atividade/<ID>`, aba `#Detalhe`.

---

## 1. Histórico de jobs

```
Leia o histórico do job <ID> no iClips (somente leitura) e me entregue uma linha do tempo:
1. Todos os eventos de auditoria (Auditoria/Listar): data e hora (Manaus), quem fez e o que mudou (etapa, responsável, prazo, situação, exclusão, reabertura).
2. Marque separado: trocas de responsável, mudanças de prazo (de/para e quem mudou), reaberturas de etapa e exclusões de peça.
3. Em quais etapas o job passou por EDIÇÃO e por quem (use a lista de sessões da AtividadeRealizadaFuncionario se precisar confirmar autoria).
4. Contagem de refações/ajustes: quantas vezes voltou da APROVAÇÃO para EDIÇÃO ou entrou em AJUSTE (CLIENTE ou INTERNO).
Não deduza autoria de login compartilhado: se o login for compartilhado, escreva "login compartilhado" e só atribua a alguém se a Diana tiver confirmado. Não invente: se um dado não aparece, diga que não aparece.
```

## 2. Cruzamento briefing × ajustes e flag de +2 ajustes

```
Abra o job <ID> (https://app.iclips.com.br/vanguarda/JobPeca/Atividade/<ID>, espere ~5,5 s) e leia #Detalhe: Briefing e Comentários.
1. Liste cada ajuste pedido (quem pediu, quando, o que pediu), do mais antigo ao mais novo.
2. Para cada ajuste, cruze com o briefing e classifique em um tipo só:
   - Erro de edição (o briefing já pedia aquilo e não foi feito);
   - Briefing sem as informações (o briefing não trazia o dado: texto, referência, formato, música, logo etc.);
   - Alteração do cliente (o cliente mudou o que tinha aprovado ou pedido);
   - Outros (explique em uma frase).
3. Diga em uma frase o motivo de cada classificação, citando o trecho do briefing ou do comentário.
4. Conte os ajustes. Se forem MAIS DE 2, marque em vermelho "+2 ajustes" e escreva uma frase com a causa dominante (ex.: "3 de 4 por briefing sem as informações").
Resultado: quadro com data, quem pediu, o que pediu, tipo, e a contagem final com a flag.
```

## 3. Deadline × histórico

```
Para o job <ID>, confira se o prazo atual está de acordo com o histórico.
1. Prazo atual de cada etapa em aberto (CarregaWorflowJobPeca) e o prazo do job na lista.
2. No histórico (Auditoria/Listar), ache cada mudança de prazo: de quê, para quê, quem mudou, quando.
3. Cruze com o briefing e os comentários: houve combinado de entrega com o cliente ou atendimento que justifique o prazo? Algum pedido de "urgente", "para hoje" ou "para amanhã" no WhatsApp/Chat sem reflexo no prazo do iClips?
4. Aponte as divergências: prazo vencido; prazo mudado sem motivo visível; prazo da edição depois do prazo da aprovação; prazo diferente do que foi combinado; etapa sem prazo.
5. Conclusão em uma linha: "OK", "divergente" (com o que corrigir e quem avisar) ou "sem dados para afirmar".
Só leitura: não altere prazo nem escreva no job.
```

## 4. Etapas bloqueantes

```
Para o job <ID>, leia o fluxo (CarregaWorflowJobPeca) e diga o que bloqueia a EDIÇÃO.
1. Liste as etapas em ordem com: nome, concluída ou não, responsável (vazio ou TRÁFEGO = etapa do Tráfego), prazo.
2. Etapas anteriores à edição que ainda não foram concluídas (ARTE, TEXTO, CARTELAS, APROVAÇÃO, material do cliente) são bloqueantes. Etapas posteriores (APROVAÇÃO INTERNA, ARQUIVAMENTO, ENCERRAMENTO) não bloqueiam.
3. Para cada bloqueio: etapa, responsável, prazo, e se o prazo dela é depois do prazo da edição. Cheque o briefing e os comentários por material faltando (locução, áudio, vídeo bruto, logo, texto) mesmo quando todas as etapas anteriores estão concluídas.
4. Conclusão: "Livre para editar" ou "Bloqueado por <etapa/responsável>", e quem precisa agir.
Não conte como bloqueio uma etapa só porque está em aberto depois da edição.
```
