// Abstract ODE solver methods

#include "AbstractOdeSolver.h"

// TODO: Implement the following methods:
// 1) AbstractOdeSolver::SetStepSize
// 2) AbstractOdeSolver::SetTimeInterval
// 2) AbstractOdeSolver::SetInitialValue

using namespace std;

void AbstractOdeSolver::SetStepSize(double h)
{
	stepSize = h;
}

void AbstractOdeSolver::SetInitialValue(double y0)
{
	initialValue = y0;
}

void AbstractOdeSolver::SetTimeInterval(double t0, double t1)
{
	initialTime = t0;
	finalTime = t1;
}