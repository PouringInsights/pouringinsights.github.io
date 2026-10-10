import json, subprocess, soundfile as sf, numpy as np
P='/home/user/calesthio/openmontage/remotion-composer/public/kds/audio/'
# (id, src_start, src_end, gap_before)
SEG=[("name",11.00,14.065,3.6),("found",20.20,30.42,0.9),("majors",30.915,36.02,0.6),
("faculty",49.45,59.22,1.0),("learn",65.80,72.20,0.9),("research",76.70,85.15,0.9),
("life",93.66,99.62,1.0),("logi",99.80,108.08,0.9),("mj",122.50,131.40,0.8),
("partners",141.66,153.30,1.0),("questions",153.72,164.86,0.8),("outcomes",164.86,170.64,0.5),
("outro",187.30,193.90,1.2)]
v,sr=sf.read(P+'vocals.wav'); 
if v.ndim>1: v=v.mean(1)
out=[]; t=0.0; plan=[]
fade=int(0.025*sr)
for sid,a,b,gap in SEG:
    t+=gap
    seg=v[int(a*sr):int(b*sr)].copy()
    seg[:fade]*=np.linspace(0,1,fade); seg[-fade:]*=np.linspace(1,0,fade)
    out.append(np.zeros(int(gap*sr))); out.append(seg)
    plan.append({"id":sid,"src":[a,b],"at":round(t,3),"offset":round(t-a,3),"dur":round(b-a,3)})
    t+=b-a
tail=4.5; out.append(np.zeros(int(tail*sr))); t+=tail
y=np.concatenate(out); 
y=y/np.max(np.abs(y))*0.89
sf.write(P+'voice_b.wav',y,sr)
json.dump({"total":round(t,3),"segments":plan},open('plan.json','w'),indent=1)
print(round(t,2)); [print(p) for p in plan]
