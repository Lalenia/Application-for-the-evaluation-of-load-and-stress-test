# Application for the evaluation of load and stress tests

"This project was made during my internship at IVU Traffic Technologies AG and belongs entirely to the company. The use from others is not allowed. 
This code therefor is not the end product and sensitive information are replaced with section signs."

## The project
As part of quality assurance, companies load and stress tests to ensure the
stability of the company's software. During these tests
the performance data of the test systems is collected with monitoring software for example based on the open source
the open source components Icinga 2, Graphite and Grafana.

With this module, this data of the load and stress tests from the server can be recorded automatically after a test has been completed, which significantly reduces the effort required for test execution.
 This is to be done according to freely
parameters and criteria (definable periods of time, storage locations and file
file types) and no longer have to be implemented manually. Afterwards these data should be visualized as a report in a file.
output in a file.

## Description 

To automate the process of collecting workload graphs and raw data, a script with the following functionality was implemented:
- The script interprets the parameters described in Parameters, which specify which data should be retrieved in which time frame on which Graphite server.
- The script reads the list of records to be fetched from the configuration file supplied as parameters.
- The environment specific configuration is read from the environment configuration file supplied as a parameter.
- The script creates the output directory specified in the "outputdir" parameter if it does not exist.
- For each data set, the script iterates through the specified formats and
o fetches the data in the specified format from the rest API of the Graphite server. The time space specified on the command line is passed to the Graphite API via on the appropriate parameters. Environment specific parameters are replaced by the values in the file passed as environment configuration.
o saves the data in a file with the key of the data set as file name and the format as extension.

### Parameters
The script uses the following command line parameters:
1. URL of the Graphite server
2. Configuration file with the description of the data to be retrieved from Graphite.
3. Configuration file for environment specific parameters Start time of the query interval
4. End time of the query interval
5. Destination directory for the output files

### Configuration file
The configuration file specifies the data to be fetched by the script. It contains a hash with one entry per record. The key of the entry in the hash is the name of the data set. Each record contains the following parameters:
Specification of the data to be retrieved from Graphite.
A list of formats in which the data retrieved from Graphite should be represented.
Additional parameters that will be passed to Graphite when retrieving the data.

### Parameter Description for the command line.
1.  -u <url>
2.  -f <file>
3.  --envcfg <file>
4.  --from <time>
5.  --to <time>
6.  --outputfir <dir>
 
### Parameter description for the configuration file.
- target
- formats
- params
Variables in the format ${IDENTIFIER} can be used in the target and params parameters. These variables are replaced by the values of the parameters from the environment configuration file. 

### Command line
The script is called with the following command line:
collect_util_data.py -f congig --config_file.json -envcfg -env_cfg_file.yaml -u http://&&&& /graphite --outputdir results --from 2020.03.09 08:00 - to 2020.03.09 16:00
