import unittest
from unittest import TestCase
from unittest import mock
from memoryManager import MemoryManager


class TestMemoryManager(TestCase):

    def test_init(self):
        mm = MemoryManager(128)
        self.assertEqual(len(mm.listOfBlocks), 8)
        self.assertEqual(mm.listOfBlocks, [[], [], [], [], [], [], [], [(0, 127)]])
        self.assertEqual(len(mm.listOfNames), 0)
        self.assertEqual(mm.memoryBlocks, 128)

    def test_wrong_init(self):
        with self.assertRaises(ValueError):
            mm = MemoryManager(-1)

    def test_wrong_init2(self):
        with self.assertRaises(ValueError):
            mm = MemoryManager(10)

    def test_allocate(self):
        mm = MemoryManager(128)
        test_cases = [
            {"name": "Block 1", "size": 32, "expected_list": [[], [], [], [], [], [(32, 63)], [(64, 127)], []],
             "expected_list_names": True},
            {"name": "Block 2", "size": 7, "expected_list": [[], [], [], [(40, 47)], [(48, 63)], [], [(64, 127)], []],
             "expected_list_names": True},
            {"name": "Block 3", "size": 64, "expected_list": [[], [], [], [(40, 47)], [(48, 63)], [], [], []],
             "expected_list_names": True},
            {"name": "Block 4", "size": 56, "expected_list": [[], [], [], [(40, 47)], [(48, 63)], [], [], []],
             "expected_list_names": False},
            {"name": "Block Wrong size", "size": -1, "expected_list": [[], [], [], [(40, 47)], [(48, 63)], [], [], []],
             "expected_list_names": False},
        ]
        for test in test_cases:
            mm.allocate(test["name"], test["size"])
            self.assertEqual(mm.listOfBlocks, test["expected_list"])
            self.assertEqual(test["name"] in mm.listOfNames, test["expected_list_names"])

    def test_free(self):
        mm = MemoryManager(128)
        # Stage of allocation
        test_cases_allocation = [
            {"name": "Block 1", "size": 16, "expected_list": [[], [], [], [], [(16, 31)], [(32, 63)], [(64, 127)], []],
             "expected_list_names": True},
            {"name": "Block 2", "size": 16, "expected_list": [[], [], [], [], [], [(32, 63)], [(64, 127)], []],
             "expected_list_names": True},
            {"name": "Block 3", "size": 16, "expected_list": [[], [], [], [], [(48, 63)], [], [(64, 127)], []],
             "expected_list_names": True},
            {"name": "Block 4", "size": 16, "expected_list": [[], [], [], [], [], [], [(64, 127)], []],
             "expected_list_names": True},
        ]

        for test in test_cases_allocation:
            mm.allocate(test["name"], test["size"])
            self.assertEqual(mm.listOfBlocks, test["expected_list"])
            self.assertEqual(test["name"] in mm.listOfNames, test["expected_list_names"])

        # Stage of freeing
        test_cases_free = [
            {"name": "Block 1", "expected_list": [[], [], [], [], [(0, 15)], [], [(64, 127)], []],
             "expected_list_names": False},
            {"name": "Block No Allocate", "expected_list": [[], [], [], [], [(0, 15)], [], [(64, 127)], []],
             "expected_list_names": False},
            {"name": "Block 3", "expected_list": [[], [], [], [], [(0, 15), (32, 47)], [], [(64, 127)], []],
             "expected_list_names": False},
            {"name": "Block 2", "expected_list": [[], [], [], [], [(32, 47)], [(0, 31)], [(64, 127)], []],
             "expected_list_names": False},
        ]
        for test in test_cases_free:
            mm.free(test["name"])
            self.assertEqual(mm.listOfBlocks, test["expected_list"])
            self.assertEqual(test["name"] in mm.listOfNames, test["expected_list_names"])

    def test_disply(self):
        mm = MemoryManager(128)
        mm.display()
        self.assertEqual(len(mm.listOfBlocks), 8)
        self.assertEqual(mm.listOfBlocks, [[], [], [], [], [], [], [], [(0, 127)]])
        self.assertEqual(len(mm.listOfNames), 0)
        self.assertEqual(mm.memoryBlocks, 128)

    def test_begin_program(self):
        mm5 = MemoryManager(128)
        mm5.allocate("Block_1", 32)
        test_cases_wrong_input = ["no action", "reserve no param", "reserve Block_1 16", "free no param",
                                  "free 2", "display", "exit"]

        with mock.patch('builtins.input', side_effect=test_cases_wrong_input):
            mm5.begin_program()
            self.assertEqual(len(mm5.listOfBlocks), 8)
            self.assertEqual(mm5.listOfBlocks, [[], [], [], [], [], [(32, 63)], [(64, 127)], []])
            self.assertEqual(len(mm5.listOfNames), 1)
            self.assertEqual(mm5.memoryBlocks, 128)


if __name__ == '__main__':
    unittest.main()
