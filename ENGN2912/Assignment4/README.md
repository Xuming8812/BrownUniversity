# HW4 Ming Xu

TODO: Update the above name fields with your name and surname.

Optional: Add your TRAVIS badge here!

Travis Badge:
[![Build Status](https://travis-ci.com/ENGN2912B-2018/hw4-Xuming8812.svg?token=3JDRzeLyM1vNMxzmeSBG&branch=master)](https://travis-ci.com/ENGN2912B-2018/hw4-Xuming8812)

https://travis-ci.com/ENGN2912B-2018/hw4-Xuming8812.svg?token=3JDRzeLyM1vNMxzmeSBG&branch=master

## Important Notes:
* Make sure you use the flag CMAKE_CXX_COMPILER=g++ when building on CCV
* Commit changes often. Use the student branch to develop code. Make a pull request for the master branch before the deadline.
* The template code provided will not compile until the pairs class is implemented
* To check the output of the autograder visit travis-ci.com and sign in with your GitHub account
* If you have any questions, post them on Slack

# Goals:

## Problem 4.1:
* Read the problem description in the PDF file on Canvas
* Implement the analyzeTextFile function in `/src/analyzeTextFile.cpp`
* Make sure that the code provided in `mainQ1.cpp` produces correct results
  - Create and run executable: `./hw4Q1Executable` in the build directory
  - Enter relative file path: e.g. `../sampleTextFile.txt`
* Run GSuite tests: `./hw4Tests/01_TextFileAnalysisTests/01_runHW4TextFileAnalysisTests`
  - **NOTE** GSuite tests should be run from the build directory. Do not navigate to sub-directories!

## Problem 4.2:
* Read the problem description in the PDF file on Canvas
* Implement templated pairs class in `src/pairs.h`
  - **Note:** You do not have to modify `src/pairs.cpp` (empty file)
* Make sure that the code provided in `mainQ2.cpp` produces correct results
  - Create and run executable: `./hw4Q2Executable` in the build directory
* Run GSuite tests: `./hw4Tests/02_PairsTests/02_runHW4PairsTests`

## Problem 4.3:
* Read the problem description in the PDF file on Canvas
* Implement estimatePiSeries function in `src/estimatePiSeries.cpp`
  - Use Gregory series summation to estimate the value of PI
* Implement estimatePiRecurrence function in `src/estimatePiRecurrence.cpp`
  - Use recurrence relation provided in the PDF
* Make sure that the code provided in `mainQ3.cpp` produces correct results
  - Create and run executable: `./hw4Q3Executable` in the build directory
  - **TODO:** Use gprof to evaluate the performance of your code
    - Describe your observations here
    
    Answer: In my initial implement of function "estimatePiSeries", I used "pow" to calculate -1^n,which was called too many times and took 38.27% of the whole running time according to the gprof. In order to decreasing the running time, the "estimatePiSeries" was improved by replacing the "pow" function by using a flag with initial value of 1. In each iteration, flag*=-1. Then the program can run much faster. Based on that observation, I found the functions for calculating double-type value are somehow not efficient enough. So, my next step is to try to decrease the number of calculation on double-type values.
    
    So, in the judgement condition of while loop, function "fabs" is replaced by "pi_k - pi_0 >= eps || pi_0 - pi_k >= eps", and in the while loop body, the number of multiplication and division operations of double-type value are decreased. 
    
    As a result, the "estimatePiSeries" function can run much faster
   
* Run GSuite tests: `./hw4Tests/03_PiTests/03_runHW4PiTests`

## Problem 4.4:
* Read the problem description in the PDF file on Canvas
* Implement the Image class and the ImageDenoiser class in `src/Image.cpp` and `src/ImageDenoiser.cpp`
  - Use function declarations in `src/Image.h` and `src/ImageDenoiser.cpp` as reference
* Make sure that the code provided in `mainQ4.cpp` produces the correct result
  - Create and run executable: `./hw4Q4Executable` in the build directory
  - View the image file generated: `../filteredImage.pgm`
  - **Note:** You can view pgm image files using an online viewer or in MATLAB
* Run GSuite tests: `./hw4Tests/04_ImageDenoisingTests/04_runHW4ImageDenoisingTests`
  - **NOTE** GSuite tests should be run from the build directory. Do not navigate to sub-directories!
  
Good luck!

ENGN2912B TAs
