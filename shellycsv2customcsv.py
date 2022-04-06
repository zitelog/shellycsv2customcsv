import os, argparse, sys, csv, re
from pathlib import Path
from datetime import datetime



'''shellycsv2customcsv parser, script entry point.'''


if __name__ == '__main__':

    if sys.version_info[0] < 3:
        sys.exit('Python 3 or a more recent version is required.')


    argparse = argparse.ArgumentParser(prog='shellycsv2customcsv', description="Parse the CSV file produced by the shelly device and save the result in shelly_custom.csv")
    argparse.add_argument("shellycsvfile", help="If no path is specified the file will be searched in the current directory")
    argparse.add_argument('--output-path', metavar='', help="output directory, must exist. If no path is specified the file will be saved in the current directory")

    args = argparse.parse_args()


    if not Path(args.shellycsvfile).is_file():
        print (argparse.prog + f": error: argument inputfile: file not exist: '{args.shellycsvfile}'")
        exit()


    if args.output_path is not None and not Path(args.output_path).is_dir():
        print (argparse.prog + f": error: argument output-path: path not exist: '{args.output_path}'")
        exit()


    shellycsvfile = args.shellycsvfile
    customcsv = 'shelly_custom.csv'

    if args.output_path is not None:
        customcsv = args.output_path + '/' + customcsv


    def shelly_lines_2_custom_lines(shelly_lines):

        custom_lines = []

        for line in shelly_lines:

            shelly_date = re.match(r'^([a-zA-Z]{3})\s([a-zA-Z]{3})\s([0-9]{2})\s([0-9]{4})', line)

            if shelly_date is not None:

                shelly_value = re.search(r';([\S\s]*?);', line)
                shelly_date_2_datetime = datetime.strptime(shelly_date.group(0), '%a %b %d %Y')
                custom_date = shelly_date_2_datetime.strftime("%Y-%m-%d")

                custom_lines.append([custom_date, shelly_value.group(1)])
        
        return custom_lines


    with open(shellycsvfile, newline='') as file:

        lines = file.read()

        if 'Time;Values' in lines and 'Consumption' in lines and 'Reversed' in lines:
            shelly_consumption_lines = re.search(r'^Consumption([\S\s]*?)Reversed', lines, re.MULTILINE)
            shelly_reversed_lines = re.search(r'^Reversed([\S\s]*?)Min Voltage', lines, re.MULTILINE)

            custom_consumption_lines = shelly_lines_2_custom_lines(shelly_consumption_lines.group(1).splitlines())
            custom_reversed_lines = shelly_lines_2_custom_lines(shelly_reversed_lines.group(1).splitlines())

            custom_csv_header = ['Data', 'Consumo', 'Restituzione']
            custom_csv_data = []
        
            for index, custom_consumption_line in enumerate(custom_consumption_lines):
                if (custom_consumption_line[0] == custom_reversed_lines[index][0]):
                    custom_csv_data.append({
                                            'Data': custom_consumption_line[0], 
                                            'Consumo': custom_consumption_line[1], 
                                            'Restituzione': custom_reversed_lines[index][1]
                                            })

            with open(customcsv, 'w', encoding='UTF8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=custom_csv_header)
                writer.writeheader()
                writer.writerows(custom_csv_data)
        else:
            print (f"error: file '{shellycsvfile}' would appear not to be a CSV file produced by the shelly device")
            file.close()
            exit()
        
        file.close()

        