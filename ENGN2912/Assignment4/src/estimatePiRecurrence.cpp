#include <cmath>
#include "estimatePiRecurrence.h"

/*
*
* Check error compared to REF_PI, defined in the header file
* Use 'fabs()' to define a termination criteria
*/
double estimatePiRecurrence(const double eps){
	double f0{ 0 }, fk{ 1 };

	double pi_0{ 0 }, pi_k{ 16.0 / 3 };

	unsigned i{ 1 };

	while (fabs(pi_k - pi_0) >= eps)
	{
		f0 = fk;
		pi_0 = pi_k;

		fk = f0 / (1 + sqrt(f0*f0 + 1));
		pi_k = pow(2, i + 2)*(fk - pow(fk, 3) / 3);

		i++;
	}

	return pi_k;
}
