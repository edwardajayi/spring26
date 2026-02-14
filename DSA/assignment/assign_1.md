# Assignment 1: Cryptographic Key Analysis on 2-DES

**Objective**: Implement a program to sort cryptographic keys using a stable O(N log N) algorithm (Merge Sort) and analyze the complexity. **NO STL ALLOWED.**

## 1. Project Structure
The following structure is strictly required:
```
YourAndrewID/
│
├── bin/          # Executables go here
├── build/        # CMake build artifacts
├── data/
│   ├── input.txt
│   └── output.txt
├── src/
│   ├── main.cpp
│   └── key_analysis.h  (Header file)
├── CMakeLists.txt
└── yourAndrewID_1.pdf  (Report)
```

## 2. Implementation Steps

### Step 1: Data Structure (`key_analysis.h`)
Create a struct `KeyEntry` with:
- `int index`: The original line number/ID.
- `unsigned int key`: The hexadecimal key value.

### Step 2: File I/O (`main.cpp`)
- **Reading**: 
    - Open `data/input.txt`.
    - Read `N` (number of keys).
    - Dynamically allocate array: `new KeyEntry[N]`.
    - Read `N` lines. Parse hex strings (e.g., `0x00FF`) to `unsigned int`.
    - *Tip*: Use `d` for int and `x` for hex parsing if using `fscanf`, or `std::hex` if using `iostream` (but `iostream` is part of standard library, `vector` is STL. `iostream` is usually allowed, `vector` is not. To be safe/pure, C-style `FILE*` is often safer for "No STL" logic, but C++ `fstream` is not STL containers. We will stick to standard C++ IO but NO containers).

### Step 3: Merge Sort (The Core Task)
**Constraints**: O(N log N) worst-case, Stable.
- Implement `mergeSort(arr, left, right)`.
- Implement `merge(arr, left, mid, right)`.
- **Stability Rule**: When `leftArr[i].key == rightArr[j].key`, choose `leftArr[i]` to preserve original relative order.

### Step 4: Output
- Open `data/output.txt`.
- Print your Andrew ID on the first line.
- Print sorted keys: `Index 0xKey` (formatted as hex).

## 3. Complexity Analysis & Report
- **Merge Sort**: O(N log N) time, O(N) auxiliary space.
- **Proof**: Show that for $m$ searches where $m > 1$, $O(N \log N) + m \times O(\log N)$ (Sort + Binary Search) is strictly better than $m \times O(N)$ (Repeated Linear Search).

## 4. Verification Plan
1.  **Sample Test**:
    - Input:
      ```
      5
      1 0x00FF
      2 0x12AB
      3 0x00FF
      4 0x0001
      5 0xABCD
      ```
    - Expected Output:
      ```
      [YourAndrewID]
      4 0x0001
      1 0x00FF
      3 0x00FF
      2 0x12AB
      5 0xABCD
      ```
2.  **Edge Cases**: `N=1`, Sorted, Reverse Sorted, All Equal.
