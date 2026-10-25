#!/usr/bin/env python3
"""Build voiced versions of every cut.

  python3 video/mix.py clips.json          # clips.json: {"0": "<wav url>", ...}
  python3 video/mix.py clips.json --config audio/v2.json   # v2 design: page, lines and cut map

For each cut: times every scene to its voiceover clip (clip + breathing room),
writes out/timing.json, builds a soft ambient music bed with sox, mixes voice
over music into out/audio-<cut>.wav, then renders out/jamal-akim-<cut>.mp4.
Needs ffmpeg, ffprobe, sox, curl and everything render.cjs needs.
"""
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'out')
CLIPS = os.path.join(HERE, 'audio')

# scene order per cut -> voiceover clip index (see README for the lines)
CUTS = {
    'main': list(range(16)),
    'hook': [0, 20],
    'motivate': [14, 20],
    'identity': [1, 20],
    'whatif': [16, 17, 18, 9, 11, 19],
}
LEAD, TAIL, MIN_END = 0.35, 0.6, 3.0
CHORDS = [  # A minor: Am, F, C, G
    ['A2', 'E3', 'A3', 'C4', 'E4'],
    ['F2', 'C3', 'F3', 'A3', 'C4'],
    ['C3', 'G3', 'C4', 'E4', 'G4'],
    ['G2', 'D3', 'G3', 'B3', 'D4'],
]


def run(cmd):
    subprocess.run(cmd, check=True)


def duration(path):
    out = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                          '-of', 'csv=p=0', path], check=True, capture_output=True, text=True)
    return float(out.stdout.strip())


def music_bed(seconds, path):
    parts = []
    for i, notes in enumerate(CHORDS):
        f = os.path.join(OUT, f'chord{i}.wav')
        synth = []
        for n in notes:
            synth += ['sine', n, 'triangle', n]
        run(['sox', '-n', '-r', '48000', '-c', '2', f, 'synth', '4.2', *synth,
             'gain', '-n', '-6', 'lowpass', '1800', 'tremolo', '0.25', '15',
             'fade', 'q', '1.2', '4.2', '1.6', 'chorus', '0.6', '0.9', '55', '0.4', '0.25', '2', '-t',
             'reverb', '70'])
        parts.append(f)
    loop = os.path.join(OUT, 'loop.wav')
    run(['sox', *parts, loop])
    reps = int(seconds // duration(loop)) + 1
    run(['sox', loop, path, 'repeat', str(reps), 'trim', '0', f'{seconds:.3f}',
         'fade', 't', '2', f'{seconds:.3f}', '3', 'gain', '-n', '-3'])


def main():
    global CUTS
    urls = json.load(open(sys.argv[1]))
    page = 'composer.html'
    if '--config' in sys.argv:
        cfg = json.load(open(sys.argv[sys.argv.index('--config') + 1]))
        CUTS, page = cfg['cuts'], cfg.get('page', page)
    only = sys.argv[sys.argv.index('--only') + 1].split(',') if '--only' in sys.argv else list(CUTS)
    os.makedirs(OUT, exist_ok=True); os.makedirs(CLIPS, exist_ok=True)
    lengths = {}
    clip = lambda k: os.path.join(CLIPS, f'vo-{k}.wav')
    for k, url in urls.items():
        f = clip(k)
        if not os.path.exists(f):
            run(['curl', '-sSfL', '-o', f, url])
        lengths[k] = duration(f)

    timing = {}
    for cut, clips in CUTS.items():
        durs = [lengths[str(c)] + LEAD + TAIL for c in clips]
        durs[-1] = max(durs[-1], MIN_END)
        timing[cut] = [round(d, 3) for d in durs]
    tfile = os.path.join(OUT, 'timing.json')
    json.dump(timing, open(tfile, 'w'), indent=1)

    for cut in only:
        clips = CUTS[cut]
        total = sum(timing[cut])
        bed = os.path.join(OUT, f'bed-{cut}.wav')
        music_bed(total, bed)
        inputs, filters, start = ['-i', bed], ['[0]volume=0.16[m]'], 0.0
        for i, c in enumerate(clips):
            inputs += ['-i', clip(c)]
            ms = int((start + LEAD) * 1000)
            filters.append(f'[{i + 1}]aresample=48000,pan=stereo|c0=c0|c1=c0,adelay={ms}|{ms}[v{i}]')
            start += timing[cut][i]
        voices = ''.join(f'[v{i}]' for i in range(len(clips)))
        filters.append(f'{voices}amix=inputs={len(clips)}:normalize=0[vo]')
        filters.append('[m][vo]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[out]')
        track = os.path.join(OUT, f'audio-{cut}.wav')
        run(['ffmpeg', '-y', '-loglevel', 'error', *inputs, '-filter_complex', ';'.join(filters),
             '-map', '[out]', '-t', f'{total:.3f}', '-ar', '48000', track])
        if '--no-render' not in sys.argv:
            run(['node', os.path.join(HERE, 'render.cjs'), cut, '--page', page, '--timing', tfile, '--audio', track])


if __name__ == '__main__':
    main()
