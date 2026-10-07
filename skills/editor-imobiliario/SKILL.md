---
name: editor-imobiliario
description: Produzir vídeos imobiliários verticais a partir de anúncios, com organização visual das fotos, geração de takes e montagem FFmpeg.
---

# Editor imobiliário

## Contrato de produção

Receba o link, leia o anúncio e conduza a produção em português. Formato final: MP4 vertical 9:16. Não peça novamente informações presentes no anúncio. O usuário confirmou Higgsfield e passeio de câmera sem apresentador. Use esse padrão; o acesso às ferramentas ainda precisa ser verificado. Descubra ferramentas, documentação, upload, modelos, duração, proporção, áudio e consulta de jobs atuais. Não invente endpoints ou identifique uma API inexistente como funcional.

POV admite dois modos: `passeio` (câmera em primeira pessoa, sem apresentador ou voz) e `apresentador` (pessoa falando). Quando o pedido mencionar fala, confirme quem apresenta, voz/idioma e texto antes de geração paga. Não use identidade ou voz de terceiros sem autorização. Não transforme uma fala solicitada em vídeo silencioso. Se houver ambiguidade, prepare fotos, manifesto e prompts enquanto aguarda a resposta; não consuma geração dependente dessa escolha.

## Estrutura e retomada

Crie `producoes/ID/` com `originais/`, `verticais/`, `takes/`, `revisao/` e `final/`. Copie `templates/manifesto.json`. Caminhos do manifesto são relativos à sua pasta. Atualize-o após cada etapa. Relacione todo resultado pelo ID do ambiente e do take, nunca pela ordem de chegada. Registre fornecedor, modelo, prompt, job ID, estado, tentativas, arquivo e revisão. Reutilize resultados corretos; não regenere ao retomar.

Estados: pendente → enviado → processando → baixado → aprovado; erro registra motivo e etapa. No máximo duas novas tentativas de geração por take; depois relate a falha e peça orientação. Não registre aprovado sem inspecionar.

## 1. Anúncio e imagens

Abra a página com navegador/ferramenta disponível, examine toda a galeria e leia descrição, metragem e características. Baixe imagens originais na maior resolução disponível; descarte logo, ícones, thumbnails duplicados e imagens de outros anúncios. Não remova marcas d’água. Confira tipo real de arquivo, resolução e conteúdo visual de cada download; páginas HTML não são fotos. Registre URL de origem e arquivo. Não invente medidas de cômodos nem confunda área total com útil.

Se o anúncio depender de JavaScript, use o navegador; se o acesso continuar bloqueado, peça fotos e descrição. Não contorne autenticação ou substitua o imóvel. Escolha pelo menos quatro ambientes/visões distintos quando existirem referências; se faltarem, solicite mais fotos antes de inventar ambientes. Não duplique uma foto para simular cômodos diferentes.

## 2. Organização e conversão 9:16

Inspecione cada original antes da edição. Registre marcos: posição de portas, janelas, paredes, pilares, piso, teto e direção da câmera. Use a foto correta como referência no app confirmado, solicitando organização e verticalização na mesma edição. Não faça apenas um recorte que esconda o ambiente nem estique a imagem.

Prompt-base, preenchido com observações reais:

> Edite esta foto do ambiente {nome} para composição vertical 9:16. Preserve a arquitetura real, perspectiva, proporções e os marcos {marcos}. Organize {desordem_observada}, retire objetos soltos e arrume a cama quando houver. Se solicitado, substitua móveis por peças neutras de escala plausível; identifique esse resultado como projeção. Preserve circulação, luz natural e materiais. Não crie portas, janelas, áreas externas ou cômodos. Não esconda danos estruturais, infiltrações ou defeitos do imóvel. Não adicione pessoas, textos ou logos. Se precisar expandir o enquadramento, mantenha apenas continuidade plausível das superfícies existentes, sem inventar características. Entregue 9:16.

Conferir lado a lado com o original; confirmar dimensões reais, arquitetura e organização. Corrigir divergências antes do vídeo. Alterações de decoração são simulações ilustrativas, não estado atual do imóvel.

## 3. Takes reais

Padrão: um POV de cerca de cinco segundos por ambiente, usando a vertical aprovada como referência inicial. Ajuste à duração e aos recursos realmente suportados pelo modelo.

Prompt passeio:

> Vídeo vertical 9:16 fotorrealista, câmera na altura dos olhos avançando lentamente por uma trajetória curta e livre em {nome}. Preserve {marcos}, iluminação, móveis e identidade da imagem de referência. Movimento suave e real, sem cortes, deformações, pessoas, mãos, voz ou mudanças de móveis. Não atravesse paredes nem invente outro cômodo.

Modo apresentador: mantenha a imagem como referência do imóvel, use identidade autorizada ou personagem fictício, roteiro factual aprovado e português brasileiro. Descubra suporte real a áudio/lip sync; se necessário, use etapas separadas documentadas. Preserve arquitetura e valide sincronia, inteligibilidade e afirmações. Registre o roteiro. Não prometa fala só porque o prompt menciona voz.

Transformação vazio → mobiliado é opcional: só adicione quando solicitada. Nesse caso gere dois takes por ambiente, transformação seguida de POV, usando referências correspondentes. Uma versão esvaziada deve ser identificada como simulação.

Acompanhe jobs até conclusão efetiva, baixe clipes reais, confira início/meio/fim, movimento, proporção e correspondência com a imagem. Nunca substitua por slideshow ou zoom em foto. Preserve áudios no modo apresentador.

## 4. Montagem

Liste os takes aprovados em `ordem_takes`, na ordem narrativa. Para transformação, mantenha cada par transformação → POV. Execute `python scripts/montar_video.py producoes/ID/manifesto.json` a partir da raiz do checkout. O script exige takes aprovados, vídeos reais e entradas válidas; não adiciona fala ou efeitos automaticamente.

Use música original ou licenciada quando fornecida, registrando licença; não baixe trilha aleatória. No modo passeio, áudio é opcional e a ausência deve ser informada. No modo apresentador, a fala é obrigatória e a montagem a preserva. Não acrescente preço, CTA, logo ou textos sem pedido.

## 5. Revisão e entrega

Confira início/meio/fim e todas as junções do MP4, ordem, duplicações, continuidade, enquadramento e duração. Inspecione visualmente cada take contra seu original; metadados não provam movimento ou fidelidade. Ouça o áudio quando a ferramenta permitir; declare quando não foi possível ouvir. Registre revisão final no manifesto. Não marque entrega concluída se houver job pendente ou revisão reprovada.

Entregue link persistente do MP4, duração e indicação “organização/decoração ilustrativa”. Preserve originais, verticais, takes e manifesto no armazenamento disponível. Se houver bloqueio, entregue o progresso concreto e explique a ferramenta, acesso ou material que falta; nunca afirme que o vídeo foi gerado quando só há prompts.
