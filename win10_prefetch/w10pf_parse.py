########################
# Windows 10 Prefetch Parser
# Created by 505Forensics (http://www.505forensics.com)
#
# Usage: Utilize this script to parse either a single or set of Windows 10 prefetch files
#
# Dependencies: This script requires the installation of libscca (https://github.com/libyal/libscca), and was only tested in a Linux environment
#
# Output: Script will output in CSV to stdout by default.
#
#######################
import argparse
import csv
import sys
import os
import json
# Try importing pyscca; fail if it doesn't import
try:
    import pyscca #Import pyscca, necessary from libscca
except ImportError:
    print "Please install libscca with Python bindings"

output = {}

# Parse individual file. Output is placed in 'output' dictionary
def parse_file(pf_file,volume_information):
    try:
        scca = pyscca.open(pf_file)
        last_run_times = []
        for x in range(8):
            if scca.get_last_run_time_as_integer(x) > 0:
                last_run_times.append(scca.get_last_run_time(x).strftime("%Y-%m-%d %H:%M:%S")) #str conversion utilized to change from datetime into human-readable
            else:
                last_run_times.append('N/A')
        output[str(scca.executable_filename)] = [str(scca.run_count), format(scca.prefetch_hash, 'x').upper(), last_run_times]

        if volume_information:
            output[str(scca.executable_filename)].append(scca.number_of_volumes)
            volumes = []
            for i in range(scca.number_of_volumes):
                volume = [str(scca.get_volume_information(i).device_path), scca.get_volume_information(i).creation_time.strftime("%Y-%m-%d %H:%M:%S"), format(scca.get_volume_information(i).serial_number,'x').upper()]
                volumes.append(volume)

            output[str(scca.executable_filename)].append(volumes)
        return output
    except IOError:
        pass

# Parse an entire directory of Prefetch files. Note that it searches based on .pf extension
def parse_dir(dir,volume_information):
    for item in os.listdir(dir):
        if item.endswith(".pf"): #Only focus on .pf files
            parse_file(dir+item,volume_information)
        else:
            continue
    return output

def outputResults(output,output_file=None,output_type=None,volume_information=None):
    if output_type:
        for k, v in output.iteritems():
            json_output = {
                'Executable Name' : k,
                'Run Count' : v[0],
                'Prefetch Hash' :  v[1],
            }
            #Let the script iterate through run times for us, instead of just dumping a list
            run_list = {}
            for i in range(8):
                run_list['Run Time {}'.format(i)] = v[2][i]

            json_output['Run Times'] = run_list
            # Logic to include volume information if its requested by the analyst
            if volume_information:
                volume_list = {}
                for i in range(v[3]):
                    volume_info = {
                        'Volume Name' : v[4][i][0],
                        'Creation Time' : v[4][i][1],
                        'Serial Number' : v[4][i][2]
                    }
                    volume_list['Volume {}'.format(i)] = volume_info

                volumes = {
                    'Number of Volumes' : v[3],
                    'Volume Information' : volume_list
                }
                json_output['Volumes'] = volumes

            if output_file:
                with open(output_file,'w') as file:
                    json.dump(json_output,file)
            else:
                print json.dumps(json_output,indent=4,sort_keys=True)

    else:
        if output_file:
            csv_out = csv.writer(file(output_file,'w'))
        else:
            csv_out = csv.writer(sys.stdout)

        headers = ['Executable Name','Run Count','Prefetch Hash']
        for i in range(8): # Loop through numbers to create headers
            headers.append('Last Run Time {}'.format(i))
        # Check to see if we want volume information
        # TODO: Make this section more efficient
        if volume_information:
            # Add in number of volumes header
            headers.append('Number of Volumes')

            # Need to get the max value of the number of volumes, and create our headers accordingly. Note that some files will have less volumes than others, and will have blank cells where appropriate
            volume_count = []
            for k, v in output.iteritems():
                volume_count.append(v[3])
            for i in range(max(volume_count)):
                # Adding in volume-specific headers one-by-one, simply to avoid list formatting in the CSV output
                headers.append(str('Volume {} Name').format(i))
                headers.append(str('Volume {} Creation Time').format(i))
                headers.append(str('Volume {} Serial Number').format(i))

        csv_out.writerow(headers)
        for k, v in output.iteritems():
            row = [k, v[0], v[1]]
            for i in range(8): # Loop through range again to get each sub-value for times
                row.append(v[2][i])
            if volume_information:
                row.append(v[3])
                for i in range(v[3]):
                    #Iterate through each volume information list to include values
                    for j in range(3):
                        row.append(v[4][i][j])
            csv_out.writerow(row)

def main():
    parser = argparse.ArgumentParser(description='Parse Win10 Prefetch files utilizing libscca.')
    # Input Options
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-f','--file',metavar="FILE", help="Single prefetch file")
    group.add_argument('-d','--directory',metavar="DIRECTORY", help="Directory of prefetch files")

    #Output Options
    group = parser.add_argument_group()
    group.add_argument('-o','--output',metavar="OUTPUT",help="Output file [default is stdout]")
    group.add_argument('--json',action='store_true',help="JSON format output")

    #Parsing Option
    group.add_argument('--volumes',action="store_true",help="Include volume information")

    #Parse it!
    args = parser.parse_args()

    if args.file:
        output = parse_file(args.file,args.volumes)

    if args.directory:
        output = parse_dir(args.directory,args.volumes)

    if not output:
        print "No valid prefetch files were found!"
    else:
        outputResults(output,args.output,args.json,args.volumes)
if __name__ == "__main__":
    main()
