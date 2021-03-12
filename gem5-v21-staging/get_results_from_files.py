import argparse
import os
import json

def get_info_path_iterator(path):
    for root, _, files in os.walk(path):
        for f in files:
            if not f == "info.json":
                continue
            dirname = root
            filename = f
            yield dirname, filename

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Gathering boot-exit results')
    parser.add_argument('--input', type=str, help="Path to the results folder")
    parser.add_argument('--output', type=str, help="Path to the file containing parsed results", default="./results.csv")
    args = parser.parse_args()

    input_path = args.input
    output_path = args.output
    #boot-exit/5.4.49/simple/8/MOESI_CMP_directory/init
    folder_structure = ['kernel', 'cpu_type', 'num_cpus', 'mem_sys', 'boot_type']
    with open(output_path, 'w') as f:
        f.write('string, status, running, kill_reason, return_code\n')
        for dirname, filename in get_info_path_iterator(input_path):
            result = None
            filepath = os.path.join(dirname, filename)
            with open(filepath, 'r') as g:
                result = json.load(g)
            if not result:
                continue
            try:            
                to_write = "{},{},{},{},{}\n".format(result['string'], result['status'], result['running'], result['kill_reason'], result['return_code'])
                f.write(to_write)
            except KeyError:
                print("warn: '{}' does not contain result".format(filepath))
        
