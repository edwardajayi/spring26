/*
 * homework.cpp
 */

#include "homework.h"

int main(int argc, char** argv) {
	LogManager::resetLogFile();
	LogManager::writePrintfToLog(LogManager::Level::Status, "hw01::processFile", "In main file.");

#if 0
	/**
	 * This is bad at multiple levels should not be done.
	 * Why?
	 *
	 * 1. inputPath does not have a defined size.
	 *
	 * 2. What is the guarantee that argv[1] stores valid entries?
	 *
	 * 3. You will be passing this pointer to another function.
	 *    What if you run out of memory?
	 */
	char *inputPath = argv[1];
	char *outputPath = argv[2];
#elif USE_MALLOC
	/**
	 * By ensuring strings of specific size, you make sure that
	 * the memory consumed is known, and no illegal inputs are passed.
	 */
	char *inputPath = (char*) malloc(sizeof(char) * 1024);
	char *outputPath = (char*) malloc(sizeof(char) * 1024);
#elif USE_NEW
	/**
	 * By ensuring strings of specific size, you make sure that
	 * the memory consumed is known, and no illegal inputs are passed.
	 */
	char *inputPath = new char[1024];
	char *outputPath = new char[1024];
#else
	/**
	 * This is creating variables on a stack. What are the pros/cons of
	 * creating variables in stack vs heap?
	 */
	char inputPath[1024];
	char outputPath[1024];
#endif

	/**
	 * When you initiate a memory call, always check that the memory was allotted
	 * If not, throw an error, or send an error message.
	 */
	if (!inputPath){
		printf("allocation of inputPath failed\n");
		return -1;
	}
	if (!outputPath){
		printf("allocation of outputPath failed\n");
		return -1;
	}

	int peakMem1 = getPeakRSS();
	int currMem1 = getCurrentRSS();
	printf("peakRSS = %d, currMem=%d\n", peakMem1, currMem1);
	printf("sizeof(bool) = %d \n", (int)sizeof(bool));
	printf("sizeof(int) = %d \n", (int)sizeof(int));
	printf("sizeof(char) = %d \n", (int)sizeof(char));
	printf("INT_MIN = %d, INT_MAX =%d\n", INT_MIN, INT_MAX);

	auto start = std::chrono::high_resolution_clock::now();

	char inputPath[1024], outputPath[1024];
	sprintf(inputPath, "%s", argv[1]);
	sprintf(outputPath, "%s", argv[2]);
	BitVector::testWithFile(inputPath, outputPath);

	char path[6] = {"/tmp/"};
	//BitVector::generateTestCases(path);
	auto stop = std::chrono::high_resolution_clock::now();

	auto duration = std::chrono::duration_cast<std::chrono::microseconds>(stop - start);
	printf("run time =%d microseconds\n", (int) duration.count());


	int peakMem2 = getPeakRSS();
	int currMem2 = getCurrentRSS();
	printf("peakRSS = %d, currMem=%d\n", peakMem2, currMem2);
	printf("Diff peakRSS = %d, currMem=%d\n", peakMem2-peakMem1, currMem2-currMem1);

	int peakMem3 = getPeakRSS();
	int currMem3 = getCurrentRSS();
	printf("peakRSS = %d, currMem=%d\n", peakMem3, currMem3);
	printf("Diff peakRSS = %d, currMem=%d\n", peakMem3-peakMem2, currMem3-currMem2);

#if USE_MALLOC
	free(inputPath);
	free(outputPath);
#endif

#if USE_NEW
	delete [] inputPath;
	delete [] inputPath;
#endif
}
