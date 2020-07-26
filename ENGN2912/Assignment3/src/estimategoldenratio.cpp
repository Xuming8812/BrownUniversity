#include "estimategoldenratio.h"
#include "fibonacci.h"
#include <cmath>

// TODO: Determine the limiting golden ratio.
using namespace std;

double estimategoldenratio(){

	double eps{ 1e-9 };
	double ratio = (double)fibonacci(2) / fibonacci(1);


	int i{ 3 };

	while (fabs((double)fibonacci(i) / fibonacci(i - 1) - ratio) >= eps)
	{
		ratio = (double)fibonacci(i) / fibonacci(i - 1);
		i++;
	}


	return ratio;

}
