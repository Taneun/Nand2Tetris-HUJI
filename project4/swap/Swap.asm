// This file is part of nand2tetris, as taught in The Hebrew University, and
// was written by Aviv Yaish. It is an extension to the specifications given
// [here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
// as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
// Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).

// The program should swap between the max. and min. elements of an array.
// Assumptions:
// - The array's start address is stored in R14, and R15 contains its length
// - Each array value x is between -16384 < x < 16384
// - The address in R14 is at least >= 2048
// - R14 + R15 <= 16383
//
// Requirements:
// - Changing R14, R15 is not allowed.

// Put your code here.

//set indexes
@maxIndex
M=0
@minIndex
M=0
@currIndex
M=0
@i
M=0

@R14
D=M
@ARR
A=D
@R15
D=M
@length
M=D

//set max and min to first num
@ARR
D=M
@min
M=D
@max
M=D

//loop to find max and min
(LOOP)
@i
D=M
@currIndex
M=D
@ARR
A=D+A
D=M
//check if bigger
@curr
M=D
@max
D=D-M
@BIGGER
D;JGT
//check if smaller
@curr
D=M
@min
D=D-M
@SMALLER
D;JLT
//increase i and check if done
(INC)
@i
M=M+1
D=M
@length
D=D-M
@SWAP
D;JGE
@LOOP
D;JLT


(BIGGER)
@currIndex
D=M
@maxIndex
M=D
@curr
D=M
@max
M=D
@INC
0;JMP

(SMALLER)
@currIndex
D=M
@minIndex
M=D
@curr
D=M
@min
M=D
@INC
0;JMP

(SWAP)
//swap max and min
// Load the base address of the array
@R14
D=M

// Calculate address of maxIndex element
@maxIndex
D=D+M            // D = base + maxIndex
@tempAddress
M=D              // Store max element address in tempAddress

// Load max value into temp register
A=D              // Go to array[maxIndex] address
D=M              // D = array[maxIndex] value
@tempValue
M=D              // Store max value in tempValue

// Calculate address of minIndex element
@R14
D=M
@minIndex
D=D+M            // D = base + minIndex
@tempAddressMin
M=D              // Store min element address in tempAddressMin

// Load min value into array[maxIndex]
A=D              // Go to array[minIndex] address
D=M              // D = array[minIndex] value
@tempAddress
A=M
M=D              // Store min value in array[maxIndex]

// Load max value from tempValue into array[minIndex]
@tempValue
D=M              // D = max value
@tempAddressMin
A=M
M=D              // Store max value in array[minIndex]


(END)
@END
0;JMP
