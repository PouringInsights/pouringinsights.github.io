# Version B narration v3: drops the mispronounced "HaUI" before LogiMaster and the word "TDS".
import json, soundfile as sf, numpy as np
P='/home/user/calesthio/openmontage/remotion-composer/public/kds/audio/'
v,sr=sf.read(P+'vocals.wav'); v=v.mean(1) if v.ndim>1 else v
# (id, src_start, src_end, at)  -- 'at' keeps the v2 timeline except after the TDS cut (-0.40 s)
SEG=[("name",11.0,14.065,3.6),("found",20.2,30.42,7.565),("majors",30.915,36.02,18.385),
("faculty",49.45,59.22,24.49),("learn",65.8,72.2,35.16),("research",76.7,85.15,42.46),
("life",93.66,99.62,51.91),("logi",100.38,108.08,58.77+0.58),("mj",122.5,131.4,67.85),
("partners",141.66,150.60,77.75),("partners2",151.12,153.30,77.75+(151.12-141.66)-0.40),
("questions",153.72,164.86,90.19-0.40),("outcomes",164.86,170.64,101.83-0.40),("outro",187.3,193.9,108.81-0.40)]
total=119.91-0.40
y=np.zeros(int(total*sr)); fade=int(0.02*sr); plan=[]
for sid,a,b,at in SEG:
    seg=v[int(a*sr):int(b*sr)].copy(); seg[:fade]*=np.linspace(0,1,fade); seg[-fade:]*=np.linspace(1,0,fade)
    i=int(at*sr); y[i:i+len(seg)]+=seg
    plan.append({"id":sid,"src":a,"at":round(at,3),"dur":round(b-a,3)})
y=y/np.max(np.abs(y))*0.89
sf.write(P+'voice_b3.wav',y,sr)
json.dump({"total":round(total,3),"segments":plan},open('/home/user/calesthio/openmontage/remotion-composer/src/kds/plan_b.json','w'),indent=1)
print(total)
