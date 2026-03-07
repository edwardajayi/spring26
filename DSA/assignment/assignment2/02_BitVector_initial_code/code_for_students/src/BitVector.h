#ifndef BITVECT_H_
#define BITVECT_H_

#include <iostream>
#include <fstream>
#include <limits.h>
#include <math.h>
#include <unistd.h>
#include "util/GetMemUsage.h"
#include "util/LogManager.h"

class BitArray{
public:
	BitArray(int numberOfBitsNeeded);

	/**
	 *  Set the value of the bit at a specific location.
	 */
    void setBit(int locationOfBit, bool bitValue);

    /**
     *  Get the value of the bit at a specific location.
     */
    bool getBit(int locationOfBit);
};


class BitVector{
	/**
	 * This function must take as input a file stream that is open, read the next line
	 * and return an integer if it is valid.
	 *
        a. If there are any lines with no inputs, those lines must be skipped.
        b. If there are any lines that contain a non-integer input, those lines must be skipped.
 	 	 If end of file is reached, it must throw an end of file error
	 */
	static int readNextItemFromFile(FILE* inputFileStream);
	/**
	 *
	 */
	static char generateRandomWhiteSpace(){
		const char charArray[3] = {' ', '\n', '\t'};
		int selectedIndx = rand()%(2);
		return charArray[selectedIndx];
	};

	/**
	 * Generate a string of random length
	 */
	static std::string genRandomString(int len) {
		char randomStr[len+1];
		for (size_t i = 0; i < len; ++i) {
			int randomChar = rand()%(26+26+10);
			if (randomChar < 26)
				randomStr[i] = ('a' + randomChar);
			else if (randomChar < 26+26)
				randomStr[i] = ('A' + randomChar - 26);
			else
				randomStr[i] = ('0' + randomChar - 26 - 26);
		}
		randomStr[len] = 0;
		std::string retStr = randomStr;
		return retStr;
	};

	/**
	 * Get a random int value between INT_MIN and INT_MAX
	 */
	static int genRandomInt() {
	    const int bitsNeededForRAND_MAX = (int)(log2(RAND_MAX/2 + 1) + 1.0); /* Or log(RAND_MAX + 1) / log(2) with older language standards */
	    int ret = 0;
	    for (int i = 0; i < sizeof(int) * CHAR_BIT; i += bitsNeededForRAND_MAX) {
	        ret <<= bitsNeededForRAND_MAX;
	        ret |= rand();
	    }
	    return ret;
	}

	/**
	 * Generate a random integer between min and max.
	 */
	static int getRandomInt(int min, int max){
		if (min == max)
			return min;
		if (min == INT_MIN && max == INT_MAX)
			return genRandomInt();
		if (max == INT_MIN && min == INT_MAX)
			return genRandomInt();

		int range = max - min + 1;
		if (min > max){
			range = min - max + 1;
		}
		static bool first = true;
		if (first){
			srand( time(NULL) ); //seeding for the first time only!
			first = false;
		}

		int randomNumber = genRandomInt();
		int withinRangeNum = (randomNumber % range);
		int value = min + withinRangeNum;
		LogManager::writePrintfToLog(LogManager::Level::Status,
				"BitVector::getRandomInt", "1 randomNumber=%d, min=%d, max=%d, range=%d, value=%d", randomNumber, min, max, range, value);

		// Under some conditions, it is possible that value is not within min and max.
		// for example, if (withinRangeNum < 0 && min < 0)
		if (false){
			if (value < min || value > max){
				value = getRandomInt(min, max);
				return value;
			}
		}else{
			int indx = 2;
			LogManager::writePrintfToLog(LogManager::Level::Status,
				"BitVector::getRandomInt", "1 withinRangeNum=%d", withinRangeNum);

			if (withinRangeNum < 0 && min < 0)
				withinRangeNum = withinRangeNum * -0.5;

			while (value < min || value > max){
				withinRangeNum = (min + withinRangeNum + max) / indx++;
				value = min + withinRangeNum;
				if (indx == 10)
					indx = 2;
				LogManager::writePrintfToLog(LogManager::Level::Status,
					"BitVector::getRandomInt", "1 withinRangeNum=%d, min=%d, max=%d, indx=%d, value=%d", withinRangeNum, min, max, indx, value);
			}
			return value;
		}

		LogManager::writePrintfToLog(LogManager::Level::Status,
				"BitVector::getRandomInt", "randomNumber=%d, min=%d, max=%d, range=%d, value=%d", randomNumber, min, max, range, value);
		LogManager::writePrintfToLog(LogManager::Level::Status,
				"BitVector::getRandomInt", "%d+ (%d mod %d)\n", min, randomNumber, range);
		return value;
	};
	/**
	 * This is the entry level function to generate test cases for BitVector.
	 *
	 * @param outputFilePath Path of the output file.
	 */
	static int generateTestCases(char* outputFilePath, int min, int max, int numberOfEntries, int errorTypes);

public:
	/**
	 * This is the entry level function that must read an input file and give the output as needed
	 * for HW02.
	 *
	 * @param inputFilePath Path of the input file.
	 * @param outputFilePath Path of the output file.
	 *
	 * If the input file cannot be read throw an error of type ios_base::failure
	 * If the output file cannot be generated, then throw an error of type ios_base::failure
	 */
	static int processFile(char* inputFilePath, char* outputFilePath);
	/**
	 * This is the entry level function to generate test cases for HW02.
	 *
	 * @param outputFilePath Path of the output file.
	 */
	static int generateTestCases(char* outputFilePath);
};

#endif /* BITVECT_H_ */
