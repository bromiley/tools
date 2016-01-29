########################
#MongoDB 2.x Log Timeframe Parser
# Created by 505Forensics (http://www.505forensics.com)
#
# Usage: Utilize this script to create timeframes from a single MongoDB log file
#
# Output: Script will output in CSV to a file named <log_name>_timeframes.csv by default. The '-o' option will allow you to change the name.
#
#######################

import argparse
import csv

def parse_timeframes(input):
    connections = {}
    with open(input) as infile:
        for line in infile:
            # Look for/parse lines of an initiated connection
            if 'connection accepted' in line:
                connection_number = line.split()[6].strip('#')
                ip_port = line.split()[5]
                start_time = line.split()[0]
                connections[connection_number] = [start_time, ip_port.split(':')[0], ip_port.split(':')[1]]

            # Look for/parse lines that end a connection
            if 'end connection' in line:
                end_time = line.split()[0]
                connection_number = line.split()[1].strip('conn[]')
                ip_port = line.split()[4]
                if connection_number in connections:
                    connections[connection_number].append(end_time)
                else:
                    # Handle lines that do not have an initiated connection
                    connections[connection_number] = ['N/A', ip_port.split(':')[0], ip_port.split(':')[1], end_time]
    return connections

def outputResults(output,output_file):
    with open(output_file,'w') as csvfile:
        csv_out = csv.writer(csvfile)
        csv_out.writerow(['Connection ID', 'Start Time', 'End Time', 'IP Address', 'Port'])
        for k, v in output.iteritems():
            try:
                if v[3]:
                    csv_out.writerow([k,v[0],v[3],v[1],v[2]])
            except IndexError:
                csv_out.writerow([k,v[0],'N/A',v[1],v[2]])
    print "- Total {} timeframes found".format(len(output))

def main():
    parser = argparse.ArgumentParser(description='Parse connection timeframes from MongoDB 2.x logs')
    group = parser.add_argument_group()
    group.add_argument('-o','--out',metavar='FILE',help='File to output to [default is <log_name>_timeframes.csv]')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-l','--log',metavar='LOG',help="Log to parse")

    args = parser.parse_args()

    if args.log:
        try:
            print "- Parsing timeframes from log file {}...".format(args.log)
            # Get output dictionary from parse_timeframes
            output = parse_timeframes(args.log)
            if not output:
                print "- No timeframes found..."
            else:
                # Check for '-o' argument to change file name
                if not args.out:
                    output_file_name = args.log + "_timeframes.csv"
                else:
                    output_file_name = args.out
                # Pass output and file name to output function
                outputResults(output,output_file_name)

                # Final line of confirmation
                print "- Output written to {}".format(output_file_name)

        except IOError:
            print "- Error parsing file {}...".format(args.log)

if __name__ == "__main__":
    main()