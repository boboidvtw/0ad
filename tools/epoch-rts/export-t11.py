#!/usr/bin/env python3
"""Purpose: reproducible original T11 rigid-rig COLLADA and HUD export. Created: 2026-09-21.
SPDX-License-Identifier: GPL-2.0-or-later. Generated art: CC-BY-SA-3.0.
Seven bones, one normalized influence/vertex, authored X-axis keyframes, no external packages.
"""
import argparse
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import struct
import xml.etree.ElementTree as ET
import zlib

NS = 'http://www.collada.org/2005/11/COLLADASchema'
ET.register_namespace('', NS)
REPO = Path(__file__).resolve().parents[2]
MOD = REPO / 'binaries/data/mods/epoch_rts'

def el(parent, tag, text=None, **attrs):
    n = ET.SubElement(parent, '{%s}%s' % (NS, tag), attrs)
    if text is not None:
        n.text = str(text)
    return n

def nums(v):
    return ' '.join(format(x, '.8g') if isinstance(x, (int, float)) else x for x in v)

def source(parent, name, rows, params, kind='float', param_type='float'):
    s = el(parent, 'source', id=name)
    flat = [x for row in rows for x in row]
    el(s, kind+'_array', nums(flat), id=name+'-array', count=str(len(flat)))
    a = el(el(s, 'technique_common'), 'accessor', source='#'+name+'-array', count=str(len(rows)), stride=str(len(rows[0])))
    for p in params:
        el(a, 'param', name=p, type=param_type)

def matrix(x=0, y=0, z=0, angle=0):
    c, s = math.cos(math.radians(angle)), math.sin(math.radians(angle))
    return [1,0,0,x, 0,c,-s,y, 0,s,c,z, 0,0,0,1]

def xml(root):
    ET.indent(root, space='  ')
    return ET.tostring(root, encoding='utf-8', xml_declaration=True)+b'\n'

def png(width, height, pixels):
    def chunk(kind, data):
        return struct.pack('>I',len(data))+kind+data+struct.pack('>I',zlib.crc32(kind+data)&0xffffffff)
    raw=b''.join(b'\0'+bytes(sum(pixels[y*width:(y+1)*width], [])) for y in range(height))
    return b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',width,height,8,6,0,0,0))+chunk(b'IDAT',zlib.compress(raw,9))+chunk(b'IEND',b'')

def mesh(spec, role, clip=None):
    positions, normals, uv, triangles, weights = [], [], [], [], []
    def face(points, color, bone):
        a,b,c=points[:3];u=[b[i]-a[i] for i in range(3)];v=[c[i]-a[i] for i in range(3)]
        n=[u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]]
        length=math.sqrt(sum(x*x for x in n));start=len(positions)
        for p in points:
            positions.append(p);normals.append([x/length for x in n]);uv.append([(color+.5)/8,.5]);weights.append(bone)
        for i in range(1,len(points)-1):triangles.append([start,start+i,start+i+1])
    def box(x0,x1,y0,y1,z0,z1,color,bone):
        for pts in [[(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)],[(x1,y0,z0),(x0,y0,z0),(x0,y1,z0),(x1,y1,z0)],[(x1,y0,z1),(x1,y0,z0),(x1,y1,z0),(x1,y1,z1)],[(x0,y0,z0),(x0,y0,z1),(x0,y1,z1),(x0,y1,z0)],[(x0,y1,z1),(x1,y1,z1),(x1,y1,z0),(x0,y1,z0)],[(x0,y0,z0),(x1,y0,z0),(x1,y0,z1),(x0,y0,z1)]]:
            face(pts,color,bone)
    # Chunky silhouette with visible gaps at shoulders and hips; 4m visual unit height.
    box(-.65,.65,1.8,3.15,-.34,.34,0 if role=='worker' else 4,1)
    box(-.48,.48,2.25,3.05,.345,.37,3,1)
    box(-.48,.48,2.25,3.05,-.37,-.345,3,1)
    box(-.7,.7,1.65,1.9,-.38,.38,2,1)
    box(-.38,.38,3.28,3.95,-.32,.32,5,2)
    for bone,x in [(3,-.85),(4,.85)]:
        box(x-.19,x+.19,1.95,3,-.2,.2,0 if role=='worker' else 4,bone)
        box(x-.19,x+.19,1.7,1.98,-.2,.2,5,bone)
    for bone,x in [(5,-.35),(6,.35)]:
        box(x-.23,x+.23,.25,1.65,-.22,.22,2,bone)
        box(x-.25,x+.25,.05,.35,-.26,.45,2,bone)
    if role=='worker':
        box(-.66,.66,3.9,4.05,-.6,.6,7,2)
        box(-.4,.4,4.05,4.3,-.35,.35,7,2)
        box(.79,.91,1.45,2.35,.2,.32,2,4)
        box(.58,1.1,2.25,2.5,.12,.4,4,4)
    else:
        box(-.45,.45,3.82,4.16,-.38,.38,4,2)
        box(-.12,.12,4.16,4.5,-.35,.35,1,2)
        box(-1.48,-.6,1.7,3.15,.32,.48,4,3)
        box(-1.34,-.74,1.9,2.96,.48,.52,3,3)
        box(.8,.9,.3,5.65,.26,.36,2,4)
        face([(.64,5.65,.31),(1.06,5.65,.31),(.85,6.2,.31)],4,4)
        face([(1.06,5.65,.32),(.64,5.65,.32),(.85,6.2,.32)],4,4)
    r=ET.Element('{%s}COLLADA'%NS,version='1.4.1');a=el(r,'asset');c=el(a,'contributor')
    el(c,'author','Epoch RTS contributors');el(c,'authoring_tool','T11 deterministic rig exporter v1')
    el(a,'created','2026-09-21T00:00:00Z');el(a,'modified','2026-09-21T00:00:00Z');el(a,'unit',name='meter',meter='1');el(a,'up_axis','Y_UP')
    m=el(el(el(r,'library_geometries'),'geometry',id='body',name=role),'mesh')
    source(m,'positions',positions,['X','Y','Z']);source(m,'normals',normals,['X','Y','Z']);source(m,'uv',uv,['S','T'])
    el(el(m,'vertices',id='verts'),'input',semantic='POSITION',source='#positions')
    t=el(m,'triangles',count=str(len(triangles)))
    for offset,(semantic,name) in enumerate([('VERTEX','verts'),('NORMAL','normals'),('TEXCOORD','uv')]):
        attrs={'semantic':semantic,'source':'#'+name,'offset':str(offset)}
        if semantic=='TEXCOORD':attrs['set']='0'
        el(t,'input',**attrs)
    el(t,'p',nums([n for tri in triangles for i in tri for n in [i]*3]))
    skin=el(el(el(r,'library_controllers'),'controller',id='skin',name='skin'),'skin',source='#body')
    el(skin,'bind_shape_matrix',nums(matrix()))
    bones=spec['bones'];source(skin,'joints',[[b[0]] for b in bones],['JOINT'],'Name','Name')
    source(skin,'binds',[matrix(-b[1],-b[2],-b[3]) for b in bones],['TRANSFORM'],param_type='float4x4')
    source(skin,'weights',[[1]],['WEIGHT'])
    joints=el(skin,'joints');el(joints,'input',semantic='JOINT',source='#joints');el(joints,'input',semantic='INV_BIND_MATRIX',source='#binds')
    w=el(skin,'vertex_weights',count=str(len(positions)));el(w,'input',semantic='JOINT',source='#joints',offset='0');el(w,'input',semantic='WEIGHT',source='#weights',offset='1')
    el(w,'vcount',nums([1]*len(positions)));el(w,'v',nums([v for b in weights for v in (b,0)]))
    if clip:
        anims=el(r,'library_animations');settings=spec['clips'][clip]
        for b in bones:
            name=b[0];angles=settings['angles'].get(name,[0]*5);anim=el(anims,'animation',id=name+'-anim')
            source(anim,name+'-time',[[i*settings['duration']/4] for i in range(5)],['TIME'])
            source(anim,name+'-pose',[matrix(*b[1:],angle=v) for v in angles],['TRANSFORM'],param_type='float4x4')
            source(anim,name+'-interp',[['LINEAR']]*5,['INTERPOLATION'],'Name','Name')
            sampler=el(anim,'sampler',id=name+'-sampler')
            for sem,src in [('INPUT','time'),('OUTPUT','pose'),('INTERPOLATION','interp')]:el(sampler,'input',semantic=sem,source='#'+name+'-'+src)
            el(anim,'channel',source='#'+name+'-sampler',target=name+'/transform')
    scene=el(el(r,'library_visual_scenes'),'visual_scene',id='Scene')
    root=None
    for i,b in enumerate(bones):
        node=el(scene if i==0 else root,'node',id=b[0],sid=b[0],name=b[0],type='JOINT');el(node,'matrix',nums(matrix(*b[1:])),sid='transform')
        if i==0:root=node
    inst=el(el(scene,'node',id='model',name='model'),'instance_controller',url='#skin');el(inst,'skeleton','#epoch_root')
    el(el(r,'scene'),'instance_visual_scene',url='#Scene')
    return xml(r),{'vertices':len(positions),'triangles':len(triangles),'bones':len(bones),'bounds_min':[min(p[i] for p in positions) for i in range(3)],'bounds_max':[max(p[i] for p in positions) for i in range(3)]}

def icon(role,palette):
    # Original geometric silhouettes, drawn directly at 128px (no external image input).
    pixels=[]
    for y in range(128):
        for x in range(128):
            c=palette[6][:3]+[255]
            if min(x,y,127-x,127-y)<4:c=palette[4]
            elif min(x,y,127-x,127-y)<8:c=palette[2]
            if role=='worker':
                if 37<x<91 and 61<y<112:c=palette[0]
                if 47<x<81 and 38<y<67:c=palette[5]
                if (25<x<103 and 35<y<44) or (43<x<85 and 20<y<36):c=palette[7]
                if 88<x<94 and 59<y<111 or 77<x<106 and 58<y<71:c=palette[4]
            elif role=='soldier':
                if 39<x<80 and 58<y<112:c=palette[4]
                if 46<x<76 and 33<y<59:c=palette[5]
                if 40<x<82 and 25<y<40:c=palette[4]
                if 57<x<65 and 14<y<27:c=palette[1]
                if 25<x<54 and 65<y<106:c=palette[0]
                if 92<x<97 and 32<y<113 or abs(x-94)<(y-14)/3 and 14<y<33:c=palette[4]
            else:
                if 30<x<98 and 62<y<107:c=palette[0]
                if 28<y<65 and abs(x-64)<(y-26)*1.2:c=palette[1]
                if 53<x<74 and 78<y<107:c=palette[2]
            pixels.append(c)
    return png(128,128,pixels)

def build(spec):
    outputs={};metrics={}
    for role in ['worker','soldier']:
        outputs['art/meshes/skeletal/epoch_rts/t11_'+role+'.dae'],metrics[role]=mesh(spec,role)
        outputs['art/textures/ui/session/portraits/epoch_rts/t11_'+role+'.png']=icon(role,spec['palette'])
    for clip in spec['clips']:
        outputs['art/animation/epoch_rts/t11_'+clip+'.dae']=mesh(spec,'worker',clip)[0]
    colors=spec['palette'];outputs['art/textures/skins/epoch_rts/t11_palette.png']=png(128,16,[colors[x//16] for y in range(16) for x in range(128)])
    s=ET.Element('skeletons');standard=ET.SubElement(s,'standard_skeleton',id='epoch_t11',title='Epoch T11')
    mapping=ET.SubElement(s,'skeleton',target='epoch_t11',title='Epoch T11');ET.SubElement(ET.SubElement(mapping,'identifier'),'root').text='epoch_root'
    for parent,is_map in [(standard,False),(mapping,True)]:
        root=None
        for i,b in enumerate(spec['bones']):
            n=ET.SubElement(parent if i==0 else root,'bone',name=b[0])
            if is_map:ET.SubElement(n,'target').text=b[0]
            if i==0:root=n
    outputs['art/skeletons/epoch_t11.xml']=xml(s)
    loader=importlib.util.spec_from_file_location('house',Path(__file__).with_name('export-house.py'));house=importlib.util.module_from_spec(loader);loader.loader.exec_module(house)
    dae,texture,metrics['house']=house.export(spec['house'])
    outputs['art/meshes/structural/epoch_rts/t11_house.dae']=dae;outputs['art/textures/skins/structural/epoch_rts/t11_house.png']=texture
    outputs['art/textures/ui/session/portraits/epoch_rts/t11_house.png']=icon('house',colors)
    return outputs,metrics

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true');args=parser.parse_args()
    spec=json.loads((REPO/'assets/epoch-rts/t11-slice/slice.json').read_text());outputs,metrics=build(spec)
    for name,data in outputs.items():
        path=MOD/name
        if args.check:
            if not path.is_file() or path.read_bytes()!=data:raise SystemExit('Output mismatch: '+name)
        else:path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
    print(json.dumps({'metrics':metrics,'outputs':{n:hashlib.sha256(d).hexdigest() for n,d in outputs.items()}},indent=2))

if __name__=='__main__':main()
