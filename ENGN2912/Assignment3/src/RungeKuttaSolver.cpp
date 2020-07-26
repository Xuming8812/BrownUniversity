#include "AbstractOdeSolver.h"
#include "RungeKuttaSolver.h"
#include <iostream>
#include <iomanip>
#include <cmath>
#include<vector>

using namespace std;

double RungeKuttaSolver::SolveEquation() {

	// TODO: 1) Implement the SolveEquation method and return the function value at final time point
	//			i.e., y_i[finalTime].
	//		 2) Print the interim values using cout.

	vector<double> yValue;
	yValue.push_back(initialValue);

	double yn = initialValue;
	double tn = initialTime;

	while (tn < finalTime)
	{
		double k1 = stepSize * RightHandSide(yn, tn);
		double k2 = stepSize * RightHandSide(yn + 0.5*k1, tn + 0.5*stepSize);
		double k3 = stepSize * RightHandSide(yn + 0.5*k2, tn + 0.5*stepSize);
		double k4 = stepSize * RightHandSide(yn + k3, tn + stepSize);

		yn = yn + (k1 + 2 * k2 + 2 * k3 + k4) / 6;
		yValue.push_back(yn);
		tn = tn + stepSize;
	}

	for (size_t i{ 0 }; i < yValue.size(); ++i)
	{
		cout << "y_i[" << initialTime + i * stepSize << "] = " << yValue[i] << endl;
	}

	return yValue[yValue.size() - 1];

}
