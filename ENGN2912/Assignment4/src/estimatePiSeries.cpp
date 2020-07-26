#include <cmath>
#include <iostream>
#include "estimatePiSeries.h"

using namespace std;

/*
 * Check error compared to REF_PI, defined in the header file
 * Use 'fabs()' to define a termination criteria
 */
double estimatePiSeries(const double eps) {

	double pi_0{ 0.0 }, pi_k{4.0};

	unsigned long long i{ 3 };

	double flag = 4.0;
	
	while (pi_k - pi_0 >= eps || pi_0 - pi_k >= eps)
	{
		pi_0 = pi_k;

		flag *= -1;

		pi_k = pi_0+flag/i;
		
		i+=2;
	}

	return pi_k;

}
