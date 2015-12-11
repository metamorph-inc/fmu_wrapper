from __future__ import print_function

import matplotlib

matplotlib.use('Agg')
from openmdao.api import Component
import sys
import os
import os.path
import json
from pyfmi import load_fmu


def _debug(*args):
    print(*args)
    pass


class FmuWrapper(Component):
    """ An FMU Wrapper """

    DEFAULT_FINAL_TIME = 10

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

        # Add 'final_time' as a parameter
        self.add_param("final_time", val=self.DEFAULT_FINAL_TIME)
        _debug("param:", "final_time")

        # Add parameters and unknowns discovered from FMU
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

        final_time = self._params_dict['final_time']['val']
        for param_name, param_value in params.iteritems():
            if param_name is "final_time":
                final_time = float(str(param_value))
            else:
                param_fmu_name = self.variable_name_map_mdao_to_fmu[param_name]
                fmu_model.set(param_fmu_name, param_value)

        res = fmu_model.simulate(final_time=final_time)

        for fmi_out_name, index in res.result_data.name_lookup.iteritems():
            if fmi_out_name not in self.variable_name_map_fmu_to_mdao:
                # We aren't tracking this. Move on.
                continue

            mdao_out_name = self.variable_name_map_fmu_to_mdao[fmi_out_name]
            unknowns[mdao_out_name] = res.final(fmi_out_name)


    def jacobian(self, params, unknowns, resids):
        raise Exception('unsupported')


if __name__ == "__main__":
    if len(sys.argv) == 2:
        fmu_path = sys.argv[1]
    else:
        fmu_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test/bouncingBall.fmu')
    c = FmuWrapper(fmu_path)

    _debug(json.dumps({'params': c._params_dict, 'unknowns': c._unknowns_dict}))

    unknowns = dict()
    c.solve_nonlinear({'h': 22.0}, unknowns, None)
    _debug(json.dumps(unknowns, indent=2))
