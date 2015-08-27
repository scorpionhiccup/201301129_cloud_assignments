import sys, getopt

def convert(input_lines):
	to_replace={
		'ebp': 'rbp',
		'ebx':'rdi', 'esp': 'rsp', 
		'pushl':'pushq', 'movq':'movl', 
		'ecx':'rsi'}
	
	output_lines=[]
	lines_to_exclude=['cfi_restore', 'leave']
	
	for index in range(len(input_lines)):
		if 'cfi_def_cfa_offset'  in input_lines[index]:
			output_lines.append(input_lines[index].replace('8', '16'))
			#http://stackoverflow.com/questions/7534420/gas-explanation-of-cfi-def-cfa-offset
			#8 byte for return address onto the stack
			#another 8 bytes for stack of main itself:
			continue
		elif 'cfi_offset' in input_lines[index]:
			output_lines.append(input_lines[index].replace('8', '16').replace('5', '6'))
			continue
		elif 'cfi_def_cfa_register' in input_lines[index]:
			output_lines.append(input_lines[index].replace('5', '6'))	
			continue
		elif 'cfi_def_cfa' in input_lines[index]:
			output_lines.append(input_lines[index].replace('4, 4', '7, 8'))	
			continue	
		elif any(ext in input_lines[index] for ext in lines_to_exclude):
			if 'leave' in input_lines[index]:
				output_lines.append("	popq	%rbp")
			continue
		elif 'subl'	in input_lines[index] and '%esp' in input_lines[index]:
			continue
		elif "movl	%esp, %ebp" in input_lines[index]:
			input_lines[index].replace("movl	%esp, %ebp", "movq	%rsp, %rbp")
			output_lines.append(reduce(lambda a, kv: a.replace(*kv), 
				to_replace.iteritems(), input_lines[index])
			)
			output_lines[-1] = output_lines[-1].replace("movl", "movq")
			continue

		output_lines.append(reduce(lambda a, kv: a.replace(*kv), 
			to_replace.iteritems(), input_lines[index])
		)

	return output_lines

def translate(argv):
	optlist, args = getopt.getopt(argv, 'i:o:')

	input_file = "32_bit.asm"
	output_file = "64_bit.asm"
	
	for o, a in optlist:
		if o == "-i":
			input_file=a
		elif o=="-o":
			output_file=a

	with open(input_file, 'r') as data_file:
		input_lines = data_file.read().splitlines()
	
	data_file.close()
	output_lines=convert(input_lines)

	with open(output_file, 'w') as output64_file:
		for line in output_lines:
			output64_file.write(line + '\n')

	output64_file.close()

if __name__ == '__main__':
	translate(sys.argv)
