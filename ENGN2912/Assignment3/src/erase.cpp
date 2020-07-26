#include "erase.h"

// TODO: Implement your "erase" function 
#include "erase.h"
#include "concat.h"
#include "substr.h"

using namespace std;

// TODO: Implement your "erase" function 
unsigned getLength(char*);
char* getSub(char*, unsigned, unsigned);
char* getSub(char*, unsigned);


char* erase(char* str1, char* str2)
{
	unsigned start;
	unsigned end;
	unsigned len1{ getLength(str1) };
	unsigned len2{ getLength(str2) };

	bool isSub = substr(str1, str2, start);

	if (!isSub)
	{
		return str1;
	}

	char* temp1 = getSub(str1, 0, start);
	char* temp2 = getSub(str1, start + len2);

	char* result = concat(temp1, temp2);

	return result;

}

unsigned getLength(char* str)
{
	unsigned len{ 0 };

	while (str[len] != '\0')
	{
		len++;
	}

	return len;
}

char* getSub(char* str, unsigned start, unsigned length)
{
	unsigned len = getLength(str);

	if (start >= len)
	{
		return new char[1]{ '\0' };
	}
	if (length == 0)
	{
		return new char[1]{ '\0' };
	}

	char* result = new char[length + 1];

	for (unsigned i{ 0 }; i < length; i++)
	{
		result[i] = str[start + i];
	}

	result[length] = '\0';

	return result;
}

char* getSub(char* str, unsigned start)
{
	unsigned len = getLength(str);

	if (start >= len)
	{
		return new char[1]{ '\0' };
	}


	char* result = new char[len - start + 1];

	for (unsigned i{ start }; i < len; i++)
	{
		result[i - start] = str[i];
	}

	result[len - start] = '\0';

	return result;
}
