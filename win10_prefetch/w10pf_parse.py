########################
# Windows 10 Prefetch Parser
# Created by 505Forensics (http://www.505forensics.com)
#
# Usage: Utilize this script to parse either a single or set of Windows 10 prefetch files
#
# Dependencies: This script requires the installation of libscca (https://github.com/libyal/libscca), and was only tested in a Linux environment
#
# Output: Script will output in CSV to stdout by default. Feel free to redirect to a file of choice
#
#######################
import argparse
import csv
import sys
import os
# Try importing pyscca; fail if it doesn't import
try:
    import pyscca #Import pyscca, necessary from libscca
except ImportError:
    print "Please install libscca with Python bindings"

# Define the dictionary that will become out parsed output
output = {}

# Parse individual file. Output is placed in 'output' dictionary
def parse_file(pf_file):
    try:
        scca = pyscca.open(pf_file)
        last_run_times = []
        for x in range(8):
            if scca.get_last_run_time_as_integer(x) > 0:
                last_run_times.append(scca.get_last_run_time(x).strftime("%Y-%m-%d %H:%M:%S")) #str conversion utilized to change from datetime into human-readable
            else:
                last_run_times.append('N/A')
        output[str(scca.get_executable_filename())] = str(scca.get_run_count()), last_run_times
        return output
    except IOError:
        pass

# Parse an entire directory of Prefetch files. Note that is searches based on .pf extension
def parse_dir(dir):
    for item in os.listdir(dir):
        if item.endswith(".pf"): #Only focus on .pf files
            parse_file(dir+item)
        else:
            continue
    return output

def outputResults(output):
    if bool(output):
        csv_out = csv.writer(sys.stdout)
        csv_out.writerow(['Executable Name','Run Count','Last Run Time 1','Last Run Time 2','Last Run Time 3','Last Run Time 4','Last Run Time 5','Last Run Time 6','Last Run Time 7','Last Run Time 8'])
        for k, v in output.iteritems():
            # Need to fix the following loop; automate the boring stuff :)
            csv_out.writerow([k, v[0], v[1][0], v[1][1], v[1][2], v[1][3], v[1][4], v[1][5], v[1][6], v[1][7]])
    else:
        print "No valid prefetch files were found!"

def main():
    parser = argparse.ArgumentParser(description='Parse Win10 Prefetch files utilizing libscca')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-f','--file',metavar="FILE", help="Single prefetch file")
    group.add_argument('-d','--directory',metavar="DIRECTORY", help="Directory of prefetch files")
    args = parser.parse_args()

    if args.file:
        output = parse_file(args.file)

    if args.directory:
        output = parse_dir(args.directory)

    outputResults(output)

if __name__ == "__main__":
    main()