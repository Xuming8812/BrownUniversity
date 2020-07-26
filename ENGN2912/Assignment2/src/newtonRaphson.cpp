#include <iostream>
#include <cmath>
#include "newtonRaphson.h"

using namespace std;


double newtonRaphson(double x0, double epsilon)
{
	
   //TODO: Given the initial value x0 and the convergence tolerance epsilon, return the solution of the equation e^x + x^3 - 5 = 0  
	//mind that f(x) = e^x + x^3 -5 and f`(x) = e^x +3^x2;
	// Xn+1 = Xn-f(Xn)/f`(Xn);
	double x_n{ x0 }, x_n1{ x0 };													//define two double to store Xn and Xn+1

	do
	{
		x_n = x_n1;																	//in every iteration, assign the last Xn+1 to current Xn
		x_n1 = x_n - (exp(x_n) + pow(x_n, 3) - 5) / (exp(x_n) + 3 * pow(x_n, 2));	//calculate according to the Newton Raphson function

	} while (abs(x_n1 - x_n) >= abs(epsilon));										//exit when |Xn+1 - Xn| < eps


	return x_n1;																	//return solution

}
