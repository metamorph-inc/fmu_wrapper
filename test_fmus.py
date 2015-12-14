import os
import os.path
import fnmatch
import json
import matplotlib

matplotlib.use('Agg')
from pyfmi import load_fmu


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--fmudir", help="Directory of FMUs to test")
    parser.add_argument("--xml", action='store_true')
    parser.add_argument("--verbose", action='store_true')
    args = parser.parse_args()
    fmudir = args.fmudir

    # Recursively fetch all FMUs from the path given
    # Use the FMU wrapper on each one
    # Use solve_nonlinear to test each one
    # Give the results

    matches = []
    for root, dirnames, filenames in os.walk(fmudir):
        for filename in fnmatch.filter(filenames, '*.fmu'):
            matches.append(os.path.join(root, filename))

    print (json.dumps(matches, indent=2))

    report = []
    for fmu in matches:
        status = "OK"

        try:
            fmu_model = load_fmu(fmu)
            variables = fmu_model.get_model_variables()
            try:
                fmu_model.simulate(final_time=0)
            except:
                status = "FAILED SIM"
        except:
            status = "FAILED TO LOAD"

        report.append(fmu + ' ' + status)

    print '\n'.join(report)
