import unittest
import os.path
from openmdao.api import Problem, Group, IndepVarComp
from fmu_wrapper.fmu_wrapper import FmuWrapper

_this_dir = os.path.dirname(os.path.abspath(__file__))


class FmuWrapperTestCase(unittest.TestCase):
    def test_FmuWrapper(self):
        prob = Problem()
        root = prob.root = Group()
        root.add('fmu', FmuWrapper(os.path.join(_this_dir, 'bouncingBall.fmu')), promotes=['*'])
        root.add('c', IndepVarComp('nine', 9.0))
        root.add('final_time', IndepVarComp('ten', 10))
        root.connect('final_time.ten', 'final_time')
        root.connect('c.nine', 'der_v__initial_value')
        root.connect('c.nine', 'e_initial_value')
        root.connect('c.nine', 'g_initial_value')
        root.connect('c.nine', 'h_initial_value')
        root.connect('c.nine', 'v_initial_value')
        root.connect('c.nine', 'der_h__initial_value')
        prob.setup()
        prob.run()
        self.assertAlmostEqual(0.53169023, prob['h'])


if __name__ == "__main__":
    unittest.main()
