#include "fibonacci.h"

// TODO: Implement a recursive fibonacci function.
using namespace std;

unsigned long long int fibonacci(int n){
	
	if (n == 0)
	{
		return 0;
	}
	if (n == 1)
	{
		return 1;
	}

	unsigned long long int result;
	result = fibonacci(n - 1) + fibonacci(n - 2);

	return result;
}
