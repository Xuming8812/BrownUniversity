#include "ImageDenoiser.h"
#include <iostream>
#include <algorithm>

using namespace std;

//constructor and destructor are provided
ImageDenoiser::ImageDenoiser(unsigned int const filterHeight, unsigned int const filterWidth)
{
  this->hFilter = filterHeight;
  this->wFilter = filterWidth;
}

ImageDenoiser::~ImageDenoiser(){}

bool ImageDenoiser::denoiseImage(Image const& inputImage, Image& outputImage)
{
  //if the inputImage is empty cout a warning and return false`
  //else resize the member variable data of outputImage to the same size as inputImage and apply median filter, if successful return true
	if (inputImage.isEmpty())
	{
		cout << "Warning: The image is empty!" << endl;

		return false;

	}

	int rowNum = inputImage.getHeight(), colNum = inputImage.getWidth();
	int halfFilterHeight = (this->hFilter - 1) / 2, halfFilterWidth = (this->wFilter - 1) / 2;
	//resize the outputImage

	outputImage.setData(rowNum, colNum, 0);

	for (int i{ 0 }; i < rowNum; ++i)
	{
		for (int j{ 0 }; j < colNum; ++j)
		{
			vector<unsigned> store;

			for (int m = i - halfFilterHeight; m <= i + halfFilterHeight; ++m)
			{
				for (int n = j - halfFilterWidth; n <= j + halfFilterWidth; ++n)
				{
					if (m >= 0 && m < rowNum && n >= 0 && n < colNum)
					{
						store.push_back(inputImage.getPixelIntensity(m, n));
					}
				}
			}

			int index = store.size() / 2;

			if (store.size() == 0)
			{
				index = 0;
			}

			std::sort(store.begin(), store.end());

			outputImage.setPixelIntensity(i, j, store[index]);
		}
	}

	return true;
  return false;
}
