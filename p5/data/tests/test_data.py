import unittest
from p5.data import clear_storage, get_item, remove_item, set_item


class TestStorage(unittest.TestCase):
    def test_set_item(self):
        set_item('test', 'p5py')
        self.assertEqual(get_item('test'), 'p5py')

    def test_get_item(self):
        set_item('test', 'p5py')
        self.assertEqual(get_item('test'), 'p5py')

    def test_remove_item(self):
        set_item('test1', 'p5py')
        set_item('test2', 'p5py1')
        remove_item('test1')
        self.assertEqual(get_item('test1'), None)
        self.assertEqual(get_item('test2'), 'p5py1')

    def test_clear_storage(self):
        set_item('test1', 'p1')
        set_item('test2', 'p2')
        clear_storage()
        self.assertEqual(get_item('test1'), None)
        self.assertEqual(get_item('test2'), None)


if __name__ == "__main__":
    unittest.main()
