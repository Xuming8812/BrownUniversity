#include "Image.h"
#include <iostream>
#include <string>
#include <vector>
#include <sstream>
#include <fstream>

using namespace std;

//constructor and deconstructor are provided
Image::Image(){ this->empty = true; this->height = 0; this->width = 0; (this->data).clear(); }
Image::~Image(){}

bool Image::readImage(string const& inputFileName)
{
    //parse input file and store pixel intensities in private member varlable data, if read successful return true
    //if input file does not exist, cout a warning and return false
	ifstream fin;
	string line;
	stringstream ss;
	unsigned rowNum{ 0 }, colNum{ 0 };
	fin.open(inputFileName);

	if (!fin)
	{
		cout << "Warning: The file doesn`t exsit!" << endl;
		this->empty = true;
		return false;
	}

	//set the empty value
	this->empty = false;

	//neglect the first row for image name
	getline(fin, line);

	//read row number and col num
	getline(fin, line);

	//use a string stream to turn string to int
	ss << line;
	ss >> colNum >> rowNum;

	//set value for width and height
	this->width = colNum;
	this->height = rowNum;

	//neglect the third row for max intensity
	getline(fin, line);

	//call setData function to resize and intialize the data matrix
	setData(rowNum, colNum, 0);

	//read data
	for (unsigned i{ 0 }; i < rowNum; ++i)
	{
		if (!getline(fin, line))
		{
			this->empty = true;
			return false;
		}

		//ss.flush();
		stringstream temp;

		temp << line;

		for (unsigned j{ 0 }; j < colNum; ++j)
		{
			temp >> this->data[i][j];
		}
	}

	fin.close();

	return true;
}

bool Image::writeImage(string const& outputFileName)
{
  //if the member variable data is not empty, save image content to file (overwrite if neccessary), if write successful return true
  //if the member variable data is empty, cout a warning and return false
	if (this->empty)
	{
		cout << "Warning: The image is empty!" << endl;

		return false;
	}

	ofstream fout;

	fout.open(outputFileName);
	fout << "P2" << endl;
	fout << this->width << " " << this->height << endl;
	fout << "255" << endl;

	unsigned rowNum{ this->height }, colNum{ this->width };

	for (unsigned i{ 0 }; i < rowNum; ++i)
	{
		string row{ " " };
		for (unsigned j{ 0 }; j < colNum; ++j)
		{
			row += to_string(this->data[i][j]) + " ";
		}

		row = row.substr(1);
		fout << row << endl;
	}

	fout.close();

	return true;

}

unsigned int Image::getPixelIntensity(unsigned int const r, unsigned int const c) const
{
  //if pixel location (r,c) is out of the image boundaries return 0, else return the pixel intensity at (r,c)
	if (r > this->height || c > this->width)
	{
		return 0;
	}

	return this->data[r][c];

}

void Image::setPixelIntensity(unsigned int const r, unsigned int const c, unsigned int const intensity)
{
  //if pixel location (r,c) is out of the image boundaries do notthing, else set the pixel intensity at (r,c) to "intensity"
	if (r > this->height || c > this->width)
	{
		return;
	}

	this->data[r][c] = intensity;
}

void Image::setData(unsigned int const rowSize, unsigned int const colSize, unsigned int pixelIntensity)
{
  //clear the contents of the member variable data, resize it to [rowSize, colSize]
  //and initialize all the pixel intensities to "pixelIntensity"
	this->empty = false;
	this->height = rowSize;
	this->width = colSize;
	this->data.resize(rowSize, vector<unsigned>(colSize, pixelIntensity));
}

unsigned int Image::getHeight() const { return this->height; }
unsigned int Image::getWidth() const { return this->width; }
bool Image::isEmpty() const { return this->empty; }
vector< vector<unsigned int> > Image::getData() const { return this->data; }
