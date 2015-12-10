import unittest


class FmuWrapperTestCase(unittest.TestCase):

    def setUp(self):
        pass
        
    def tearDown(self):
        pass
        
    def test_FmuWrapper(self):
        prob = Problem()
        root = prob.root = Group()
        # excelFile = r"excel_wrapper_test.xlsx"
        # xmlFile = r"excel_wrapper_test.xml"
        # jsonFile = r"testjson_1.json"
        # root.add('ew', ExcelWrapper(excelFile, jsonFile,True),promotes=['*'])
        # prob.setup()
        # prob.run()
        #
        # self.assertEqual((2.1* float(prob['x'])),prob['y'],"Excel Wrapper failed for FLoat values")
        # self.assertEqual((bool(prob['b'])),prob['bout'],"Excel Wrapper failed for Boolean Values")
        # self.assertEqual(prob['s'].lower(),prob['sout'],"Excel Wrapper failed for String values")
        # self.assertEqual(float(prob['sheet1_in'])+100,prob['sheet2_out'],"Excel wrapper fails in multiple sheets")





        
if __name__ == "__main__":
    unittest.main()
