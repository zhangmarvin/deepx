import numpy as np
from base import BaseTest

from deepx.nn import Vector, Full
from deepx.node import ShapeException

class TestGraph(BaseTest):

    def test_graph_basic(self):
        np.random.seed(0)
        net1 = Vector(10) >> Full(10)

        np.random.seed(0)
        net2 = Vector(10).chain(Full(10))

        self.assertEqual(net1, net2)

    def test_graph_basic2(self):
        np.random.seed(0)
        net1 = Vector(10) >> Full(10)

        np.random.seed(0)
        net2 = Vector(10).chain(Full(20))

        self.assertNotEqual(net1, net2)

    def test_shape_inference(self):
        part1 = Full(100)
        part2 = Full(20)

        self.assertEqual(part1.shape, (None, 100))
        self.assertEqual(part2.shape, (None, 20))

        part1.chain(part2)

        self.assertEqual(part1.shape, (None, 100))
        self.assertEqual(part2.shape, (100, 20))

    def test_shape_inference2(self):
        part1 = Full(10, 100)
        part2 = Full(100, 20)

        self.assertEqual(part1.shape, (10, 100))
        self.assertEqual(part2.shape, (100, 20))

        part1.chain(part2)

        self.assertEqual(part1.shape, (10, 100))
        self.assertEqual(part2.shape, (100, 20))

    def test_bad_shape(self):
        part1 = Full(10, 100)
        part2 = Full(90, 20)

        with self.assertRaises(ShapeException):
            part1.chain(part2)

    def test_bad_shape2(self):
        part1 = Full(100)
        part2 = Full(20)

        self.assertEqual(part1.shape, (None, 100))
        self.assertEqual(part2.shape, (None, 20))

        part1.chain(part2)

        self.assertEqual(part1.shape, (None, 100))
        self.assertEqual(part2.shape, (100, 20))

        part3 = Full(100)
        part2.chain(part3)

        part4 = Full(90)
        with self.assertRaises(ShapeException):
            part4.chain(part3)

    def test_shape_elementwise(self):
        part1 = Full()
        part2 = Full(20)

        self.assertEqual(part1.shape, (None, None))
        self.assertEqual(part2.shape, (None, 20))

        part2.chain(part1)

        self.assertEqual(part1.shape, (20, 20))
        self.assertEqual(part2.shape, (None, 20))

    def test_shape_elementwise2(self):
        part1 = Full(20)
        part2 = Full()
        part3 = Full(30, 40)

        self.assertEqual(part1.shape, (None, 20))
        self.assertEqual(part2.shape, (None, None))
        self.assertEqual(part3.shape, (30, 40))

        part4 = part1.chain(part2)

        self.assertEqual(part1.shape, (None, 20))
        self.assertEqual(part2.shape, (20, 20))
        self.assertEqual(part4.shape, (None, 20))

        with self.assertRaises(ShapeException):
            part4.chain(part3)