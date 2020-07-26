#include "translation.h"

// TODO: Implement your "translation" function 
using namespace std;

bool translation(double const& p1X, double const& p1Y, double const& p2X, double const& p2Y, double& vectorX, double& vectorY)
{
	if (p1X == p2X && p1Y == p2Y)
	{
		vectorX = 0;
		vectorY = 0;
		return false;
	}

	vectorX = p2X - p1X;
	vectorY = p2Y - p1Y;

	return true;
}
