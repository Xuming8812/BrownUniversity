#ifndef PAIRS_HPP
#define PAIRS_HPP

#include <iostream>
#include <string>

using namespace std;

// TODO: implement the templated pairs class

template <typename T1, typename T2>
class pairs
{
public:

	//default constructor, call the default constructor of first and second, respectively
	pairs() :first_{}, second_{}
	{
	};

	//constructor with input
	pairs(const T1& first, const T2& second) :first_(first), second_(second)
	{
	}
	
	//default destructor
	~pairs()
	{
	};

	//access function for first element
	T1 get_first() const
	{
		return first_;
	}
	//access function for second element
	T2 get_second() const
	{
		return second_;
	}
	//access function for first element
	void set_first(const T1& input)
	{
		first_ = input;
	}
	//access function for second element
	void set_second(const T2& input)
	{
		second_ = input;
	}

	// overload the copy operator
	pairs<T1, T2>& operator=(const pairs<T1, T2>& input)
	{
		if (&input != this)		//avoid seft assignment
		{
			this->first_ = input.get_first();
			this->second_ = input.get_second();
		}

		return *this;
	}

	// overload the == operator
	bool operator==(const pairs& input) const
	{
		return this->first_ == input.get_first() && this->second_ == input.get_second();
	}

	// overload the != operator
	bool operator!=(const pairs& input) const
	{
		return !this->operator==(input);
	}

	void print()
	{
		cout << "(" << this->get_first() << ", " << this->get_second() << ")" << endl;
	}

private:
	T1 first_;
	T2 second_;
};

// overload the << operator by inline non-member function implement
template <typename T1, typename T2>

inline ostream& operator<<(ostream& outStream, const pairs<T1, T2>& item)
{
	outStream << "(" << item.get_first() << ", " << item.get_second() << ")";

	return outStream;
}

#endif //PAIRS_HPP
