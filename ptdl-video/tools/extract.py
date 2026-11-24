import re, sys, os, json
from lxml import etree
ns={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
root=sys.argv[1]; out=sys.argv[2]
pres=etree.parse(f"{root}/ppt/presentation.xml")
rels=etree.parse(f"{root}/ppt/_rels/presentation.xml.rels")
rmap={r.get('Id'):r.get('Target') for r in rels.getroot()}
order=[rmap[s.get('{%s}id'%ns['r'])] for s in pres.findall('.//p:sldId',ns)]
lines=[]
for i,t in enumerate(order,1):
    x=etree.parse(f"{root}/ppt/{t}")
    hidden=x.getroot().get('show')=='0'
    paras=[]
    for p in x.findall('.//a:p',ns):
        s=''.join(r.text or '' for r in p.findall('.//a:t',ns)).strip()
        if s: paras.append(s)
    note=''
    rp=f"{root}/ppt/slides/_rels/{os.path.basename(t)}.rels"
    if os.path.exists(rp):
        for r in etree.parse(rp).getroot():
            if 'notesSlide' in r.get('Target'):
                nx=etree.parse(os.path.normpath(f"{root}/ppt/slides/{r.get('Target')}"))
                note=' / '.join(''.join(q.text or '' for q in p.findall('.//a:t',ns)).strip() for p in nx.findall('.//a:p',ns))
                note=re.sub(r'(\s*/\s*)+',' / ',note).strip(' /')
    lines.append(f"### SLIDE {i}{' (HIDDEN)' if hidden else ''}\n"+'\n'.join(paras)+(f"\n[GHI CHÚ GV]: {note}" if note and not note.isdigit() else ''))
open(out,'w').write('\n\n'.join(lines))
print(out, len(order))
