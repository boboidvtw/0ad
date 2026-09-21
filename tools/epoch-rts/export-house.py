#!/usr/bin/env python3
"""Purpose: deterministic T10 static COLLADA/PNG exporter. Created: 2026-09-21.
SPDX-License-Identifier: GPL-2.0-or-later
No external packages. Generated art is CC-BY-SA-3.0 (see source asset README).
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import struct
import xml.etree.ElementTree as ET
import zlib

NS = 'http://www.collada.org/2005/11/COLLADASchema'
ET.register_namespace('', NS)


def element(parent, tag, text=None, **attrs):
    node = ET.SubElement(parent, '{%s}%s' % (NS, tag), attrs)
    if text is not None:
        node.text = str(text)
    return node


def export(spec):
    dims = ['width', 'depth', 'wall_height', 'roof_height', 'roof_overhang']
    if any(type(spec[k]) not in (int, float) or not math.isfinite(spec[k]) or not 0 < spec[k] <= 100 for k in dims):
        raise ValueError('Dimensions must be finite numbers in (0,100] meters')
    if spec['roof_overhang'] > min(spec['width'], spec['depth'])/4:
        raise ValueError('Overhang must not exceed one quarter of the smaller wall dimension')
    colors = [spec['palette'][k] for k in ['wall', 'roof', 'wood', 'player']]
    if any(len(c) != 4 or any(type(v) is not int or not 0 <= v <= 255 for v in c) for c in colors):
        raise ValueError('Palette must contain four RGBA byte values per color')
    positions, normals, uv, triangles = [], [], [], []
    # Y-up meters. +Z is front, ground origin at center. One UV tile per face.
    def face(points, color):
        a, b, c = points[:3]
        u = [b[i]-a[i] for i in range(3)]
        v = [c[i]-a[i] for i in range(3)]
        normal = [u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0]]
        length = math.sqrt(sum(x*x for x in normal))
        if length == 0:
            raise ValueError('Degenerate face')
        start = len(positions)
        for point in points:
            positions.append(point)
            normals.append([x/length for x in normal])
            uv.append([(color+0.5)/4, 0.5])
        for i in range(1, len(points)-1):
            triangles.append([start, start+i, start+i+1])
    def box(x0, x1, y0, y1, z0, z1, color):
        face([(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)],color)
        face([(x1,y0,z0),(x0,y0,z0),(x0,y1,z0),(x1,y1,z0)],color)
        face([(x1,y0,z1),(x1,y0,z0),(x1,y1,z0),(x1,y1,z1)],color)
        face([(x0,y0,z0),(x0,y0,z1),(x0,y1,z1),(x0,y1,z0)],color)
        face([(x0,y1,z1),(x1,y1,z1),(x1,y1,z0),(x0,y1,z0)],color)
        face([(x0,y0,z0),(x1,y0,z0),(x1,y0,z1),(x0,y0,z1)],color)
    x, z = spec['width']/2, spec['depth']/2
    h, top = spec['wall_height'], spec['wall_height']+spec['roof_height']
    over = spec['roof_overhang']
    box(-x,x,0,h,-z,z,0)
    # Gable roof; ridge follows Z. Outward winding and separate face normals.
    a,b,c=(-x-over,h,z+over),(x+over,h,z+over),(0,top,z+over)
    d,e,f=(-x-over,h,-z-over),(x+over,h,-z-over),(0,top,-z-over)
    face([a,b,c],1);face([e,d,f],1)
    face([a,c,f,d],1);face([c,b,e,f],1);face([d,e,b,a],1)
    box(-x*0.18,x*0.18,0,h*0.675,z,z+spec['depth']*0.015,2)  # front door
    box(-x,x,h*0.3,h*0.5,z,z+spec['depth']*0.01,3)  # broad player-color wall bands
    box(-x,x,h*0.3,h*0.5,-z-spec['depth']*0.01,-z,3)
    box(-x-spec['width']*0.008,-x,h*0.3,h*0.5,-z,z,3)
    box(x,x+spec['width']*0.008,h*0.3,h*0.5,-z,z,3)
    root = ET.Element('{%s}COLLADA' % NS, version='1.4.1')
    asset = element(root,'asset')
    contrib = element(asset,'contributor')
    element(contrib,'author','Epoch RTS contributors')
    element(contrib,'authoring_tool','Epoch RTS deterministic static exporter v1')
    element(asset,'created','2026-09-21T00:00:00Z')
    element(asset,'modified','2026-09-21T00:00:00Z')
    element(asset,'unit',name='meter',meter='1')
    element(asset,'up_axis','Y_UP')
    geometries=element(root,'library_geometries')
    geometry=element(geometries,'geometry',id='house-mesh',name='house')
    mesh=element(geometry,'mesh')
    for name, values, params in [('positions',positions,['X','Y','Z']),('normals',normals,['X','Y','Z']),('uv',uv,['S','T'])]:
        source=element(mesh,'source',id=name)
        element(source,'float_array',' '.join(format(v,'.8g') for row in values for v in row),id=name+'-array',count=str(len(values)*len(params)))
        access=element(element(source,'technique_common'),'accessor',source='#'+name+'-array',count=str(len(values)),stride=str(len(params)))
        for param in params:
            element(access,'param',name=param,type='float')
    vertex=element(mesh,'vertices',id='vertices')
    element(vertex,'input',semantic='POSITION',source='#positions')
    tris=element(mesh,'triangles',count=str(len(triangles)))
    for offset,(semantic,source) in enumerate([('VERTEX','vertices'),('NORMAL','normals'),('TEXCOORD','uv')]):
        attrs={'semantic':semantic,'source':'#'+source,'offset':str(offset)}
        if semantic=='TEXCOORD': attrs['set']='0'
        element(tris,'input',**attrs)
    element(tris,'p',' '.join(str(i) for tri in triangles for index in tri for i in [index]*3))
    scene=element(element(root,'library_visual_scenes'),'visual_scene',id='Scene',name='Scene')
    element(element(scene,'node',id='house',name='house',type='NODE'),'instance_geometry',url='#house-mesh')
    element(element(root,'scene'),'instance_visual_scene',url='#Scene')
    ET.indent(root,space='  ')
    dae=ET.tostring(root,encoding='utf-8',xml_declaration=True)+b'\n'
    # 64x16 nearest color blocks; no external texture or image editing input.
    def chunk(kind, data):
        return struct.pack('>I',len(data))+kind+data+struct.pack('>I',zlib.crc32(kind+data)&0xffffffff)
    row=b''.join(bytes(colors[x//16]) for x in range(64))
    png=b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',64,16,8,6,0,0,0))+chunk(b'IDAT',zlib.compress((b'\0'+row)*16,9))+chunk(b'IEND',b'')
    metrics={'vertices':len(positions),'triangles':len(triangles),'bounds_min':[min(p[i] for p in positions) for i in range(3)],'bounds_max':[max(p[i] for p in positions) for i in range(3)],'up_axis':'Y_UP','meters_per_unit':1,'uv_sets':1,'texture_size':[64,16],'bones':0,'animations':0}
    return dae,png,metrics


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true',help='Rebuild in memory and compare without writing')
    args=parser.parse_args()
    repo=Path(__file__).resolve().parents[2]
    source=repo/'assets/epoch-rts/t10-house/house.json'
    dae,png,metrics=export(json.loads(source.read_text()))
    mod=repo/'binaries/data/mods/epoch_rts'
    outputs={mod/'art/meshes/structural/epoch_rts/t10_house.dae':dae,mod/'art/textures/skins/structural/epoch_rts/t10_house.png':png}
    for path,data in outputs.items():
        if args.check:
            if not path.is_file() or path.read_bytes()!=data:
                raise SystemExit('Generated output mismatch: '+str(path.relative_to(repo)))
        else:
            path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
    print(json.dumps({'mode':'check' if args.check else 'export','metrics':metrics,'outputs':{str(p.relative_to(repo)):hashlib.sha256(b).hexdigest() for p,b in outputs.items()}},indent=2))


if __name__=='__main__':
    main()
