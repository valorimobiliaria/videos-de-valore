"""Montagem de takes aprovados. Sem dependências Python externas."""
import argparse
import json
import math
from pathlib import Path
import subprocess
import tempfile


def run(args):
    return subprocess.run(args, check=True, capture_output=True, text=True).stdout


def probe(path):
    return json.loads(run(['ffprobe', '-v', 'error', '-show_streams',
                           '-show_format', '-of', 'json', str(path)]))


def assemble(manifest):
    data = json.loads(manifest.read_text())
    base = manifest.resolve().parent
    mode = data['modo']
    if mode not in ('passeio', 'apresentador'):
        raise ValueError('Modo inválido')
    takes = data['takes']
    ids = [t['id'] for t in takes]
    order = data['ordem_takes']
    if len(ids) != len(set(ids)) or not order or len(order) != len(set(order)):
        raise ValueError('IDs duplicados ou ordem vazia')
    indexed = {t['id']: t for t in takes}
    paths, durations = [], []
    for ident in order:
        take = indexed[ident]
        if take['estado'] != 'aprovado':
            raise ValueError(f'Take ainda não aprovado: {ident}')
        path = (base / take['arquivo']).resolve()
        info = probe(path)
        videos = [s for s in info['streams'] if s['codec_type'] == 'video']
        if not videos or videos[0].get('disposition', {}).get('attached_pic'):
            raise ValueError(f'Vídeo ausente: {ident}')
        duration = float(info['format']['duration'])
        if not math.isfinite(duration) or duration <= 0:
            raise ValueError(f'Duração inválida: {ident}')
        if mode == 'apresentador' and not any(s['codec_type'] == 'audio' for s in info['streams']):
            raise ValueError(f'Fala ausente: {ident}')
        paths.append(path)
        durations.append(duration)
    output = (base / data['saida']).resolve()
    if output in paths or output.exists():
        raise ValueError('Saída já existe ou coincide com uma entrada; escolha outra saída')
    output.parent.mkdir(parents=True, exist_ok=True)
    music = (base / data['musica']).resolve() if data.get('musica') else None
    if music and (not data.get('musica_licenca') or not music.is_file()):
        raise ValueError('Música precisa de arquivo e registro de licença')
    cmd = ['ffmpeg', '-v', 'error', '-nostdin', '-n']
    for path in paths:
        cmd += ['-i', str(path)]
    if music:
        cmd += ['-stream_loop', '-1', '-i', str(music)]
    filters, labels = [], []
    speech = mode == 'apresentador'
    for i in range(len(paths)):
        filters.append(f'[{i}:v:0]scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=30,setpts=PTS-STARTPTS,format=yuv420p[v{i}]')
        labels.append(f'[v{i}]')
        if speech:
            filters.append(f'[{i}:a:0]aresample=48000,aformat=channel_layouts=stereo,apad,atrim=duration={durations[i]},asetpts=PTS-STARTPTS[a{i}]')
            labels.append(f'[a{i}]')
    filters.append(''.join(labels) + f'concat=n={len(paths)}:v=1:a={int(speech)}[video]' + ('[speech]' if speech else ''))
    audio = '[speech]' if speech else None
    if music:
        total = sum(durations)
        filters.append(f'[{len(paths)}:a:0]aresample=48000,aformat=channel_layouts=stereo,atrim=duration={total},asetpts=PTS-STARTPTS,volume=0.15,afade=t=in:d=0.5,afade=t=out:st={max(0,total-0.5)}:d=0.5[music]')
        if speech:
            filters.append('[speech][music]amix=inputs=2:duration=first:normalize=0[audio]')
            audio = '[audio]'
        else:
            audio = '[music]'
    cmd += ['-filter_complex_threads', '1', '-filter_complex', ';'.join(filters), '-map', '[video]']
    cmd += ['-map', audio, '-c:a', 'aac'] if audio else ['-an']
    cmd += ['-c:v', 'libx264', '-threads', '2', '-preset', 'fast', '-crf', '20', '-pix_fmt', 'yuv420p', '-movflags', '+faststart']
    with tempfile.TemporaryDirectory(dir=output.parent) as tmp:
        candidate = Path(tmp) / 'video.mp4'
        run(cmd + [str(candidate)])
        info = probe(candidate)
        video = next(s for s in info['streams'] if s['codec_type'] == 'video')
        if (video['width'], video['height'], video['codec_name']) != (1080, 1920, 'h264'):
            raise ValueError('Exportação inválida')
        if abs(float(info['format']['duration']) - sum(durations)) > max(0.5, len(paths) / 30):
            raise ValueError('Duração exportada divergente')
        if audio and not any(s['codec_type'] == 'audio' for s in info['streams']):
            raise ValueError('Áudio ausente na exportação')
        candidate.rename(output)
    print(f'MP4 exportado: {output}; {info["format"]["duration"]} segundos. Revisão visual final pendente.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifesto', type=Path)
    args = parser.parse_args()
    try:
        assemble(args.manifesto)
    except subprocess.CalledProcessError as error:
        parser.exit(1, error.stderr or str(error))
    except (ValueError, KeyError, OSError) as error:
        parser.exit(1, f'{error}\n')
