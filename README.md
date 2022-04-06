# shellycsv2customcsv
`shellycsv2customcsv` is a Python3 script to parse CSV file produced by the shelly device and save the result in a custom CSV as described below:
1. Get information from the Consumption and Reversal "tables".
2. Change the date format and merge the information from Consumption and Reversal "tables".
3. Save the result in `shelly_custom.csv`.


## Usage

```
usage: shellycsv2customcsv [-h] [--output-path] shellycsvfile

Parse the CSV file produced by the shelly device and save the result in shelly_custom.csv

positional arguments:
  shellycsvfile   If no path is specified the file will be searched in the current directory

optional arguments:
  -h, --help      show this help message and exit
  --output-path   output directory, must exist. If no path is specified the file will be saved in the current directory
```

### Example

```
$ python shellycsv2customcsv.py download.csv --output-path ~/Desktop
```
It will create in the output folder (`~/Desktop/`) the `shelly_custom.csv` file
