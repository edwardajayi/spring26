#ifndef KEY_ANALYSIS_H
#define KEY_ANALYSIS_H

// Part 3, Step 1: Define a Data Structure
struct KeyEntry {
    int id;             // Key Index
    unsigned int key;   // Cryptographic Key (stored as hex/unsigned int)
};

// Function Prototypes

/**
 * Reads the input file.
 * @param filename Path to input file.
 * @param n Reference to store the number of keys.
 * @return Pointer to dynamically allocated array of KeyEntry.
 */
KeyEntry* readInput(const char* filename, int& n);

/**
 * Writes the sorted keys to the output file.
 * @param filename Path to output file.
 * @param keys Array of KeyEntry.
 * @param n Number of keys.
 */
void writeOutput(const char* filename, KeyEntry* keys, int n);

/**
 * Standard Merge Sort implementation (Stable).
 * @param keys Array to sort.
 * @param left Start index.
 * @param right End index.
 */
void mergeSort(KeyEntry* keys, int left, int right);

/**
 * Helper function to merge two sorted subarrays.
 * Ensures stability by preferring left elements on equality.
 */
void merge(KeyEntry* keys, int left, int mid, int right);

#endif // KEY_ANALYSIS_H
