#include <iostream>
#include <iomanip>
#include "factorial.h"

using namespace std;

int main(int argc, char* argv[]) 
{
    
    //Question 2: Factorial
    cout << endl;    
    cout << "Question 2: Factorial" << endl;

    // TODO: 1) Using command-line parameters argc and argv, parse the input stream.
    //       2) For valid input (non-negative integers), output the factorial using
    //	     "factorial" function provided and the factorial function "factorial2" you are expected
    //       to implement (src/factorial.h and src/factorial.cpp) which can handle large inputs. 
    //       3) For non valid input (negative integers, floating points, alphabetic characters etc.)
    //       output a warning message with the following format: "Warning: Invalid input <invalid input>."
    

	for (int i{ 1 }; i < argc; ++i)
	{
		float inputF{ 0 };
		int input;
		input = atoi(argv[i]);
		inputF = atof(argv[i]);
		if (inputF != input)													//judge if the input is a floating points
		{
			cout << "Warning: Invalid input " << argv[i] << "." << endl;
		}
		else if (input <= 0)													//judge if the input is negative or containing alphabetic
		{
			cout << "Warning: Invalid input " << argv[i] << "." << endl;
		}
		else
		{
			int result1;
			double result2;														//use a double to store the huge number
			result1 = factorial(input);
			cout << "The factorial value of " << argv[i] << " by given factorical function is " << result1 << endl;
			result2 = factorial2(input);		
			cout << setprecision(20);
			cout << "The factorial value of " << argv[i] << " by the new factorical function is " << result2 << endl;
		}

	}

	//cin.get();

    return 0;
}





