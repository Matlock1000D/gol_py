import gol
import unittest

class Tests(unittest.TestCase):
    def test_test(self):
        self.assertEqual(True,True)
    def test_init(self):
        testgol = gol.gol_main(5, [])
        self.assertEqual(testgol.testvar,1)
    def test_init_nontrivial(self):
        size = 3
        testgol = gol.gol_main(size, [(1,1)])
        result = [0 for i in range(size)]
        result[0] = '000'
        result[1] = '010'
        result[2] = '000'
        for i in range(size):
            result[i] = [eval(j) for j in result[i]]
        self.assertEqual(testgol.field,result)
    def test_running_dead(self):
        size = 3
        testgol = gol.gol_main(size, [(1,1)])
        self.assertEqual(testgol.run_game(10),-1)
    def test_running_steady(self):
        size = 3
        testgol = gol.gol_main(size, [(1,1),(1,0),(1,2)])
        self.assertEqual(testgol.run_game(10),1)

if __name__ == '__main__':
    unittest.main()