# Abstract Data Types (ADT)

## Introduction to Abstract Data Types

In computer science, an **Abstract Data Type (ADT)** is a theoretical model for data types. The key to understanding ADTs lies in the word "abstract." It means that the data type is defined by its *behavior* (semantics) from the point of view of a user/client, rather than by its *implementation* within the computer.

An ADT specifies:
1.  **The complete set of values** that a variable of this type can assume.
2.  **The complete set of operations** that can be performed on these values.

Crucially, this specification is made **without reference to the underlying implementation**. The user of an ADT knows *what* the data type does, but not necessarily *how* it does it. This separation of interface from implementation is the essence of **information hiding**.

---

## Core Characteristics

### 1. Value Definition
An ADT restricts the domain of values. For example, a boolean ADT can only hold `true` or `false`. An Integer ADT holds whole numbers within a specific range.

### 2. Operation Definition
The ADT defines the valid operations. For a Stack ADT, operations might include `push`, `pop`, `peek`, and `isEmpty`. The definition includes the input parameters for each operation, the output (return value), and the effect on the ADT's state (pre-conditions and post-conditions).

### 3. Abstraction (Implementation Independence)
This is the most critical feature. The behavior is mathematical or logical.
*   **Example**: A "List" ADT can be implemented using a purely array-based approach or a linked-list approach.
*   **The User's Perspective**: The user calls `list.add(item)`. They do not care if the internal mechanism involves incrementing an array index or allocating a new heap node and updating pointers. They only care that the item is added.

### 4. Information Hiding
By hiding the complexity of the implementation, we achieve several benefits:
*   **Simplicity**: The user interacts with a clean interface.
*   **Maintainability**: The implementation can change (e.g., for optimization) without breaking the code that uses the ADT, as long as the interface remains the same.
*   **Security**: Internal data structures are protected from invalid or malicious states that a user might accidentally induce if they had direct access.

---


---

## Why We Need OOP (Object-Oriented Programming)

While we *can* implement ADTs in C using structs and pointers (as shown above), **Object-Oriented Programming (OOP)** is the paradigm that truly provides the mechanisms to **enforce** these properties automatically.

### 1. Unified Logical Definition (Encapsulation)
OOP allows us to combine (encapsulate) both the data specification and the operation specification into **one logical definition**:
*   **Class Definition**: Acts as the blueprint.
    *   **Data Members**: The state/values.
    *   **Methods**: The function members/operations.
*   **Objects**: These are instantiated classes.

In C, the data (`struct`) and operations (`functions`) are separate. In OOP (C++, Java, Python), they are bound together in the class.

### 2. Beyond Basic Encapsulation
OOP provides much more than just grouping:
*   **Access Modifiers**: Keywords like `private`, `protected`, and `public` *enforce* information hiding. In C, a user can often still access struct members if they really want to. In C++, `private` members strictly forbid access.
*   **Inheritance**: Allows us to create new ADTs based on existing ones (extending behavior without rewriting code).
*   **Polymorphism**: Allows different ADTs to be treated as a common type (e.g., a `Circle` and `Square` both treated as `Shape`).

---

## Typing and Data Types

To understand ADTs, we must distinguish them from native types.

### Native Data Types
These are built into the programming language (e.g., `int`, `float`, `char`, `boolean`).
*   **Purpose**: Typing is necessary for the computer to understand how to interpret bit patterns in memory. It tells the compiler/interpreter how much memory to allocate and how to perform arithmetic or logical operations on that memory.

### ADTs (Programmer-Defined Types)
ADTs are created by programmers using native types or other existing ADTs.
*   **Purpose**: They are designed to model complex concepts (like a "Student," a "Bank Account," or a "Graph") while hiding the complexity of their composition.

---

## Summary: The Role of an ADT

An ADT acts as a contract between the creator of the type and the user of the type.

1.  **Hides Complexity**: It conceals the details of how information is stored (e.g., in a binary tree vs. a hash table) and how operations are algorithmically performed.
2.  **Exposes Services**: It provides a public API (Application Programming Interface) consisting of methods to access, add, delete, manipulate, and transform data.
3.  **General Utility**: Well-designed ADTs are often generic and reusable. A `Queue` ADT, for instance, is designed to handle the logic of "First-In-First-Out" regardless of whether it stores integers, strings, or complex user objects. This generality creates 
---

## ADT Design Goals

The primary goal in designing an ADT is to **hide complexity** and implementation details.

### 1. Encapsulation
Encapsulation is the principle of bundling data and operations into a single logical unit ("capsule").
*   **Hide**: The internal data structure, algorithms, and resource allocation logic.
*   **Expose**: A well-defined interface (services) that allows programmers to access and manipulate data.

### 2. Key Design Decisions
When designing an ADT, we must decide:
*   **What to hide**: Operational details that the user doesn't need to see.
*   **What to expose**: The minimum set of operations required for the application.
*   **Internal Structure**: How to allocate resources (static vs dynamic), what primitive types to use, and how elements relate to each other.

### 3. Correctness
Since potentially many applications will depend on a single ADT (e.g., a standard String class), it must work correctly for **all possible inputs**.

---



### Practical Example: C++ Struct (Memory Layout)
Here is a specific code example using character arrays for the fields, which is common in legacy C/C++ or embedded contexts where memory is tightly controlled. 

```cpp
struct Student {
    char id[10];        // 10 bytes: Stores an ID like "S12345678\0"
    char firstName[20]; // 20 bytes: Name + null terminator
    char lastName[20];  // 20 bytes
    char dob[11];       // 11 bytes: Strictly "YYYY-MM-DD\0"
    float gpa;          // 4 bytes: Standard float
};
```

### Minimum Byte Usage Calculation
Let’s break down the minimum memory required for a single variable of type `Student`:

1.  **id** (`char[10]`): **10 bytes**
2.  **firstName** (`char[20]`): **20 bytes**
3.  **lastName** (`char[20]`): **20 bytes**
4.  **dob** (`char[11]`): **11 bytes**
5.  **gpa** (`float`): **4 bytes**

**Total Minimum Size:**
$$ 10 + 20 + 20 + 11 + 4 = 65 \text{ bytes} $$

> **Important:** This calculation represents the *sum of the members*. In practice, the compiler may add "padding" bytes between members (e.g., after the `dob` array to align the `float` on a 4-byte boundary). So the actual `sizeof(Student)` in memory might be slightly larger (e.g., 68 bytes), but the logical data content is 65 bytes.

> **Wait, isn't a char 2 bytes?**
> You might be thinking of languages like **Java** or **C#**, where `char` is **2 bytes** to support Unicode (UTF-16) natively. In **C++**, a standard `char` is defined as **1 byte** (usually 8 bits). If you need to store larger characters for international languages, C++ uses `wchar_t` (2 or 4 bytes), `char16_t`, or `char32_t`. For standard ASCII text, `char` is always **1 byte**.

---

## Memory Optimization: Handling Padding & Ordering

You asked a critical question: *Is there a way we should handle the ordering in struct so as to handle padding and memory space allocation?* **YES.**

The order of members in a struct significantly impacts its total size due to **alignment**.

### The Rule of Thumb
**Order your struct members from largest alignment requirement (usually largest size) to smallest.**
1.  Pointers (8 bytes on 64-bit systems)
2.  `double` / `long long` (8 bytes)
3.  `int` / `float` (4 bytes)
4.  `short` (2 bytes)
5.  `char` (1 byte)

### Example: Why Ordering Matters

Consider this "Bad" struct:
```cpp
struct BadOrder {
    char a;     // 1 byte
                // [3 bytes padding to align 'b' to 4-byte boundary]
    int b;      // 4 bytes
    char c;     // 1 byte
                // [3 bytes padding to align total struct size to multiple of 4]
}; 
// Total Size: 1 + 3 + 4 + 1 + 3 = 12 bytes
```

Now, the "Good" struct (reordered by size):
```cpp
struct GoodOrder {
    int b;      // 4 bytes
    char a;     // 1 byte
    char c;     // 1 byte
                // [2 bytes padding to align total struct size to multiple of 4]
};
// Total Size: 4 + 1 + 1 + 2 = 8 bytes
```

By simply reordering, we saved **33%** of the memory (4 bytes per instance). In an array of a million structs, that’s 4MB of RAM saved!

---


---

## Implementation Example: The Stack (From Lecture Slides)

Let's dissect the code from your slides to understand how ADTs can be implemented in C.

### 1. The Concrete Implementation (Struct)
This version exposes the full structure to the user.

```c
#define SIZE 500
struct SomeStructType {       /* stack is implemented as */
    char items[SIZE];         /* an array of items */
    int num;                  /* number of items */
};
typedef struct SomeStructType MyType; /* struct type */
MyType stack;                 /* stack is a struct data structure */
```

**Explanation:**
1.  `#define SIZE 500`: A constant defines the maximum capacity. This is a **static allocation** decision.
2.  `struct SomeStructType`: This defines the *implementation details*. It reveals that the stack is built using an array (`items`) and an integer counter (`num`).
3.  `typedef ... MyType`: This gives the struct a new alias, `MyType`. This looks like an ADT name, but...
4.  `MyType stack`: When the user declares a variable `stack`, the compiler allocates the **full 504 bytes** (500 for char + 4 for int based on our earlier math) right there.
    *   **Pro**: Fast allocation (on the stack frame).
    *   **Con**: If the implementation changes (e.g., `SIZE` becomes 1000), the user's code must be recompiled because the size of `MyType` has changed.

### 2. The Abstract Implementation (Pointer/Handle)
This version hides the details behind a pointer, offering better encapsulation.

```c
#define SIZE 500
struct SomeStructType {       /* stack is implemented as */
    char items[SIZE];         /* an array of items */
    int num;                  /* number of items */
};
typedef struct SomeStructType *MyType; /* pointer type */
MyType stack;                 /* variable is a pointer to a stack */
```

**Key Difference:**
Notice the `*` in the typedef: `typedef struct SomeStructType *MyType;`

**Explanation:**
1.  `MyType stack`: Now, when the user declares `stack`, they only allocate a **pointer** (usually 8 bytes).
2.  **Information Hiding**: The user holds a "handle" (`stack`) to the data structure, but they don't necessarily know or care how big the structure is.
3.  **Flexibility**: The implementation could change completely (e.g., to a linked list), and as long as `MyType` remains a pointer, the user's compiled code might not even need to know the size of the underlying struct if they only interact with it via functions.

