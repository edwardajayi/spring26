# File I/O in C++

## The C-Style Approach: Mastering fprintf & fscanf

### Why Use File I/O?

File I/O (Input/Output) is a critical concept in programming for several reasons:

1.  **Persistence**:
    *   Standard input/output (like the console) is volatile, meaning data is lost once the program finishes running.
    *   Files allow data to persist beyond the program's execution, storing it permanently on the disk.

2.  **Volume**:
    *   It is essential for processing large datasets.
    *   In Data Structures & Algorithms (DSA), you often deal with datasets containing 10,000+ lines, which is impractical to enter manually via the console.

3.  **Automation**:
    *   File I/O allows your code to read test cases automatically.
    *   This eliminates the need for manual typing and ensures consistent testing with the same data.

## The C++ Setup

### 1. The Header

In C++, we use the `<cstdio>` header to access C-style input/output functions. This is the C++ equivalent of C's `<stdio.h>`.

```cpp
#include <cstdio>
```

### 2. The Handle

We manipulate files using a **File Pointer**. It acts as a handle to the file stream.

```cpp
FILE *fp;
```

**Note**: `fp` is just a variable name, but the type must be `FILE *`.

## Opening a File

### Syntax: fopen

Use the `fopen` function to initialize the file pointer.

```cpp
fp = fopen("data.txt", "r");
```

### Common Modes:

*   `"r"` : **Read** (File must exist)
*   `"w"` : **Write** (Creates new file or overwrites)
*   `"a"` : **Append** (Adds to the end of file)

## Writing to Files

### Function: fprintf

Think of it as "File Print Formatted". It works exactly like `printf`, but takes the file pointer as the first argument.

It sends formatted text directly into the file stream you opened with `"w"` or `"a"` mode.
