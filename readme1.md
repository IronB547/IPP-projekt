# Implementation documentation for IPP project 1. 2021/2022

##### Name: Tomáš Dvořák
##### Login: xdvora3r

---

## Implementation details

#### Foreword
I have chosen the simpler way for implementing parse.php. I have not used classes, mainly because I am not used to working with them but, there were other reasons, like complexity. For implementation I have used a single switch. I know that a big switch like this isn't ideal, but to me, the code is very simple to understand and still readable (especially with one line functions).

#### Specification

Most of the work is done by `determine_val`. However, there are certain IPPcode22 functions that required special modifications . For e.g. LABEL takes just a string without the *@*, so `determine_val` is too "advanced" for it. I have also ignored type checking in said function, so to show a few **valid** examples:

```
LT GF@abc int@54 nil@nil
JUMPIFEQ TF@def bool@true string@abcdefg\104
ADD GF@XYZ GF@XYZ int@0xA5F
```

But still, these are **invalid**:
```
GT jump int@54 nil@nil
JUMPIFNEQ GF@abc bool@0 bool@false
SUB nil@nil int@0xA5F
```

These will result in the pre-specified error code 23.

#### Variables
**INT** numbers can be hexadecimal, octal, binary and with +/- (or just a plain number).
**BOOL** values, such as `bool@0` or `bool@1` are not valid. Only `bool@true` or `bool@false` are valid (and uppercase variants `bool@TRUE bool@FALSE`).
**STRING** is always being converted by inbuilt function `htmlspecialchars`, due to special characters part of which are: *<, >, & etc.*
**NIL** is a simple `nil@nil`.

---

## Functions
The code has many functions. They can be categorized by their usage:
* Cleaner code: `print_instruction`, `print_instruction_short`, `check_ops, var_only`
* Better readability of said code: `function_print`
* Supporting other functions: `get_val`
* Main functionality: `determine_val`, `remove_spaces`
* Error handling: `header_error`, `incorrect_function_error`, `other_error`

Each function is well described in the code. You may read the comments for further information to each function.