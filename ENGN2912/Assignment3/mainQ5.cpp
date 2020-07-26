#include <iostream>
#include "concat.h"
#include "substr.h"
#include "erase.h"

using namespace std;

// TODO: 1) Add declarations in src/concat.h, src/substr.h, and src/erase.h
//       2) Add implementations in src/concat.cpp, src/substr.cpp, and src/erase.cpp
//       3) Write tests for your code below.

int main(){

	char str1[9] = { 'e', 'n', 'g', 'i','n','e','e','r', '\0' };
	char str2[7] = { 's', 'c', 'h', 'o', 'o', 'l','\0' };

	concat(str1, str2);

	unsigned pos = 0;

	substr(str1, str2, pos);
	char str3[5] = { 'h', 'o', 'o', 'l','\0' };
	substr(str2, str3, pos);

	char str4[4] = { 'h', 'o', 'o','\0' };

	char* result = erase(str2, str4);
	
	return 0;

}
