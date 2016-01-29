########################
#MongoDB 2.x Log Timeframe Parser
# Created by 505Forensics (http://www.505forensics.com)
#
# Usage: Utilize this script to collect information on session activity from a single MongoDB log file
#
# Output: Script will output in CSV to a file named <log_name>_session_stats.csv by default. The '-o' option will allow you to change the name.
#
#######################

import argparse
import csv

def parse_sessions(input):
    # Final dictionary returned
    collections = {}

    with open(input) as infile:
        for line in infile:
            try:
                action = line.split()[2]
                # Only action item is currently query. Need to expand to other mongo actions
                if action == 'query':
                    connection_number = line.split()[1].strip('conn[]')
                    collection = line.split()[3]
                    # Test to see if connection ID already has an entry. If so, don't overwrite. If not, create.
                    try:
                        if collection in collections[connection_number]:
                            pass
                        else:
                            collections[connection_number].append(collection)
                    except KeyError:
                        collections[connection_number] = [collection]

            except IndexError:
                pass

        return collections

def outputResults(output,output_file):
    # CSV output is currently default
    with open(output_file,'w') as csvfile:
        csv_out = csv.writer(csvfile)
        csv_out.writerow(['Connection ID', 'Collections Accessed'])
        for k, v in output.iteritems():
            csv_out.writerow([k, (",").join(output[k])])

    print "- Total {} sessions written".format(len(output))

def main():
    parser = argparse.ArgumentParser(description='Parse session statistics from MongoDB 2.x logs')
    group = parser.add_argument_group()
    group.add_argument('-o','--out',metavar='FILE',help='File to output to [default is <log_name>_session_stats.csv]')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-l','--log',metavar='LOG',help='Log to Parse')

    args = parser.parse_args()

    if args.log:
        try:
            print "- Parsing session information from log file {}...".format(args.log)
            output = parse_sessions(args.log)
            if not output:
                print "- No session information was found..."
            else:
                if not args.out:
                    output_file_name = args.log + "_session_stats.csv"
                else:
                    output_file_name = args.out
                outputResults(output,output_file_name)
                print "- Output written to {}...".format(output_file_name)
        except IOError:
            print "- Error parsing file {}...".format(args.log)

if __name__ == "__main__":
    main()