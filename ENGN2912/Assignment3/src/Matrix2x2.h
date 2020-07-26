#ifndef Matrix2x2_h
#define Matrix2x2_h

// TODO: Declare the Matrix2x2 class

#include <iostream>

class Matrix2x2
{
	friend std::ostream& operator<<(std::ostream&, const Matrix2x2&);

public:

	static const size_t numbers{ 4 };
	explicit Matrix2x2(double*);						//constructor with input of a double array
	Matrix2x2();										//default constructor using dynamic memory allocation	
	Matrix2x2(double, double, double, double);			//constructor with input of 4 doubles
	Matrix2x2(const Matrix2x2&);

	~Matrix2x2();										//destructor

	void Print() const;									//print the matrix
	double Det() const;									//calculate the determinant of the matrix

	Matrix2x2 Inv();									//if inverse matrix exists, then return it. else, throw an error

	Matrix2x2& operator=(Matrix2x2 const&);				//overload the copy constructer

	Matrix2x2 operator-() const;						//overload the unary minus operator

	Matrix2x2 operator+(Matrix2x2 const &) const;		//overload operator+
	
	Matrix2x2 operator-(Matrix2x2 const &) const;		//overload operator-

	Matrix2x2 operator*(Matrix2x2 const &) const;		//overload operator*

	Matrix2x2 operator*(const double) const;			//overload operator* for double

	double getData(size_t index) const;					//access function of data

	double operator()(int, int) const;					//overload () for reading data

	double& operator()(int, int);						//overload () for writing data

	double geta1() const;
	double geta2() const;
	double geta3() const;
	double geta4() const;

private:
	double* data;
};

#endif // !MATRIX2X2_H

