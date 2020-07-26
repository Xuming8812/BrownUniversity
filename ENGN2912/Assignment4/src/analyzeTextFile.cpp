#include "analyzeTextFile.h"
#include <iostream>
#include <string>
#include <sstream>
#include <fstream>

using namespace std;

void analyzeTextFile(string const& fileName, unsigned int& lineCount, unsigned int& characterCount)
{
	// initialize variables
	lineCount = 0;
	characterCount = 0;

	// read file, if not exists cout a warning
	ifstream fin;

	fin.open(fileName);

	//cout warning and return if the file doesn`t exsit
	if (!fin)
	{
		cout << "The file doesn`t exsit!" << endl;
		return;
	}
	//calculate the total number
	fin.seekg(0, ios::end);
	characterCount = fin.tellg();
	fin.seekg(0, ios::beg);

	string temp;

	while (getline(fin, temp))
	{
		lineCount++;
	}
	
	//characterCount+=lineCount;

	// close file

	fin.close();
}
