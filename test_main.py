from unittest import TestCase
from main import connect
from main import move_forward
from main import move_sideways
import asyncio
import sys


class TestMoveForward(TestCase):
    def test_move_forward_1(self):
        result = move_forward('N', 0, 1)
        self.assertEqual(result, (1, 1))

    def test_move_forward_2(self):
        result = move_forward('N', 1, 1)
        self.assertEqual(result, (2, 1))

    def test_move_forward_3(self):
        result = move_forward('N', 2, 1)
        self.assertEqual(result, (3, 1))

    def test_move_forward_4(self):
        result = move_forward('N', 3, 1)
        self.assertEqual(result, (4, 1))

    def test_move_forward_5(self):
        result = move_forward('N', 1, 4)
        self.assertEqual(result, (2, 4))

    def test_move_forward_6(self):
        result = move_forward('S', 1, 4)
        self.assertEqual(result, (0, 4))

    def test_move_forward_7(self):
        result = move_forward('S', 5, 7)
        self.assertEqual(result, (4, 7))

    def test_move_forward_8(self):
        result = move_forward('S', 3, 7)
        self.assertEqual(result, (2, 7))


class TestMoveSideways(TestCase):
    def test_move_sideways_1(self):
        result = move_sideways(0, 1)
        self.assertEqual(result, (0, 2))

    def test_move_sideways_2(self):
        result = move_sideways(1, 1)
        self.assertEqual(result, (1, 2))

    def test_move_sideways_3(self):
        result = move_sideways(2, 1)
        self.assertEqual(result, (2, 2))

    def test_move_sideways_4(self):
        result = move_sideways(3, 1)
        self.assertEqual(result, (3, 2))

    def test_move_sideways_5(self):
        result = move_sideways(1, 4)
        self.assertEqual(result, (1, 5))

    def test_move_sideways_6(self):
        result = move_sideways(1, 4)
        self.assertEqual(result, (1, 5))

    def test_move_sideways_7(self):
        result = move_sideways(5, 7)
        self.assertEqual(result, (5, 8))

    def test_move_sideways_8(self):
        result = move_sideways(3, 7)
        self.assertEqual(result, (3, 8))


if __name__ == '__main__':
    if len(sys.argv) >= 2:
        auth_token = sys.argv[1]
        asyncio.get_event_loop().run_until_complete(connect(auth_token))
    else:
        print('Please provide your auth_token.')
