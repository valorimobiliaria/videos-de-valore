# Retomada para o próximo agente

## Objetivo

Receber o link de um anúncio imobiliário, baixar e analisar fotos, gerar edições organizadas em 9:16 no Higgsfield, criar takes de passeio POV sem apresentador e montar MP4 vertical com FFmpeg. Conversar em português. Não adicionar transformação vazio→mobiliado, apresentador ou locução sem pedido.

## Produção solicitada

URL: https://valorimobiliaria.com.br/imovel/apartamento-mobiliado-de-2-4-no-jardins-neo-residence-em-frente-ao-shopping-jardins/4932

O anúncio ainda não foi acessado com sucesso. Não há fotos baixadas, ambientes selecionados, jobs enviados ou vídeo final. Características e metragem precisam ser lidas na fonte; não inferir dados do endereço da página.

## O que está implementado

- Instruções do agente: `AGENTS.md` e `skills/editor-imobiliario/SKILL.md`.
- Modelo de manifesto: `templates/manifesto.json`.
- Montagem executável: `scripts/montar_video.py`.
- Oito skills oficiais Higgsfield em `.agents/skills/`.

A montagem foi validada com dois clipes sintéticos: ordem das cenas, resolução 1080×1920, codec H.264, duração e recusa de takes não aprovados. Isso não valida edição de fotos, geração de movimento ou fidelidade visual de um imóvel real.

## Pendências

No ambiente anterior, o proxy bloqueou o domínio do anúncio com HTTP 403. Uma adição do domínio foi salva no rascunho de configuração; aplicação/publicação e acesso não foram confirmados.

O CLI Higgsfield foi instalado, mas o login não foi concluído no ambiente anterior por falta de navegador interativo. O usuário relatou conexão do plugin na interface, porém nenhuma ferramenta Higgsfield foi disponibilizada àquela sessão. Em outro agente, descobrir novamente as ferramentas e verificar acesso real; não pedir nova conexão sem conferir a existente.

Não copiar credenciais para o repositório ou para o chat. Não afirmar que assinatura, benefícios ilimitados ou créditos da API são compartilhados sem verificar a conta e as regras atuais.

## Próxima ação

Abrir o anúncio, baixar as referências e inspecioná-las; verificar o plugin ou login CLI na máquina de execução; escolher modelos e parâmetros atuais; executar o fluxo definido na skill do projeto. Criar recursos em `producoes/4932/` e registrar resultados no manifesto. Essa pasta é ignorada pelo Git e precisa de armazenamento persistente próprio.
