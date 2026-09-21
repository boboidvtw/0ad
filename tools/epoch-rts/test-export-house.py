#!/usr/bin/env python3
"""Purpose: T10 exporter geometry and editable-parameter regressions. Created: 2026-09-21.
SPDX-License-Identifier: GPL-2.0-or-later
"""
import copy
import importlib.util
import json
import math
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

spec = importlib.util.spec_from_file_location('house_exporter',Path(__file__).with_name('export-house.py'))
exporter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(exporter)
SOURCE=Path(__file__).resolve().parents[2]/'assets/epoch-rts/t10-house/house.json'


class ExportHouseTests(unittest.TestCase):
    def setUp(self):
        self.source=json.loads(SOURCE.read_text())

    def test_triangle_indices_normals_and_bounds(self):
        dae,_,metrics=exporter.export(self.source)
        root=ET.fromstring(dae);ns={'c':exporter.NS}
        positions=list(map(float,root.find('.//c:float_array[@id="positions-array"]',ns).text.split()))
        normals=list(map(float,root.find('.//c:float_array[@id="normals-array"]',ns).text.split()))
        indices=list(map(int,root.find('.//c:triangles/c:p',ns).text.split()))
        self.assertEqual(len(indices),metrics['triangles']*9)
        for start in range(0,len(indices),9):
            corners=[positions[i*3:i*3+3] for i in indices[start:start+9:3]]
            self.assertTrue(all(len(p)==3 for p in corners))
            a,b,c=corners
            u=[b[i]-a[i] for i in range(3)];v=[c[i]-a[i] for i in range(3)]
            cross=[u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]]
            length=math.sqrt(sum(x*x for x in cross));self.assertGreater(length,0)
            for i in indices[start+1:start+9:3]:
                normal=normals[i*3:i*3+3]
                self.assertAlmostEqual(sum(x*y for x,y in zip(cross,normal))/length,1,places=6)
        self.assertEqual(metrics['bounds_min'],[-5.5,0,-4.5])
        self.assertEqual(metrics['bounds_max'],[5.5,6,4.5])
        self.assertEqual(root.find('c:asset/c:unit',ns).get('meter'),'1')
        self.assertEqual(root.find('c:asset/c:up_axis',ns).text,'Y_UP')

    def test_small_house_door_stays_below_roof(self):
        self.source.update(width=1,depth=1,wall_height=0.1,roof_height=0.2,roof_overhang=0.1)
        _,_,metrics=exporter.export(self.source)
        self.assertAlmostEqual(metrics['bounds_max'][1],0.3)
        self.assertEqual(metrics['bounds_min'][0],-0.6)
        self.assertEqual(metrics['bounds_max'][0],0.6)

    def test_invalid_parameters_rejected(self):
        for key,value in [('width',True),('depth',0),('wall_height',-1),('roof_height',float('nan')),('roof_overhang',100)]:
            with self.subTest(key=key,value=value):
                config=copy.deepcopy(self.source);config[key]=value
                with self.assertRaises(ValueError): exporter.export(config)
        self.source['palette']['wall'][0]=300
        with self.assertRaises(ValueError): exporter.export(self.source)

    def test_deterministic_output(self):
        self.assertEqual(exporter.export(self.source),exporter.export(self.source))


if __name__=='__main__':
    unittest.main()
