# Brief Introduction
This folder **server** contains server subproject of the project **testing-scheduler**. 

This server project is developed based on **Python**.

# Directory Structure
- conductorclient: &nbsp;conductor python package
- src: &nbsp;it contains the core source code
- test: &nbsp;it's used to store testcases.

# Description
## Testcase
Testcases are stored in the subdirectory **test/test_case**.

The single directory in **test/test_case** stands for a **testsuite**. It contains several **testcase**.

There is a sample testsuite -- **logic** which contains the sample testcase.

## Run Instructions
*IMPORTANT: the current suggested build way of the project is **containerized build**. Please enter the directory **testing-scheduler/docker**, to see the details via the README.md there.*
</br>

###[CLI]
We can run the testcase by in the terminal, like:
> ./src/test_parser.py --filepath=path/to/file

explanation：

- ./test_parser.py:  the parse script
- path/to/file: the file path of the test case

###[webUI]
0. Setup Conductor in your host. Please visit [conductor dockers](https://github.com/Netflix/conductor/blob/master/docker/README.md) to learn how to do it.**This project use the docker-compose way to build.**
1. run the command below in cli：
	
    > python src/rest/router.py
2. start the server of frontend. see the README.md in details in the directory **testing-scheduler/ui**.
3. view the web page: http://localhost:5311/