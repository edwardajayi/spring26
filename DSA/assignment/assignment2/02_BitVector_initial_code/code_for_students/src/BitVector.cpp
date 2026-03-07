#include "BitVector.h"

int BitVector::readNextItemFromFile(FILE* inputFileStream){
	if (! inputFileStream){
		char* message = new char[2048];
		sprintf(message, "Cannot open input file for reading");
		throw std::ios_base::failure(message);
		delete []message;
	}

}


int BitVector::processFile(char *inputFilePath, char *outputFilePath){
	FILE* inFileStream = fopen(inputFilePath, "r");
	if (! inFileStream){
		char* message = new char[2048];
		sprintf(message, "Cannot open input file for reading: %s", inputFilePath);
		throw std::ios_base::failure(message);
		delete []message;
	}

	FILE* outFileStream = fopen(outputFilePath, "w");
	if (! outFileStream){
		char* message = new char[2048];
		sprintf(message, "Cannot open output file for writing: %s", outputFilePath);
		throw std::ios_base::failure(message);
		delete []message;
	}

	LogManager::writePrintfToLog(LogManager::Level::Status, "BitVector::processFile", "Starting the processing");

	/*
	Your code to process a file should be written after these comments.
	*/

	fflush(outFileStream);
	fclose(outFileStream);

	fclose(inFileStream);
}

int BitVector::generateTestCases(char* outputFilePath, int min, int max, int numberOfEntries, int errorTypes){
	if (false)
		return 0;
	FILE* outFileStream = fopen(outputFilePath, "w");
	if (! outFileStream){
		char* message = new char[2048];
		sprintf(message, "Cannot open output file for writing: %s", outputFilePath);
		throw std::ios_base::failure(message);
		delete []message;
	}
	int currInt;
	int maxRandomToAddError = 5;
	for (int i=0; i< numberOfEntries; i++){
		currInt = getRandomInt(min, max);
		if (errorTypes == 0){
			fprintf(outFileStream, "%d\n", currInt);
		}
		if (errorTypes == 1){
			if (getRandomInt(0, maxRandomToAddError) == 3){
				int intNum = getRandomInt(0, maxRandomToAddError);
				float floatNum = ((float) intNum) / 100;
				fprintf(outFileStream, "%f\n", floatNum);
			}
			if (getRandomInt(0, maxRandomToAddError) == 2)
				fprintf(outFileStream, "%c", generateRandomWhiteSpace());
			fprintf(outFileStream, "%d\n", currInt);
		}

		if (errorTypes == 2){
			if (getRandomInt(0, maxRandomToAddError) == 2)
				fprintf(outFileStream, "%c\n", generateRandomWhiteSpace());
			fprintf(outFileStream, "%d\n", currInt);
		}

		if (errorTypes == 3){
			if (getRandomInt(0, maxRandomToAddError) == 2){
				std::string randomStr = genRandomString(3);
				fprintf(outFileStream, "%s\n", randomStr.c_str());
			}
			fprintf(outFileStream, "%d\n", currInt);
		}
	}
	fflush(outFileStream);
	fclose(outFileStream);
}

int BitVector::generateTestCases(char* outputFolderPath){
	char filePath[1024];
	int numElements;
	int minValue[2] = {-1023, INT_MIN};
	int maxValue[2] = {1023, INT_MAX};
	char dataType[2][5] = {"easy", "hard"};

	for (int k=0; k<2; k++){
		for (int i=0; i<4; i++){
			sprintf(filePath, "%s/%s_sample_0%d.txt", outputFolderPath, dataType[k], i+1);
			numElements = getRandomInt(500000, 800000);
			//numElements = 10;
			LogManager::writePrintfToLog(LogManager::Level::Status, "BitVector::generateTestCases",
				"numElements=%d", numElements);
			generateTestCases(filePath, minValue[k], maxValue[k], numElements, i);

			sprintf(filePath, "%s/%s_test_0%d.txt", outputFolderPath, dataType[k], i+1);
			numElements = getRandomInt(500000, 800000);
			LogManager::writePrintfToLog(LogManager::Level::Status, "BitVector::generateTestCases",
				"numElements=%d", numElements);
			generateTestCases(filePath, minValue[k], maxValue[k], numElements, i);
		}
	}
}
