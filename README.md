# Cloud Computing Assignments 

## Assignment - I:

Prequisitives:
gcc-multilib

To compile to get the 32 bit Assembly Language Code:
> gcc -m32 -S [-o path_to_output_file ] [-i path_to_input_file] path_to_program_file

To compile to get the 64 bit Assembly Language Code:
> gcc -m64 -S [-o path_to_output_file ] [-i path_to_input_file] path_to_program_file

Default Input C Program File: **./prog.c**

To run the Translator:
python translator.py [-i path_to_input_file] [-o path_to_output_file] 

Default Input 32 Bit Assembly File: **./32_bit.asm**

Default Output 32 Bit Assembly File: **./64_bit.asm**