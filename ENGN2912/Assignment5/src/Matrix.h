#include <iostream>
#include <iomanip>
#include <stdexcept>
#include <vector>
#include <complex>
#include <typeinfo>
#include <cmath>

#ifndef Matrix_h
#define Matrix_h


#define DEBUG

using namespace std;

template<typename T, unsigned int rowSize = 2, unsigned int columnSize = 2>
class Matrix {
private:

	T** data_;
	unsigned int rowSize_;
	unsigned int columnSize_;
	string valueTypeT;



	//a helper function to delete the current pointer of data
	void deletePointerHelper()
	{
		//delete each row, which is also is array pointer
		for (unsigned i{ 0 }; i < this->rowSize_; ++i)
		{
			delete [] data_[i];
		}
		//delete the array pointer storing each row pointer
		delete [] data_;
	}

	void createPointerHelper()
	{
		//get size of the matrix
		const unsigned row{ this->rowSize_ };
		const unsigned col{ this->columnSize_ };

		//initialize data_ as a array for pointer of each row
		data_ = new T*[row];

		for (unsigned i{ 0 }; i < row; ++i)
		{
			//for each row, it`s a pointer to an array
			data_[i] = new T[col];
		}
	}

	void exchangeTwoRows(T* row1,T* row2, unsigned col)
	{
		T temp;
		for (unsigned i{ 0 }; i < col; ++i)
		{
			temp = row1[i];
			row1[i] = row2[i];
			row2[i] = temp;
		}
	}

	T detHelper( T** input,unsigned row)
	{
		T result{ 1 };

		int exchangeTimes{ 0 };
		
		T zero{ 0 };

		for (unsigned i{ 0 }; i < row; i++)
		{

			//if the element on diagonal line is 0, show exchange two row
			if (input[i][i] == zero)
			{
				for (unsigned j{ i }; j < row; ++j)
				{
					if (input[i][i] != zero)
					{
						T temp;
						//exchange two rows
						for (unsigned k{ 0 }; k < row; ++k)
						{
							temp = input[i][k];
							input[i][k] = input[j][k];
							input[j][k] = temp;
						}

						exchangeTimes++;
					}
				}
			}
			else
			{
				for (unsigned j{ i + 1 }; j < row; ++j)
				{
					auto cofficient = input[j][i] / input[i][i];

					for (unsigned k{ 0 }; k < row; ++k)
					{
						input[j][k] = input[j][k] - input[i][k] *cofficient;
					}
				}
			}
		}

		for (unsigned i{ 0 }; i < row; i++)
		{
			result *= input[i][i];
		}

		if (exchangeTimes % 2 == 1)
		{
			result = -result;
		}

		return result;

	}

public:

	unsigned int getRowSize() const
	{
		// TODO: return row size		
		return rowSize_;
	}

	unsigned int getColumnSize() const
	{
		// TODO: return column size
		return columnSize_;
	}

	Matrix():rowSize_(rowSize),columnSize_(columnSize)
	{


		//create pointer for data
		createPointerHelper();

		const unsigned row{ this->rowSize_ };
		const unsigned col{ this->columnSize_ };

		//initial all element by 0
		for (unsigned i{ 0 }; i < row; ++i)
		{
			for (unsigned j{ 0 }; j < col; ++j)
			{
				data_[i][j] = 0;
			}

		}


		#ifdef DEBUG
			cout << "Matrix<" << getValueType() << ">::Matrix() default constructor" << endl;
		#endif
	}

	Matrix(Matrix const& referenceMatrix)
	{
		// TODO: implement the copy constructor
		
		//if data_ exsits, there are data in the current matrix, need to delete it first;
		//if (data_)
		//{
		//	deletePointerHelper();
		//}

		// set the matrix size by the input matrix
		this->rowSize_ = referenceMatrix.getRowSize();
		this->columnSize_ = referenceMatrix.getColumnSize();
		
		//create pointer for data
		createPointerHelper();

		const unsigned row{ this->rowSize_ };
		const unsigned col{ this->columnSize_ };


		//traversal to assign value for each element
		for (unsigned i{ 0 }; i < row; ++i)
		{
			for (unsigned j{ 0 }; j < col; ++j)
			{
				this->data_[i][j] = referenceMatrix(i, j);
			}
		}

		#ifdef DEBUG
			cout << "Matrix<" << getValueType() << ">::Matrix() copy constructor" << endl;
		#endif
	}

	Matrix(T const * const& data) :rowSize_(rowSize), columnSize_(columnSize)
	{
		// TODO: implement the data array constructor
		
		createPointerHelper();

		const unsigned row{ this->rowSize_ };
		const unsigned col{ this->columnSize_ };

		for (unsigned i{ 0 }; i < row; ++i)
		{
			for (unsigned j{ 0 }; j < this->columnSize_; ++j)
			{
				this->data_[i][j] = data[i*row + j];
			}
		}

		#ifdef DEBUG
			cout << "Matrix<" << getValueType() << ">::Matrix() constructor by a array of T" << endl;
		#endif
	}

	Matrix(vector<T> const& data) :rowSize_(rowSize), columnSize_(columnSize)
	{
		// TODO: implement the data vector constructor

		createPointerHelper();

		if (data.size() < this->rowSize_*this->columnSize_)
		{
			throw runtime_error(" The size of input vector is shorter than the capacity of the matrix!");
		}

		for (unsigned i{ 0 }; i < this->rowSize_; ++i)
		{
			for (unsigned j{ 0 }; j < this->columnSize_; ++j)
			{
				this->data_[i][j] = data[i*this->rowSize_ + j];
			}
		}

		#ifdef DEBUG
			cout << "Matrix<" << getValueType() << ">::Matrix() constructor by a vector of T" << endl;
		#endif
	}

	~Matrix()
	{
		// TODO: implement the destructor
		#ifdef DEBUG

			cout << "Matrix<" << getValueType() << ">::Matrix() destructor" << endl;
		#endif

		if (data_)
		{
			deletePointerHelper();
		}
		
	}

	T& operator()(unsigned const row, unsigned const column)
	{
		// TODO: overload the parenthesis operator
		if (row < 0 || row >= this->rowSize_)
		{
			throw runtime_error("The input row number is our of range!");
		}

		if (column < 0 || column >= this->columnSize_)
		{
			throw runtime_error("The input column number is our of range!");
		}

		#ifdef DEBUG
			T element = data_[0][0];

			string typeT = typeid(element).name();

			if(typeT == "i")
			{
				typeT = "int";
			}
			else if(typeT == "d")
			{
				typeT = "double";
			}
			else if(typeT == "f")
			{
				typeT = "float";
			}
			else if(typeT == "St7complexIdE")
			{
				typeT = "complex";
			}
			else
			{
			}



			cout << "Matrix<" << typeT << ">::Matrix() overriden operator () for setting value" << endl;
		#endif

		return data_[row][column];
	}

	T operator()(unsigned const row, unsigned const column) const
	{
		if (row < 0 || row >= this->rowSize_)
		{
			throw runtime_error("The input row number is our of range!");
		}

		if (column < 0 || column >= this->columnSize_)
		{
			throw runtime_error("The input column number is our of range!");
		}

		#ifdef DEBUG
			T element = data_[0][0];

			string typeT = typeid(element).name();

			if(typeT == "i")
			{
				typeT = "int";
			}
			else if(typeT == "d")
			{
				typeT = "double";
			}
			else if(typeT == "f")
			{
				typeT = "float";
			}
			else if(typeT == "St7complexIdE")
			{
				typeT = "complex";
			}
			else
			{
			}

			cout << "Matrix<" << typeT << ">::Matrix() overriden operator () for getting value" << endl;
		#endif

		return  data_[row][column];
	}

	void Print()
	{
		// TODO: implement the Print() method

		T element = data_[0][0];


		//get the type of T
		string typeT = typeid(element).name();
		//if type is int, width is 4
		if (typeT == "i" || typeT == "unsigned")
		{
			for (unsigned i{ 0 }; i < this->rowSize_; ++i)
			{
				cout << "| ";
				for (unsigned j{ 0 }; j < this->columnSize_; ++j)
				{
					if (j != 0)
					{
						cout << "  ";
					}
					cout << setw(4) << right << data_[i][j];
				}
				cout << " |" << endl;
			}
		}
		//if type is floating point, precision is 3, using scientific notion and width is 10
		else if (typeT == "f" || typeT == "d")
		{
			cout << setprecision(3) << scientific;
			
			for (unsigned i{ 0 }; i < this->rowSize_; ++i)
			{
				cout << "| ";
				for (unsigned j{ 0 }; j < this->columnSize_; ++j)
				{
					if (j != 0)
					{
						cout << "  ";
					}
					cout << setw(10) << right << data_[i][j];
				}
				cout << " |" << endl;
			}
		}
		//if type is complex, precision is 3 and width is 7
		else if (typeT=="St7complexIdE")
		{
			
			for (unsigned i{ 0 }; i < this->rowSize_; ++i)
			{
				cout << "| ";
				for (unsigned j{ 0 }; j < this->columnSize_; ++j)
				{
					if (j != 0)
					{
						cout << "  ";
					}

					std::complex<double> current = static_cast<complex<double>>(data_[i][j]);

					if(current.imag()<0)
					{
						double temp{- current.imag() };						
						cout.precision(4);
						cout << setw(7) << fixed<< right << current.real() << " - " << setw(7) << fixed << right << temp << "i";						
					}
					else
					{
						cout.precision(4);						
						cout << setw(7)  << fixed<< right << current.real() << " + " << setw(7) << fixed << right << current.imag() << "i";
					}	
					
				}
				cout << " |" << endl;
			}
		}

		#ifdef DEBUG
			cout << "Matrix<" << getValueType() << ">::Matrix() member function to print data of matrix" << endl;
		#endif
	}

	friend ostream& operator<< (ostream& out, Matrix& referenceMatrix)
	{
		// TODO: overload the << operator : "introvert" friend

		T element = referenceMatrix(0,0);
		
		//get the type of T
		string typeT = typeid(element).name();

		//if type is int, width is 4
		if (typeT == "i" || typeT == "unsigned")
		{
			for (unsigned i{ 0 }; i < referenceMatrix.getRowSize(); ++i)
			{
				out << "| ";
				for (unsigned j{ 0 }; j < referenceMatrix.getColumnSize(); ++j)
				{
					if (j != 0)
					{
						out << "  ";
					}
					out << setw(4) << right << referenceMatrix(i,j);
				}
				out << " |" << endl;
			}
		}
		//if type is floating point, precision is 3, using scientific notion and width is 10
		else if (typeT == "f" || typeT == "d")
		{
			out << setprecision(3) << scientific;

			for (unsigned i{ 0 }; i < referenceMatrix.getRowSize(); ++i)
			{
				out << "| ";
				for (unsigned j{ 0 }; j < referenceMatrix.getColumnSize(); ++j)
				{
					if (j != 0)
					{
						out << "  ";
					}
					out << setw(10) << right << referenceMatrix(i, j);
				}
				out << " |" << endl;
			}
		}
		//if type is complex, precision is 3 and width is 7
		else if (typeT == "St7complexIdE")
		{
			out << setprecision(4);
			for (unsigned i{ 0 }; i < referenceMatrix.getRowSize(); ++i)
			{
				out << "| ";
				for (unsigned j{ 0 }; j < referenceMatrix.getColumnSize(); ++j)
				{
					if (j != 0)
					{
						out << "  ";
					}

					std::complex<double> current = static_cast<complex<double>>(referenceMatrix(i,j));

					if(current.imag()<0)
					{
						double temp{- current.imag() };						
						out.precision(4);
						out << setw(7) << fixed<< right << current.real() << " - " << setw(7) << fixed << right << temp << "i";						
					}
					else
					{
						out.precision(4);						
						out << setw(7)  << fixed<< right << current.real() << " + " << setw(7) << fixed << right << current.imag() << "i";
					}
				}
				out << " |" << endl;
			}
		}

		#ifdef DEBUG


			if(typeT == "i")
			{
				typeT = "int";
			}
			else if(typeT == "d")
			{
				typeT = "double";
			}
			else if(typeT == "f")
			{
				typeT = "float";
			}
			else if(typeT == "St7complexIdE")
			{
				typeT = "complex";
			}
			else
			{
			}


			cout << "Matrix<" << typeT << ">::Matrix() friend member function overriden operator << for output" << endl;
		#endif

		return out;
	}

	Matrix& operator= (Matrix const& referenceMatrix)
	{
		// TODO: overload the assignment operator

		if (&referenceMatrix != this)
		{
			//if data_ exsits, there are data in the current matrix, need to delete it first;
			if (data_)
			{
				deletePointerHelper();
			}

			// set the matrix size by the input matrix
			this->rowSize_ = referenceMatrix.getRowSize();
			this->columnSize_ = referenceMatrix.getColumnSize();

			//create pointer for data
			createPointerHelper();

			const unsigned row{ this->rowSize_ };
			const unsigned col{ this->columnSize_ };


			//traversal to assign value for each element
			for (unsigned i{ 0 }; i < row; ++i)
			{
				for (unsigned j{ 0 }; j < col; ++j)
				{
					this->data_[i][j] = referenceMatrix(i, j);
				}
			}
		}

		#ifdef DEBUG
			cout << "Matrix<" << getValueType() << ">::Matrix() overriden operator = for assignment "<< endl;
		#endif
		
		return *this;
	}

	Matrix operator-()
	{
		// TODO: overload the unary subtraction operator
		const unsigned row{ this->rowSize_ };
		const unsigned col{ this->columnSize_ };

		Matrix result = *this;

		for (unsigned i{ 0 }; i < row; ++i)
		{
			for (unsigned j{ 0 }; j < col; ++j)
			{
				result(i, j) = static_cast<T>(-data_[i][j]);
			}
		}

		#ifdef DEBUG
			cout << "Matrix<" << getValueType() << ">::Matrix() overriden operator - for unary -" << endl;
		#endif

		return result;
	}

	Matrix operator+(Matrix const& referenceMatrix)
	{
		// TODO: overload the binary addition operator
		const unsigned row{ this->rowSize_ };
		const unsigned col{ this->columnSize_ };

		Matrix result = referenceMatrix;

		for (unsigned i{ 0 }; i < row; ++i)
		{
			for (unsigned j{ 0 }; j < col; ++j)
			{
				result(i, j) = static_cast<T>(data_[i][j] + referenceMatrix(i, j));
			}
		}

		#ifdef DEBUG
			cout << "Matrix<" << getValueType() << ">::Matrix() overriden operator + for addiction" << endl;
		#endif

		return result;
	}

	Matrix operator-(Matrix const& referenceMatrix)
	{
		// TODO: overload the binary subtraction operator

		const unsigned row{ this->rowSize_ };
		const unsigned col{ this->columnSize_ };

		Matrix result = referenceMatrix;

		for (unsigned i{ 0 }; i < row; ++i)
		{
			for (unsigned j{ 0 }; j < col; ++j)
			{
				result(i,j) = static_cast<T>(data_[i][j]- referenceMatrix(i,j));
			}
		}

		#ifdef DEBUG
			cout << "Matrix<" << getValueType() << ">::Matrix() overriden operator + for substraction" << endl;
		#endif

		return result;
	}

	template <unsigned rowSize2, unsigned columnSize2>
	Matrix<T, rowSize, columnSize2> operator*(Matrix<T, rowSize2, columnSize2>& referenceMatrix)
	{
		// TODO: overload the binary multiplication operator
		Matrix<T, rowSize, columnSize2> result;

		const unsigned row{ this->rowSize_ };
		const unsigned col{ this->columnSize_ };
		const unsigned col2{ this->columnSize_ };

		for (unsigned i{ 0 }; i < row; ++i)
		{
			for (unsigned j{ 0 }; j < col2; ++j)
			{
				for (unsigned k{ 0 }; k < col; ++k)
				{
					result(i, j) = result(i, j) + this->data_[i][k] * referenceMatrix(k, j);
				}
			}
		}

		#ifdef DEBUG

			T element = referenceMatrix(0,0);
			string typeT = typeid(element).name();

			if(typeT == "i")
			{
				typeT = "int";
			}
			else if(typeT == "d")
			{
				typeT = "double";
			}
			else if(typeT == "f")
			{
				typeT = "float";
			}
			else if(typeT == "St7complexIdE")
			{
				typeT = "complex";
			}
			else
			{
			}
			
			cout << "Matrix<" << typeT << ">::Matrix() overriden operator * for multiplication between matrices" << endl;
		#endif

		return result;
	}

	Matrix operator*(T const& scalar)
	{
		// TODO: overload the scalar multiplication operator (matrix * scalar)
		const unsigned row{ this->rowSize_ };
		const unsigned col{ this->columnSize_ };

		Matrix result = *this;

		for (unsigned i{ 0 }; i < row; ++i)
		{
			for (unsigned j{ 0 }; j < col; ++j)
			{
				result(i, j) = static_cast<T>(data_[i][j]* scalar);
			}
		}

		#ifdef DEBUG
			cout << "Matrix<" << getValueType() << ">::Matrix() overriden operator * for multiplication between a matrix and a number" << endl;
		#endif

		return result;
	}

	friend Matrix operator*(T const& scalar, Matrix const& referenceMatrix)
	{
		// TODO: overload the scalar multiplication operator (scalar * matrix) : "introvert" friend
		const unsigned row{ referenceMatrix.getRowSize() };
		const unsigned col{ referenceMatrix.getColumnSize() };

		Matrix result = referenceMatrix;

		for (unsigned i{ 0 }; i < row; ++i)
		{
			for (unsigned j{ 0 }; j < col; ++j)
			{
				result(i, j) = static_cast<T>(referenceMatrix(i,j) * scalar);
			}
		}

		#ifdef DEBUG

			T element = referenceMatrix(0,0);
			string typeT = typeid(element).name();

			if(typeT == "i")
			{
				typeT = "int";
			}
			else if(typeT == "d")
			{
				typeT = "double";
			}
			else if(typeT == "f")
			{
				typeT = "float";
			}
			else if(typeT == "St7complexIdE")
			{
				typeT = "complex";
			}
			else
			{
			}
			cout << "Matrix<" << typeT << ">::Matrix() friend member function overriden operator * for mulitiplication between a number and a matrix" << endl;
		#endif

		return result;


	}

	T Det()
	{
		// TODO: implement the determinant method
		const unsigned row{ this->rowSize_ };
		const unsigned col{ this->columnSize_ };

		T result;

		if(row!= col)
		{
			throw length_error("Cannot take determinant of a non-square matrix!");
		}

		// gaussian method to make a triangle matrix

		T** tempData;

		tempData = new T*[row];

		for (unsigned i{ 0 }; i < row; ++i)
		{
			//for each row, it`s a pointer to an array
			tempData[i] = new T[col];
		}

		for (unsigned i{ 0 }; i < row; ++i)
		{
			for (unsigned j{ 0 }; j < row; ++j)
			{
				tempData[i][j] = data_[i][j];
			}
		}

		result = detHelper(tempData, row);
		//delete the pointer after using
		for (unsigned i{ 0 }; i < row; ++i)
		{
			delete[] tempData[i];
		}

		delete[] tempData;

		#ifdef DEBUG
			cout << "Matrix<" << getValueType() << ">::Matrix() member function to calculate determinant" << endl;
		#endif

	
		return result;
	}

	Matrix Inv()
	{
		// TODO: implement the inverse method

		const unsigned row{ this->rowSize_ };
		const unsigned col{ this->columnSize_ };

		if (row != col)
		{
			throw length_error("Cannot take determinant of a non-square matrix!");
		}

		T zero{ 0 };

		T det = this->Det();

		if (det == zero)
		{
			throw range_error("There is no inverse matrix for this matrix!");
		}

		Matrix result;

		//create a matrix to store the adjoint matrix
		T** tempData;

		tempData = new T*[row-1];

		for (unsigned i{ 0 }; i < row-1; ++i)
		{
			//for each row, it`s a pointer to an array
			tempData[i] = new T[col-1];
		}

		for (unsigned i{ 0 }; i < row; ++i)
		{
			for (unsigned j{ 0 }; j < row; ++j)
			{
				for (unsigned k{ 0 }; k < row - 1; ++k)
				{
					for (unsigned l{ 0 }; l < row - 1; ++l)
					{
						unsigned x = k >= i ? k + 1 : k;
						unsigned y = l >= j ? l + 1 : l;
						
						tempData[k][l] = data_[x][y];
					}
				}

				result(j, i) = detHelper(tempData, row-1);

				if ((i + j) % 2 == 1)
				{
					result(j, i) = -result(j, i);
				}

				result(j, i) = static_cast<T>(result(j, i) / det);
				
			}
		}

		//delete the pointer after using
		for (unsigned i{ 0 }; i < row-1; ++i)
		{
			delete[] tempData[i];
		}

		delete[] tempData;

		#ifdef DEBUG
			cout << "Matrix<" << getValueType() << ">::Matrix() member function to calculate inverse matrix" << endl;
		#endif

		return result;
	}

	string getValueType()
	{
		T element = data_[0][0];
		string typeT = typeid(element).name();

		if(typeT == "i")
		{
			typeT = "int";
		}
		else if(typeT == "d")
		{
			typeT = "double";
		}
		else if(typeT == "f")
		{
			typeT = "float";
		}
		else if(typeT == "St7complexIdE")
		{
			typeT = "complex";
		}
		else
		{
		}

		return typeT;
		
	}

};
#endif // Matrix_hpp#pragma once
