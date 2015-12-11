from __future__ import print_function

from openmdao.api import Component
import os
import os.path
import json
from pyfmi import load_fmu


def _debug(*args):
    # print(*args)
    pass


class FmuWrapper(Component):
    """ An FMU Wrapper """

    def __init__(self, fmuPath):
        super(FmuWrapper, self).__init__()

        self.fmuPath = fmuPath

        data_type_names = ['Real', 'Int', 'Bool', 'String', 'Enumeration']
        variability_names = ['Constant', 'Parameter', 'Discrete', 'Continuous']
        causality_names = ['Input', 'Output', 'Internal', 'None']

        fmu_model = load_fmu(fmuPath)
        self.fmu_model = fmu_model
        variables = fmu_model.get_model_variables()

        self.variable_name_map_mdao_to_fmu = dict()
        self.variable_name_map_fmu_to_mdao = dict()

        for variable_name, v in variables.iteritems():
            description = fmu_model.get_variable_description(variable_name)
            data_type = fmu_model.get_variable_data_type(variable_name)
            min = fmu_model.get_variable_min(variable_name)
            nom = fmu_model.get_variable_nominal(variable_name)
            max = fmu_model.get_variable_max(variable_name)
            variability = fmu_model.get_variable_variability(variable_name)
            causality = fmu_model.get_variable_causality(variable_name)

            _debug(variable_name + ':', description)
            _debug('\tdata_type:', data_type_names[data_type])
            _debug('\tmin/nom/max:', min, nom, max)
            _debug('\tvariability:', variability_names[variability])
            _debug('\tcausality:', causality_names[causality])

            variable_safe_name = variable_name.replace('(', '_').replace(')', '_')
            self.variable_name_map_mdao_to_fmu[variable_safe_name] = variable_name
            self.variable_name_map_fmu_to_mdao[variable_name] = variable_safe_name

            if causality == 0 or variability == 1:
                # It's a parameter
                self.add_param(variable_safe_name, val=nom)
                _debug("param:", variable_safe_name)
            else:
                # It's an output or state variable
                self.add_output(variable_safe_name, val=nom)
                _debug("output:", variable_safe_name)

    def solve_nonlinear(self, params, unknowns, resids):
        fmu_model = self.fmu_model
        # fmu_model.initialize()

        for param_name, param_value in params.iteritems():
            param_fmu_name = self.variable_name_map_mdao_to_fmu[param_name]
            fmu_model.set(param_fmu_name, param_value)

        res = fmu_model.simulate()

        result_dict = dict()

        for output_name, output_val in unknowns.iteritems():
            output_fmu_name = self.variable_name_map_mdao_to_fmu[output_name]
            # output_val = fmu_model

    def jacobian(self, params, unknowns, resids):
        raise Exception('unsupported')


if __name__ == "__main__":
    fmu_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test/bouncingBall.fmu')
    c = FmuWrapper(fmu_path)

    # c.solve_nonlinear({'h': 22.0}, dict(), dict())
    print(json.dumps({'params': c._params_dict, 'unknowns': c._unknowns_dict}))
