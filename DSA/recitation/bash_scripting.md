# Bash Scripting Recitation Notes

This document covers the core concepts of Bash scripting as presented in the recitation. It explains input/output, conditionals, loops, functions, and text processing utilities like `awk` and `sed`.

---

## 1. Input/Output Redirection & Word Count
**(Recitation Slide/Section 10)**

Bash allows you to control where input comes from and where output goes.

### Reading from a file
*   **Command**: `wc -w` (Word Count - words).
*   **Standard usage**: `wc -w hello.txt`
    *   Here, `hello.txt` is passed as an *argument* to the command.
*   **Redirection usage**: `wc -w < hello.txt`
    *   Here, `<` redirects the *contents* of `hello.txt` into the command's standard input (stdin).

### Heredoc `<<`
*   **Symbol**: `<<`
*   **Usage**: Used for providing multiple lines of input to a command directly from the script (not from a separate file).
    ```bash
    cat << EOF
    Line 1
    Line 2
    EOF
    ```

---

## 2. Conditionals (`if`/`elif`/`else`)
**(Recitation Slide/Section 11)**

Conditions allow scripts to make decisions.

### Comparison Operators
*   `<`, `>`, `==`, `!=` are used inside `[[ ... ]]` or `(( ... ))` (for arithmetic).
*   **Note**: Inside standard `[ ... ]` brackets:
    *   `=` or `==` checks string equality.
    *   `-eq`, `-lt`, `-gt` are used for integers.

### Parameter Expansion Example
*   **Code**: `${1,,} = John`
    *   `${1}` is the **first argument** passed to the script.
    *   `,,` is a case modification operator (Bash 4.0+) that converts the value to **lowercase**.
    *   This checks if the first argument (case-insensitive) is "john".

### Syntax
```bash
# Check if condition is true
if [ <condition> ]; then
    echo "Hello world! I’m a DSA Expert"
fi
```
*   **Important**: Spaces are required inside the brackets `[ ]`. `[condition]` will fail; `[ condition ]` works.

---

## 3. Switch Case (`case`)
**(Recitation Slide/Section 12)**

Instead of writing many `if`/`elif`/`elif` statements, usage `case` to verify a variable against a list of patterns.

### Syntax
```bash
case <variable> in
    <check1>) 
        # do something 
        ;;
    <check2>) 
        # do something else 
        ;;
    *) 
        # Default case (matches anything else)
        ;;
esac
```
*   `case ... in`: Starts the block.
*   `pattern)`: Ends with a closing parenthesis.
*   `;;`: Terminates the specific block (like `break` in C++).
*   `esac`: Ends the case statement (case spelled backwards).

---

## 4. Arrays
**(Recitation Slide/Section 13)**

Arrays hold multiple objects. In Bash, these are often strings separated by space.

### Defining an Array
```bash
# Correct syntax: NO spaces around the equal sign!
MY_ARRAY=(one two three four)
```

### Accessing Values
1.  **First Element**: 
    ```bash
    echo ${MY_ARRAY}    # Outputs: one
    echo ${MY_ARRAY[0]} # Outputs: one (Same as above)
    ```
2.  **All Elements**:
    ```bash
    echo ${MY_ARRAY[@]} # Outputs: one two three four
    ```

*   **Note**: In this context, "objects" refers to the individual strings "one", "two", etc.
*   Space is the default delimiter.

---

## 5. For Loops
**(Recitation Slide/Section 14)**

Used to reiterate through a list without manual control (automatic iteration).

### Syntax
```bash
# Loop through every item in the array
for item in ${MY_ARRAY[@]}; do
    # $item holds the current value
    echo $item
done
```

---

## 6. Functions
**(Recitation Slide/Section 15)**

Functions group commands into a reusable block.

### Definition
```bash
functionName() { 
    # do something ridiculous 
}
```

### Calling
```bash
functionName
```
*   **Parameters**: You do not define parameters in the parentheses like C++ `void foo(int x)`. Use `$1`, `$2` inside the function to access arguments.
    *   Example Call: `functionName arg1 arg2`
*   **Scope**: By default, variables defined inside a function are **global**. Use the keyword `local` to make them confined to the function.

---

## 7. Exit Codes
**(Recitation Slide/Section 16)**

Every command returns a numeric status code when it finishes.

*   `0` = **Success** (Everything went well).
*   `Non-zero` = **Error** (Something failed).
*   You check `echo $?` to see the exit code of the last command.

---

## 8. awk (Pattern Scanning & Processing)
**(Recitation Slide/Section 17)**

`awk` is a tool for filtering and processing text line-by-line.

### Basic Usage
```bash
awk '{print $1}' testfile.txt
```
*   Performs the action `{print $1}` on `testfile.txt`.
*   `$1`: Represents the **first column** (field).
*   **Default Separator**: White space (tabs or spaces).

### Custom Separator
```bash
awk -F, '{print $1}' testfile.txt
```
*   `-F,`: Sets the Field Separator to a **comma** (useful for CSVs).

---

## 9. sed (Stream Editor)
**(Recitation Slide/Section 18)**

`sed` is used for altering values in text files (Find & Replace).

### Syntax
```bash
sed 's/{c_from}/{c_to}/g' <filename>
```
*   `s`: **Substitute** mode.
*   `{c_from}`: The word/pattern to change **from**.
*   `{c_to}`: The word to change **to**.
*   `g`: **Global** scope (replace all occurrences in a line, not just the first).

### In-Place Editing
*   To actually modify the file (instead of just printing the change to screen), use the `-i` flag.
*   If you provide an extension to `-i`, it creates a backup.
    ```bash
    sed -i.bak 's/old/new/g' filename.txt
    ```
    *   Original file is duplicated to `filename.txt.bak` before it is altered.

---

## 10. Final Mini Project
**(Recitation Slide/Section 19)**

**Task**: Write a script to automatically build, compile, and run your program.

### Example Script
```bash
#!/bin/bash

# 1. Compile (Build)
g++ -o myProgram main.cpp

# 2. Check if compilation was successful (Exit code 0)
if [ $? -eq 0 ]; then
    echo "Compilation Success! Running program..."
    # 3. Run
    ./myProgram
else
    echo "Compilation Failed."
fi
```
