#include "AbstractOdeSolver.h"
#include "ForwardEulerSolver.h"
#include <iostream>
#include <iomanip>
#include <cmath>
#include<vector>

using namespace std;

double ForwardEulerSolver::SolveEquation() {

	// TODO: 1) Implement the SolveEquation method and return the function value at final time point
	//			i.e., y_i[finalTime].
	//		 2) Print the interim values using cout.

	vector<double> yValue;
	yValue.push_back(initialValue);

	double yn = initialValue;
	double tn = initialTime;
	while (tn < finalTime)
	{
		yn = yn + stepSize * RightHandSide(yn, tn);
		yValue.push_back(yn);
		tn = tn + stepSize;
	}

	for (size_t i{ 0 }; i < yValue.size(); ++i)
	{
		cout << "y_i[" << initialTime + i * stepSize << "] = " << yValue[i] << endl;
	}

	return yValue[yValue.size() - 1];

}