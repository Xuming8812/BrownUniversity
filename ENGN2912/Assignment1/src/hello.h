#pragma once

#include <iostream>
#include <string>

using namespace std;

void hello(istream& input)
{
    // TODO: Use the input stream to take in a name and use the standard output stream cout to print out "Hello, my name is <name>!"
	string name;

	input>>name;

	cout << "Hello, my name is " << name << "!";

	return;
}





