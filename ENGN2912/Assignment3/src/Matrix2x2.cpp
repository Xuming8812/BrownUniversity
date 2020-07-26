// TODO: Implement the Matrix2x2 class methods 
#include"Matrix2x2.h"
#include<iostream>
#include<iomanip>
#include<stdexcept>

using namespace std;

Matrix2x2::Matrix2x2() :data{ new double[Matrix2x2::numbers] }
{
	for (size_t i{ 0 }; i < Matrix2x2::numbers; i++)
	{
		data[i] = 0;
	}
}


Matrix2x2::Matrix2x2(const Matrix2x2& input) :data{ new double[Matrix2x2::numbers] }
{
	for (size_t i{ 0 }; i < Matrix2x2::numbers; i++)
	{
		data[i] = input.data[i];
	}
}

Matrix2x2::Matrix2x2(double a1, double a2, double a3, double a4) :data{ new double[Matrix2x2::numbers] }
{
	data[0] = a1;
	data[1] = a2;
	data[2] = a3;
	data[3] = a4;
}

Matrix2x2::Matrix2x2(double* as) :data{ new double[Matrix2x2::numbers] }
{
	for (size_t i{ 0 }; i < Matrix2x2::numbers; i++)
	{
		data[i] = as[i];
	}
}


Matrix2x2::~Matrix2x2()
{
	delete[]  data;
}

double Matrix2x2::getData(size_t i) const
{
	if (i < Matrix2x2::numbers)
	{
		return data[i];
	}
	else
	{
		throw runtime_error{ "Index out of range!" };
	}
}

double Matrix2x2::Det() const
{
	return data[0] * data[3] - data[1] * data[2];
}

Matrix2x2 Matrix2x2::Inv()
{
	double det = data[0] * data[3] - data[1] * data[2];

	if (det == 0)
	{
		throw runtime_error{ "The current matrix has no inverse matrix!" };
	}


	Matrix2x2 result(data[3] / det, -data[1] / det, -data[2] / det, data[0] / det);

	return result;
}

void Matrix2x2::Print() const
{
	cout << setprecision(3) << scientific;

	cout << "|" << setw(12) << right << data[0] << setw(12) << right << data[1] << "  |" << endl;
	cout << "|" << setw(12) << right << data[2] << setw(12) << right << data[3] << "  |" << endl;

	return;
}


Matrix2x2& Matrix2x2::operator=(const Matrix2x2& input)
{
	if (&input != this)
	{
		for (size_t i{ 0 }; i < Matrix2x2::numbers; i++)
		{
			this->data[i] = input.data[i];
		}
	}

	return *this;
}

Matrix2x2 Matrix2x2::operator-() const
{
	Matrix2x2 result(-this->data[0], -this->data[1], -this->data[2], -this->data[3]);

	return result;
}

Matrix2x2 Matrix2x2::operator+(Matrix2x2 const&  input) const
{
	Matrix2x2 result(this->getData(0) + input.getData(0), this->getData(1) + input.getData(1), this->getData(2) + input.getData(2), this->getData(3) + input.getData(3));

	return result;
}


Matrix2x2 Matrix2x2::operator-(Matrix2x2 const&  input) const
{
	Matrix2x2 result(this->getData(0) - input.getData(0), this->getData(1) - input.getData(1), this->getData(2) - input.getData(2), this->getData(3) - input.getData(3));

	return result;
}

Matrix2x2 Matrix2x2::operator*(Matrix2x2 const&  input) const
{
	double a11 = this->getData(0) * input.getData(0) + this->getData(1) * input.getData(2);
	double a12 = this->getData(0) * input.getData(1) + this->getData(1) * input.getData(3);
	double a21 = this->getData(2) * input.getData(0) + this->getData(3) * input.getData(2);
	double a22 = this->getData(2) * input.getData(1) + this->getData(3) * input.getData(3);

	Matrix2x2 result(a11, a12, a21, a22);

	return result;
}

Matrix2x2 Matrix2x2::operator*(double const input) const
{
	Matrix2x2 result(input*this->getData(0), input*this->getData(1), input*this->getData(2), input*this->getData(3));

	return result;
}

double Matrix2x2::operator()(int row, int col) const
{
	if (row > 2 && row < 0)
	{
		throw runtime_error("The input row number is out of range!");
	}
	if (col > 2 && col < 0)
	{
		throw runtime_error("The input column number is out of range!");
	}

	return data[2 * row + col];
}

double& Matrix2x2::operator()(int row, int col)
{
	if (row > 2 && row < 0)
	{
		throw runtime_error("The input row number is out of range!");
	}
	if (col > 2 && col < 0)
	{
		throw runtime_error("The input column number is out of range!");
	}

	return data[2 * row + col];
}

double Matrix2x2::geta1() const
{
	return data[0];
}
double Matrix2x2::geta2() const
{
	return data[1];
}
double Matrix2x2::geta3() const
{
	return data[2];
}
double Matrix2x2::geta4() const
{
	return data[3];
}


ostream& operator<<(ostream& output, const Matrix2x2& input)
{
	output << setprecision(3) << scientific;
	output << "|" << setw(12) << right << input.data[0] << setw(12) << right << input.data[1] << "  |" << endl;
	output << "|" << setw(12) << right << input.data[2] << setw(12) << right << input.data[3] << "  |" << endl;

	return output;
}