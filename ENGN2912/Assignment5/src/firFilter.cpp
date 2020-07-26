#include <random>
#include "firFilter.h"

using namespace std;

//fill vector with wgn
void fill_vec(vector<double> &vd, int const& seed)
{
	// TODO: fill vector vd using the knuth_b engine with "seed"

		//define the knuth_b generator with intput seed
	knuth_b kbGenerator(seed);

	//define a normal distribution with mean = -10, std = 5;
	normal_distribution<> normal(0, 1);

	for (unsigned i{ 0 }; i < vd.size(); ++i)
	{
		vd[i] = normal(kbGenerator);
	}
}

// the default constructor, needs no further implementation
firFilter::firFilter() {}

firFilter::firFilter(vector<double> const& referenceFilter)
{
	// TODO: implement the vector instantiation based constructor
	h = referenceFilter;
}

void firFilter::SetCoef(vector<double> const& referenceFilter)
{
	// TODO: implement the SetCoef method
	h = referenceFilter;
}
vector<double> firFilter::GetCoef()
{
	// TODO: implement the GetCoef() method
	return h;
}

vector<double> firFilter::filter(vector<double> const& input)
{
	// TODO:  1) create an output vector of type double with an appropriate size that can correctly hold the filtered signal
	//        2) store the filtered signal samples in the output vector and return it

	vector<double> output(input.size(),0);

	for (int i{ 0 }; i < input.size(); ++i)
	{
		for (int j{ 0 }; j < h.size()&&(i-j)>=0; ++j)
		{
			output[i] = output[i] + h[j] * input[i - j];
		}
	}

	return output;
}
