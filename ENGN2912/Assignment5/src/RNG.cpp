#include <random>
#include <fstream>
#include <algorithm>
#include <string>
#include <vector>
#include <utility>
#include "RNG.h"
#include <bitset>

using namespace std;

//fill vector with wgn
void fill_vec(vector<double> &vd, int const& seed)
{
  // TODO: fill vector vd using the knuth_b engine with "seed"
  	knuth_b kbGenerator(seed);
	
	//define a normal distribution with mean = -10, std = 5;
	normal_distribution<> normal(-10.0, 5.0);

	for (unsigned i{ 0 }; i < vd.size(); ++i)
	{
		vd[i] = normal(kbGenerator);
	}
}

//convert vector of floating-point format to fixed-point format
pair<double, double> convert_to_fixed(vector<double> const& vd, vector<int32_t>& vi, unsigned const& nBits)
{
  // TODO: 1) find the minimum and maximum values in vd, store them in a pair container and return it
  //	   2) convert each floating-point number in vd to a fixed-point format using a precision of nBits and store in vi
  	pair<double, double> minmax;

	//get the min and max element of the vector
	auto result = minmax_element(vd.begin(), vd.end());

	minmax.first = *result.first;
	minmax.second = *result.second;


	//see how many itervals there are between max and min
	unsigned itervalNum = pow(2,nBits) - 1 ;
	//then min =  -pow(2, nBits - 1) stands for the min element in vd
	//max =pow(2,nBits-1)-1 stands for the max element in vd
	int min = -pow(2, nBits - 1),max=pow(2,nBits-1)-1;
	
	double interval = (minmax.second - minmax.first) / itervalNum;

	for (auto item : vd)
	{
		int index = (int)((item - minmax.first) / interval+min);
		vi.push_back(index);
	}

	return minmax;
}

//convert fixed-point format back to floating-point format
void convert_to_float(vector<int32_t> const& vi, vector<double>& vd, unsigned const& nBits, pair<double, double> const& minmax)
{
  // TODO: using minmax convert the fixed-point back to floating-point and store in vd
	double minValue = minmax.first, maxValue = minmax.second;

	unsigned itervalNum = pow(2, nBits)-1;

	double interval = (maxValue - minValue) / itervalNum;

	int min = -pow(2, nBits - 1), max = pow(2, nBits - 1) - 1;

	for (auto item : vi)
	{
		double temp = (item - min)*interval + minValue;
		vd.push_back(temp);
	}
}

//save a fixed-point vector to a file
void save_vec(vector<int32_t> const& vi, string const& filename)
{
  // TODO: save the vector of fixed-point numbers in a binary file named "filename"
	ofstream fout;
	fout.open(filename, ios::binary);

	for (auto item : vi)
	{
		//bitset<32>temp(item);
		//fout << (char*)&item;
		fout.write((char*)&item,sizeof(int32_t));
	}
	fout.close();
}
