# Adds an optional beat ("pulse") under the music bed for cuts listed in the config's "pulse" key.
#   python3 video/patches/pulse.py video/mix.py
import sys

p = sys.argv[1]
s = open(p).read()


def R(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:60])
    s = s.replace(a, b)


R("""        CUTS, page = cfg['cuts'], cfg.get('page', page)""", """        CUTS, page = cfg['cuts'], cfg.get('page', page)
        pulse = cfg.get('pulse', [])""")
R("""    page = 'composer.html'
""", """    page, pulse = 'composer.html', []
""")
R("""        music_bed(total, bed)
""", """        music_bed(total, bed)
        if cut in pulse:
            # soft 120 bpm kick + offbeat hat, faded in and out
            beat = os.path.join(OUT, f'pulse-{cut}.wav')
            expr = ('0.55*sin(2*PI*(45+70*exp(-mod(t,0.5)*30))*mod(t,0.5))*exp(-mod(t,0.5)*9)'
                    '+0.06*(random(0)*2-1)*exp(-mod(t+0.25,0.5)*70)')
            run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'lavfi', '-i',
                 f"aevalsrc='{expr}':s=48000:d={total:.3f}",
                 '-af', f'afade=t=in:d=2,afade=t=out:st={max(total - 3, 0):.3f}:d=3', '-ac', '2', beat])
            mixed = os.path.join(OUT, f'bedp-{cut}.wav')
            run(['sox', '-m', '-v', '1', bed, '-v', '0.6', beat, mixed])
            bed = mixed
""")
open(p, 'w').write(s)
print('patched', p)
