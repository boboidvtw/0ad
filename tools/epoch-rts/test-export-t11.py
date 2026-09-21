#!/usr/bin/env python3
"""Purpose: T11 rig, animation and reproducibility contract tests. Created: 2026-09-21.
SPDX-License-Identifier: GPL-2.0-or-later
"""
import importlib.util
import json
import math
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

loader=importlib.util.spec_from_file_location('exporter',Path(__file__).with_name('export-t11.py'))
exporter=importlib.util.module_from_spec(loader);loader.loader.exec_module(exporter)
N={'c':exporter.NS}

class ExportTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.spec=json.loads((exporter.REPO/'assets/epoch-rts/t11-slice/slice.json').read_text())
        cls.outputs,cls.metrics=exporter.build(cls.spec)

    def test_outputs_match_committed_worktree(self):
        self.assertEqual(self.outputs,exporter.build(self.spec)[0])
        for path,data in self.outputs.items():
            self.assertEqual(data,(exporter.MOD/path).read_bytes(),path)

    def test_skin_weights_and_bind_pose(self):
        for role in ['worker','soldier']:
            root=ET.fromstring(self.outputs['art/meshes/skeletal/epoch_rts/t11_'+role+'.dae'])
            count=self.metrics[role]['vertices'];weights=root.find('.//c:vertex_weights',N)
            self.assertEqual(int(weights.attrib['count']),count)
            self.assertEqual(list(map(int,weights.find('c:vcount',N).text.split())),[1]*count)
            pairs=list(map(int,weights.find('c:v',N).text.split()))
            self.assertEqual(len(pairs),2*count)
            self.assertTrue(all(0<=b<7 for b in pairs[::2]))
            self.assertEqual(pairs[1::2],[0]*count)
            binds=list(map(float,root.find('.//c:float_array[@id="binds-array"]',N).text.split()))
            for i,b in enumerate(self.spec['bones']):
                self.assertEqual(binds[16*i+3],-b[1]);self.assertEqual(binds[16*i+7],-b[2]);self.assertEqual(binds[16*i+11],-b[3])

    def test_triangles_and_normals(self):
        for role in ['worker','soldier']:
            root=ET.fromstring(self.outputs['art/meshes/skeletal/epoch_rts/t11_'+role+'.dae'])
            arr=lambda name:list(map(float,root.find('.//c:float_array[@id="'+name+'-array"]',N).text.split()))
            pos,norm=arr('positions'),arr('normals')
            self.assertTrue(all(math.isfinite(x) for x in pos+norm))
            for i in range(0,len(norm),3):self.assertAlmostEqual(sum(v*v for v in norm[i:i+3]),1,places=6)
            tri=root.find('.//c:triangles',N);indices=list(map(int,tri.find('c:p',N).text.split()))
            self.assertEqual(len(indices),int(tri.attrib['count'])*9)
            self.assertTrue(all(0<=i<len(pos)//3 for i in indices))
            for j in range(0,len(indices),9):
                points=[pos[indices[j+k]*3:indices[j+k]*3+3] for k in [0,3,6]]
                a,b,c=points;u=[b[i]-a[i] for i in range(3)];v=[c[i]-a[i] for i in range(3)]
                area=[u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]]
                self.assertGreater(sum(x*x for x in area),1e-10)

    def test_clips_share_rig_and_animate(self):
        for clip,settings in self.spec['clips'].items():
            root=ET.fromstring(self.outputs['art/animation/epoch_rts/t11_'+clip+'.dae'])
            joints=root.findall('.//c:node[@type="JOINT"]',N)
            self.assertEqual([j.attrib['name'] for j in joints],[b[0] for b in self.spec['bones']])
            self.assertEqual(len(root.findall('.//c:channel',N)),7)
            self.assertGreater(settings['duration'],0)
            self.assertTrue(any(len(set(v))>1 for v in settings['angles'].values()))
            for name,angles in settings['angles'].items():
                self.assertEqual(len(angles),5)
                if clip!='death':self.assertEqual(angles[0],angles[-1])
            if clip=='death':self.assertEqual(settings['angles']['epoch_root'][-1],90)

    def test_actor_animation_and_icon_paths_resolve(self):
        for role in ['worker','soldier']:
            actor=ET.parse(exporter.MOD/f'art/actors/units/epoch_rts/t11_{role}.xml')
            names={a.attrib['name'].lower() for a in actor.findall('.//animation')}
            self.assertTrue({'idle','walk','run','attack_melee','death'}<=names)
            if role=='worker':self.assertTrue({'gather_tree','build'}<=names)
            for a in actor.findall('.//animation'):self.assertTrue((exporter.MOD/'art/animation'/a.attrib['file']).is_file())
            icon=ET.parse(exporter.MOD/f'simulation/templates/units/epoch_rts/t11_{role}.xml').findtext('.//Icon')
            self.assertTrue((exporter.MOD/'art/textures/ui/session/portraits'/icon).is_file())

if __name__=='__main__':unittest.main(verbosity=2)
