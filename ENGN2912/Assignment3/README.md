# HW3 Ming Xu

[![Build Status](https://travis-ci.com/ENGN2912B-2018/hw3-Xuming8812.svg?token=3JDRzeLyM1vNMxzmeSBG&branch=master)](https://travis-ci.com/ENGN2912B-2018/hw3-Xuming8812)

## TA Comments:

3.1) You can allocate dynamic memory using a single double pointer (\*\*). [20/20]

3.2) Quantify the difference in accuracy between the two methods. Use gprof to evaluate runtime performance [18/20]

3.3) [20/20]

3.4) [20/20]

3.5) The helper method to compute the string length defined in erase could also be used in concat and substr. [20/20]

Total: 98/100

## Important Notes:
* Make sure you use the flag CMAKE_CXX_COMPILER=g++ when building on CCV
* The template code will not compile. This is intended behavior
* Make sure you push your last changes before the deadline
* If you had any questions, post them on Slack
* Use *git pull* to get the latest homework template
  - If you have already accepted the assignment and made changes to your local repository save the repository in a zip file
  - *git pull* may result in *merge* conflicts. If you are unsure how to resolve these, contact TAs on Slack

# Goals:

## Problem 3.1:
* Read the problem description in the PDF file on Canvas
* Implement the Matrix2x2 class in `/src/Matrix2x2.h` and `/src/Matrix2x2.cpp`
* Make sure that the code provided in `mainQ1.cpp` produces correct results
  - Create and run executable: `/build/hw3Q1Executable`
* Run GSuite tests: `/build/hw3Tests/01_ClassesTests/01_runHW3ClassesTests`

## Problem 3.2:
* Read the problem description in the PDF file on Canvas
* Implement the AbstractOdeSolver, the ForwardEulerSolver and the RungeKuttaSolver
  - Corresponding source and header files are already created in `/src/`. Some of these files need no modification which is explicitly stated.
  - **Note:** The user defined ODE is implemented directly in the `mainQ2.cpp` file. This user defined ODE function is passed to the solver class constructor by a pointer. Observe that your constructor for the ODE solvers accepts a pointer to a function with the appropriate type.
* Make sure that the code provided in `mainQ2.cpp` produces correct results
  - Create and run executable: `/build/hw3Q2Executable`
* Run GSuite tests: `/build/hw3Tests/02_ODETests/02_runHW3ODETests`
* Part 5: Describe the quantitative differences between the Forward Euler and Runge-Kutta methods:

  - Part a:  As the stepsize becomes larger, the error of Foward Eular method becomes larger. While the RungeKutta method can keep the good accuracy. As the stepsize becomes smaller, the accuracy of both methods increases.
    
  - Part b: The accuracy of RungeKutta method is 4 orders higher, which is 10000 times than the Forward Euler method. Since the RungeKutta is a high order method. It fits the derivative function by choosing four points in [Xn-1, Xn], and calculate the weighed average of the four points. While Forward Euler method only use one point. According the test result, the result of every point calculated by the RungeKutta is rather accurate. While the error of Foward Euler method increases as the t increases.
   
  - Part c: 4 Times;

## Problem 3.3:
* Read the problem description in the PDF file on Canvas
* Implement the translation function in `/src/translation.cpp`
* Answer the following question: "Why are some of the arguments declared as *const*?"
  
  - It`s easy to change the original value passed by reference. It can lead to wrong results or even vital errors. By using the const mark, one can make sure that the input value can not be changed within the function. Even if the value is changed accidentally, the complier can throw a error as a remind.
  
* Write tests for your function in `mainQ3.cpp`
  - Create and run executable: `/build/hw3Q3Executable`
* Run GSuite tests: `/build/hw3Tests/03_TranslationTests/03_runHW3TranslationTests`

## Problem 3.4:
* Read the problem description in the PDF file on Canvas
* Implement the fibonacci function in `/src/fibonacci.cpp`. Make sure your implementation is recursive.
* Implement estimategoldenratio in `/src/estimategoldenratio.cpp` 
* Test your code in `mainQ4.cpp`:
  - Create and run executable: `/build/hw3Q4Executable`
* Run GSuite tests: `/build/hw3Tests/04_GoldenRatioTests/04_runHW3GoldenRatioTests`
* Document your findings here: 
  - To achieve a floating point precision of nine, a epsilon of 1e-9 is chosen to control the accuracy. If two consecutive FN has a error smaller than 1e-9, then it can be regarded the FN convergenced to a accuracy of 1E-9, which is the ninth digit after the decimal point.
 

## Problem 3.5:
* Read the problem description in the PDF file on Canvas
* Write string processing functions in separate source and header files:
  - Put your declarations and implementation in `/src/concat.h`, `/src/concat.cpp`, `/src/substr.h`, `/src/substr.cpp`, `/src/erase.h`, `/src/erase.cpp`
  - Do **NOT** use the string class
  - If needed, use helper functions to keep your code short and to avoid redundancy
* Write tests for your code in `mainQ5.cpp`
* Run GSuite tests: `/build/hw3Tests/05_StringTests/05_runHW3StringTests`

Good luck!

ENGN2912B TAs
