// This file is part of nand2tetris, as taught in The Hebrew University, and
// was written by Aviv Yaish. It is an extension to the specifications given
// [here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
// as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
// Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).

// This program illustrates low-level handling of the screen and keyboard
// devices, as follows.
//
// The program runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.
// 
// Assumptions:
// Your program may blacken and clear the screen's pixels in any spatial/visual
// Order, as long as pressing a key continuously for long enough results in a
// fully blackened screen, and not pressing any key for long enough results in a
// fully cleared screen.
//
// Test Scripts:
// For completeness of testing, test the Fill program both interactively and
// automatically.
// 
// The supplied FillAutomatic.tst script, along with the supplied compare file
// FillAutomatic.cmp, are designed to test the Fill program automatically, as 
// described by the test script documentation.
//
// The supplied Fill.tst script, which comes with no compare file, is designed
// to do two things:
// - Load the Fill.hack program
// - Remind you to select 'no animation', and then test the program
//   interactively by pressing and releasing some keyboard keys

// Put your code here.

//pixel = 0, state = 0
@pixel
M=0
@state
M=0

//endless loop
(LOOP)
//keyboard input
@KBD
D=M
//check if its needed to reset pixel, if the state change
@state
D=D-M
@DECIDE
//if the state is the same
D;JEQ
//else, reset pixel and change state
@CHANGE
D;JNE

(CHANGE)
@pixel
M=0
@KBD
D=M
@state
M=D
@DECIDE
0;JMP

(DECIDE)
@pixel
D=M
@SCREEN
D=D+A
@24576
D=D-A
@LOOP
D;JGE
//check if pixel legit
@24576
D=A
@BLACK
D=M-D
@LOOP
D;JGE
@KBD
D=M
//decide the action
@WHITE
D;JNE
@BLACK
D;JEQ

(WHITE)
@pixel
D=M
@SCREEN
A=D+A
M=-1
@pixel
M=M+1
//return to loop
@LOOP
0;JMP

(BLACK)
@pixel
D=M
@SCREEN
A=D+A
M=0
@pixel
M=M+1
//return to loop
@LOOP
0;JMP









