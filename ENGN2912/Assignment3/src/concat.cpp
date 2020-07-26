#include "concat.h"

using namespace std;

// TODO: Implement your "concat" function 

char* concat(char* str1, char* str2)
{
	unsigned len1{ 0 }, len2{ 0 };

	// calculate the effective length of the c-string

	while (str1[len1] != '\0')
	{
		len1++;
	}
	while (str2[len2] != '\0')
	{
		len2++;
	}

	char* concatStr = new char[len1 + len2 + 1];

	for (unsigned i{ 0 }; i < len1 + len2; i++)
	{
		if (i < len1)
		{
			concatStr[i] = str1[i];
		}
		else
		{
			concatStr[i] = str2[i - len1];
		}
	}

	concatStr[len1 + len2] = '\0';

	return concatStr;
}
