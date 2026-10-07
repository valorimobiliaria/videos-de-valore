# Vídeos de Valor

Cérebro de um agente editor de vídeos imobiliários: link → fotos → organização visual e enquadramento 9:16 → takes POV → MP4 com FFmpeg.

As instruções estão em [skills/editor-imobiliario/SKILL.md](skills/editor-imobiliario/SKILL.md). O agente deve usar as ferramentas disponíveis para acessar anúncios e gerar imagens/vídeos. Não existe integração automática com uma API de geração neste repositório; o fornecedor confirmado é o Higgsfield, e suas ferramentas e capacidades precisam ser descobertas antes de gerar. O modo escolhido é passeio de câmera sem apresentador.

## Uso

Para começar em outra máquina, abra este repositório no seu agente e leia `AGENTS.md`. As oito skills oficiais instaladas estão em `.agents/skills/`, e a origem está registrada em `skills-lock.json`.

Em uma máquina com navegador interativo, instale Node.js e execute:

```bash
npm i -g @higgsfield/cli
higgsfield auth login
```

Conclua o login nessa mesma máquina e verifique `higgsfield workspace list` e `higgsfield account status`. Se necessário, selecione o workspace correto. O login de outra máquina não autentica automaticamente este checkout. A cobrança e os benefícios disponíveis devem ser verificados na conta antes da geração.

O projeto também requer Python 3.10+, FFmpeg e ffprobe. A coleta de anúncios depende de ferramentas de navegação disponíveis no agente. Não há servidor ou interface web implementados.

Peça ao agente: “Crie um vídeo deste imóvel: URL”. Ele cria uma pasta `producoes/IDENTIFICADOR/`, copia o modelo de manifesto, examina as fotos e acompanha cada resultado. O manifesto é atualizado durante toda a produção.

Para montar takes já baixados e aprovados:

```bash
python scripts/montar_video.py producoes/IDENTIFICADOR/manifesto.json
```

Requer Python 3.10+, FFmpeg e ffprobe no PATH. O comando valida os arquivos, normaliza os takes para 1080×1920 a 30 fps sem esticar, concatena, exporta H.264/yuv420p/faststart e valida o MP4. Pode incluir música informada no manifesto; no modo com apresentador conserva o áudio dos takes e exige áudio em cada um.

Não há download automático de anúncios nem geração automática: essas etapas são conduzidas pelo agente com as ferramentas disponíveis e registradas no manifesto. Fotos de um imóvel real e acesso ao fornecedor são necessários para validar uma produção completa.

Leia [HANDOFF.md](HANDOFF.md) para retomar a produção solicitada e identificar os bloqueios ainda pendentes.
