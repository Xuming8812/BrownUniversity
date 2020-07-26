#include "substr.h"
using namespace std;
// TODO: Implement your "substr" function 
bool substr(char* str1, char* str2, unsigned& pos)
{
	unsigned len1{ 0 }, len2{ 0 };

	// calculate the effective length of the c-string
	bool result{ false };

	while (str1[len1] != '\0')
	{
		len1++;
	}
	while (str2[len2] != '\0')
	{
		len2++;
	}

	if (len2 > len1)
	{
		pos = 0;
		return false;
	}

	for (unsigned i{ 0 }; i < len1; i++)
	{
		if (i + len2 - 1 >= len1)
		{
			pos = 0;
			return false;
		}

		if (str1[i] == str2[0])
		{
			for (unsigned j{ 1 }; j < len2; j++)
			{
				if (str1[i + j] == str2[j])
				{
					if (j == len2 - 1)
					{
						pos = i;
						return true;
					}

				}
				else
				{
					pos = 0;
					result = false;
					break;
				}
			}
		}
	}

	return result;
}
