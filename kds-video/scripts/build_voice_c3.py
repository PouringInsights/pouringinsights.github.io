import json, soundfile as sf, numpy as np
P='/home/user/calesthio/openmontage/remotion-composer/public/kds/audio/'
v,sr=sf.read(P+'vocals.wav'); v=v.mean(1) if v.ndim>1 else v
def rms(i,w): return np.sqrt(np.mean(v[max(0,i):i+w]**2))+1e-9
def quiet(t,lo,hi):
    hop=int(0.005*sr); win=int(0.02*sr); best=None
    for i in range(int((t+lo)*sr),int((t+hi)*sr),hop):
        e=rms(i,win)
        if best is None or e<best[0]: best=(e,(i+win/2)/sr)
    return best[1],20*np.log10(best[0])
# (scene, id, start, end, gap_before)
SEG=[
 ("intro","name",11.00,14.065,8.0),("intro","young",15.62,20.15,0.45),
 ("found","found",20.2,30.42,1.3),("found","majors",30.915,36.02,0.6),("found","aim",36.10,42.75,0.45),
 ("faculty","behind",45.62,49.30,1.3),("faculty","faculty",49.45,59.22,0.45),("faculty","views",59.55,65.45,0.4),("faculty","learn",65.80,72.20,0.5),
 ("research","classes",72.20,76.40,1.3),("research","research",76.62,85.15,0.4),
 ("contests","life",93.66,99.62,1.3),("contests","logi",100.38,108.08,0.6+0.58),("contests","logi2",108.10,114.45,0.35),("contests","mc8",114.55,119.80,0.6),("contests","mj",122.50,131.40,0.45),
 ("experience","pieces",131.55,138.40,1.3),
 ("partners","partners",141.66,150.60,13.0),("partners","partners2",151.12,153.30,0.12),("partners","questions",153.72,164.86,0.5+0.40),
 ("outcomes","outcomes",164.86,170.64,1.3),
 ("outro","outro",187.30,193.90,1.6),
]
out=[];t=0.0;plan=[];fade=int(0.02*sr)
for sc,sid,a,b,gap in SEG:
    EXACT={'logi','partners','partners2'}
    a2,ea=(a,-99) if sid in EXACT else quiet(a,-0.12,0.06)
    b2,eb=(b,-99) if sid in ('partners',) else quiet(b,-0.06,0.12)
    if ea>-55 or eb>-55: print('WARN',sid,round(a2,3),round(ea,1),round(b2,3),round(eb,1))
    t+=gap
    seg=v[int(a2*sr):int(b2*sr)].copy(); seg[:fade]*=np.linspace(0,1,fade); seg[-fade:]*=np.linspace(1,0,fade)
    out+=[np.zeros(int(gap*sr)),seg]
    plan.append({"scene":sc,"id":sid,"src":round(a2,3),"end":round(b2,3),"at":round(t,3),"dur":round(b2-a2,3)})
    t+=b2-a2
tail=7.5; out.append(np.zeros(int(tail*sr))); t+=tail
y=np.concatenate(out); y=y/np.max(np.abs(y))*0.89
sf.write(P+'voice_c.wav',y,sr)
json.dump({"total":round(t,3),"segments":plan},open('plan_c.json','w'),indent=1,ensure_ascii=False)
print('TOTAL',round(t,2))
for p in plan: print(p)
