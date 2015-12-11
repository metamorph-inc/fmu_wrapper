from __future__ import print_function

import matplotlib

matplotlib.use('Agg')
from openmdao.api import Component
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

        self.param_name_map_mdao_to_fmu = dict()
        self.param_name_map_fmu_to_mdao = dict()
        self.output_name_map_fmu_to_mdao = dict()
        self.output_name_map_mdao_to_fmu = dict()

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

            is_param = False
            is_output = False
            if causality == 0:
                is_param = True
            elif causality == 1:
                is_output = True
            else:
                # Causality 2 (INTERNAL) or 3 (NONE)
                is_param = True
                is_output = True

            if is_param:
                if is_output:
                    # Need a unique name to avoid collision
                    pname = variable_safe_name + "_initial_value"
                else:
                    pname = variable_safe_name

                self.param_name_map_mdao_to_fmu[pname] = variable_name
                self.param_name_map_fmu_to_mdao[variable_name] = pname

                self.add_param(pname, val=nom)
                _debug("param:", variable_safe_name)

            if is_output:
                self.output_name_map_mdao_to_fmu[variable_safe_name] = variable_name
                self.output_name_map_fmu_to_mdao[variable_name] = variable_safe_name

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
                param_fmu_name = self.param_name_map_mdao_to_fmu[param_name]
                fmu_model.set(param_fmu_name, param_value)

        res = fmu_model.simulate(final_time=final_time)

        for fmi_out_name, index in res.result_data.name_lookup.iteritems():
            if fmi_out_name not in self.output_name_map_fmu_to_mdao:
                # We aren't tracking this. Move on.
                continue

            mdao_out_name = self.output_name_map_fmu_to_mdao[fmi_out_name]
            unknowns[mdao_out_name] = res.final(fmi_out_name)


    def jacobian(self, params, unknowns, resids):
        raise Exception('unsupported')


if __name__ == "__main__":
    fmu_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test/bouncingBall.fmu')
    c = FmuWrapper(fmu_path)

    _debug(json.dumps({'params': c._params_dict, 'unknowns': c._unknowns_dict}))

    unknowns = dict()
    c.solve_nonlinear({'h_initial_value': 12.0, 'final_time': 5}, unknowns, None)
    _debug(json.dumps(unknowns, indent=2))
