#ifndef __DNAFINDPATTERN_H
#define __DNAFINDPATTERN_H

#include <string>
#include <iostream>
#include <fstream>
#include <vector>
#include <regex>

#include <boost/filesystem.hpp>

#define DEBUG

namespace fs = boost::filesystem;
boost::system::error_code ec;

// stores
// string 	-> the matched regular expression,
// unsigned -> the line number where the expression is matched (use indexing starting from 1 NOT 0),
// unsigned -> the starting character position where the expression is matched (use indexing starting from 1 NOT 0),
typedef std::tuple<std::string, unsigned, unsigned> dnaPatternContainer;

using std::cout;
using std::cin;
using std::endl;
using std::cerr;

/*
 * dnaPattern:  searches for patterns within a data file containing ASCII strings of DNA sequences
 *
 * Methods:
 *	dnaPattern()													// default constructor
 *	dnaPattern(filename)									// alternate constructor to set the file name
 *	dnaPattern(filename, pattern)					// alternate constructor to set the file name and regex string, update the isPatternSet_ flag
 *	setFilename(filename)									// clear the searchResults_ vector and update the file name string
 *	setPattern(pattern)										// clear the searchResults_ vector, update the regex string and the isPatternSet_ flag
 *	search()															// execute regex search for the specified pattern
 *  operator[]														// a random access operator to the searchResults_ vector
 *
 * Member Variables:
 *  boost::filesystem::path filename_									// the file to be processed
 *	regex regexPattern_																// a regular expression pattern that is specified by the user
 *	std::vector<dnaPatternContainer> searchResults_		// a vector pointing to locations in the file where the pattern exists (use indexing starting from 1 NOT 0)
 *  bool isPatternSet_ 																// a boolean variable to check whether a valid regex pattern is set
 */
class dnaPattern {
public:
	dnaPattern()
	{
	}
	dnaPattern(fs::path fname)
	{
		
		this->filename_ = fname;
	}
	dnaPattern(fs::path fname, std::regex patt)
	{

		this->filename_ = fname;
		this->regexPattern_ = patt;

		isPatternSet_ = true;
	}
	void setFilename(std::string fname)
	{

		try
		{
			fs::path fPath(fname);
			if (fs::exists(fPath) && fs::is_regular_file(fPath))
			{
				this->filename_ = fPath;
			}

			//clear vector of search results
			searchResults_.clear();
			isValid_ = true;

		}
		catch (...)
		{
			std::cout << "The path doesn`t exsit! Please check!" << std::endl;
			return;
		}
	}
	void setPattern(std::string patt)
	{

		try
		{
			std::regex expression(patt);
			this->regexPattern_ = expression;
			//clear vector of search results
			searchResults_.clear();
			isValid_ = true;
			isPatternSet_ = true;
		}
		catch (...)
		{
			std::cout << "Can`t generate regular expression! Please check!" << std::endl;
			return;
		}
	}
	void search(); // Decleration, add the implementation below
	dnaPatternContainer &operator[](unsigned k)
	{
		// check whether k is in range
		if (k > searchResults_.size())
		{
			std::cout << "The index is out of range!" << std::endl;
			
			static dnaPatternContainer dummyContainer;
			return dummyContainer;
		}

		return searchResults_[k];
		// the following lines are here for error-free compilation and need not be part of the solution, could be modified
		//static dnaPatternContainer dummyContainer;
		//return dummyContainer;
	}
	std::vector<dnaPatternContainer> getSearchResults()
	{
		// TODO: add implementation
		
		return searchResults_;
	}

	bool isValid()
	{
		return isValid_;
	}

private:
	fs::path filename_ = "";
	std::regex regexPattern_;
	std::vector<dnaPatternContainer> searchResults_;
	bool isPatternSet_ = false;
	bool isValid_ = true;
};

void dnaPattern::search()
{
// TODO: add implementation
	fs::path fPath;
	//get path of the input data
	fPath = this->filename_;

	//check whether the regular expression has been set
	while (!isPatternSet_)
	{
		std::cout << "The regular expression hasn`t been set! Please input a valid one!" << std::endl;

		std::string temp;

		std::cin >> temp;

		setPattern(temp);
	}

	//create regex expression
	std::regex expression(regexPattern_);
	
	//initialize the rowNum and colNum
	int rowNum{ 1 }, colNum{1};
	
	//if the direction is valid
	if (fs::exists(fPath))
	{
		//read in data
		boost::filesystem::fstream fstream(fPath);
		std::string temp;

		//iterate the whole file and read one line at one time
		while (getline(fstream, temp))
		{
			//check whether there are any invalid characters
			unsigned pos = temp.find_first_not_of("ATGC");

			if (pos <temp.size())
			{
				std::cout<< pos << "The data has invalid character!" << endl;
				searchResults_.clear();

				isValid_ = false;
				//searchResults_.resize(0);

				return;
			}
			
			//begin matching
			std::regex_iterator<std::string::const_iterator> begin(temp.cbegin(),temp.cend(),regexPattern_);

			for(auto iter = begin; iter!= std::sregex_iterator();iter++)
			{
				std::string foundString = iter->str();
				colNum = temp.find(foundString)+1;

				dnaPatternContainer newTuple = std::make_tuple(iter->str(),rowNum,colNum);

				searchResults_.push_back(newTuple);


			}
			//increase the row number
			rowNum++;
			
		}
		
		//close the file
		fstream.close();
	}
	else
	{
		return;
	}
}


/*
 * dnaFindPattern:  wrapper function to dnaPattern class that accepts std::strings
 *
 * Input:
 *		strPath			// an absolute/relative path to a directory or a specific file
 *		strPattern	// a regular expression string
 *
 * Output:
 * 		vector<dnaPattern> - a vector of dnaPattern objects (one per file searched)
 *
 * Note:
 * Only return an object for a file that was successfully searched.
 * Even if the search could not find the regular expression contained in the file an object needs to be returned.
 */
std::vector<dnaPattern> dnaFindPatterns(std::string strPath, std::string strPattern){

//vector to store searching result 
	std::vector<dnaPattern> result;

	fs::path path(strPath);

	#ifdef DEBUG
		std::cout<<path.string()<<endl;
	#endif

	//get the current directory for relative path
	fs::path currentPath = fs::current_path();

	//check whether the path exsits
	while (!fs::exists(path))
	{
		std::cout << "The path doesn`t exsit! Please input a valid one!" << std::endl;

		std::string temp;

		std::cin >> temp;

		fs::path input(temp);

		path = input;

	}
	//save the final string for path
	std::string finalPathString = path.string();

	
	//check whether the regular expression is valid
	bool isExpressionValid{ false };

	std::string temp{ strPattern };

	std::regex expression;

	while (!isExpressionValid)
	{
		//check whether the pattern is valid
		try
		{
			std::regex input(temp);

			isExpressionValid = true;

			expression = input;
		}
		catch (...)
		{
			std::cout << "Can`t generate regular expression! Please input a valid one!" << std::endl;
			
			std::cin >> temp;		
		}
	}
	//save the final result of regular expression
	std::string finalRegularString = temp;
	
	//check whether the path is a directory
	if (fs::is_directory(path))
	{
		fs::recursive_directory_iterator begin(path);
		fs::recursive_directory_iterator end;
		
		//loop all the data file in the directory
		for (; begin != end; ++begin)
		{
			if (fs::is_directory(*begin))
			{
				//continue if the current path is still a directory
				continue;
			}
			else
			{
				//judge if it`s a regular file
				if (fs::is_regular_file(*begin))
				{
					std::string strDataPath = begin->path().string();
					//check whether the file is a .data file

					if (strDataPath.find(".data",0) == std::string::npos)
					{
						std::cout << "The current file is not a vaild .data file. This search will be skipped!" << endl;
						continue;
					}

					//define a new dnaPattern
					dnaPattern newDnaPattern;

					//set path and pattern
					newDnaPattern.setFilename(finalPathString);
					newDnaPattern.setPattern(finalRegularString);
					//begin search
					newDnaPattern.search();

					if (!newDnaPattern.isValid())
					{
						std::cout << "The data has invalid characters!" << endl;
						continue;
					}

					if (newDnaPattern.getSearchResults().size() == 0)
					{
						std::cout << "Nothing found!" << endl;
					}

					//save search result
					result.push_back(newDnaPattern);
				}
			}
		}
	}
	else
	{
		if (fs::is_regular_file(path))
		{

			//check whether the file is a .data file
			if (finalPathString.find(".data", 0) == std::string::npos)
			{
				std::cout << "The current file is not a vaild .data file. This search will be skipped!" << endl;
				return result;
			}

			//define a new dnaPattern
			dnaPattern newDnaPattern;

			//set path and pattern
			newDnaPattern.setFilename(finalPathString);
			newDnaPattern.setPattern(finalRegularString);
			//begin search
			newDnaPattern.search();

			if (!newDnaPattern.isValid())
			{
				std::cout << "The data has invalid characters!" << endl;
				return result;
			}

			if (newDnaPattern.getSearchResults().size() == 0)
			{
				std::cout << "Nothing found!" << endl;
			}
			//save search result
			result.push_back(newDnaPattern);
			
		}
	}

	return result;
}

#endif // __DNAFINDPATTERN_H
