import sys
import unittest
sys.path.append("src")
sys.path.append(r'..\src')
import gol


class Tests(unittest.TestCase):
    def test_test(self):
        self.assertEqual(True,True)
    def test_init(self):
        testgol = gol.GolMain(5, [])
        self.assertEqual(testgol.testvar,1)
    def test_init_nontrivial(self):
        size = 3
        testgol = gol.GolMain(size, [(1,1)])
        result = [0 for i in range(size)]
        result[0] = '000'
        result[1] = '010'
        result[2] = '000'
        for i in range(size):
            result[i] = [eval(j) for j in result[i]]
        self.assertEqual(testgol.field,result)
    def test_running_dead(self):
        size = 3
        testgol = gol.GolMain(size, [(1,1)])
        self.assertEqual(testgol.run_game(10),-1)  
    def test_running_glider(self):
        size = 100
        testgol = gol.GolMain(size, [(50,51),(50,50),(50,49),(49,49),(48,50)])
        self.assertEqual(testgol.run_game(10),1)
    def test_running_glider_gun(self):
        testgol = gol.GolMain(-1, 'testi.txt', 'file')
        self.assertEqual(testgol.run_game(100),1)
    def test_pygame(self):
        testgol = gol.GolMain(-1, 'testi.txt', 'file', renderer='pygame')
        self.assertEqual(testgol.run_game(-1),1)

if __name__ == '__main__':
    unittest.main()
