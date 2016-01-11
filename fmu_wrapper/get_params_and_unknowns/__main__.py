from __future__ import print_function
import sys
import json
from fmu_wrapper.fmu_wrapper import FmuWrapper

if __name__ == "__main__":
    fmu_path = sys.argv[1]
    c = FmuWrapper(fmu_path)

    print(json.dumps({'params': c._init_params_dict, 'unknowns': c._init_unknowns_dict}))
