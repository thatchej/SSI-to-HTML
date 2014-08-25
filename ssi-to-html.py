#This script will traverse through a directory heirarchy starting at the current directory
#and change all Server Side Includes in .html files to the actual HTML they represent
#
#Functions as an alternative to the server side include mechanism, but does it
#statically instead of dynamically
#
#Author: Jaron Thatcher
#Date: July 7, 2014

import os
import sys
import fileinput
import re
import time

intro = """\
 ______     ______     __        ______   ______        __  __     ______   __    __     __        
/\  ___\   /\  ___\   /\ \      /\__  _\ /\  __ \      /\ \_\ \   /\__  _\ /\ "-./  \   /\ \       
\ \___  \  \ \___  \  \ \ \     \/_/\ \/ \ \ \/\ \     \ \  __ \  \/_/\ \/ \ \ \-./\ \  \ \ \____  
 \/\_____\  \/\_____\  \ \_\       \ \_\  \ \_____\     \ \_\ \_\    \ \_\  \ \_\ \ \_\  \ \_____\ 
  \/_____/   \/_____/   \/_/        \/_/   \/_____/      \/_/\/_/     \/_/   \/_/  \/_/   \/_____/                     
"""
print intro
print "This script has a chance to irreversibly change the .html files in this directory and those below it."
user_input = raw_input("\nARE YOU SURE YOU WISH TO CONTINUE?(Y\N): ") 

if (user_input == 'y' or user_input == 'Y'):

	start_time = time.time()
	root = '.'
	errors = open('errors.txt', 'w')
	changed=0
	i=0
	error_count = 0
	print "Working ",
	sys.stdout.flush()

	for subdir, dirs, files in os.walk(root):
		for f in files:
			if '.html' in f:

				full_path_to_html = subdir + '/' + f
				tmp = open(full_path_to_html).read()
				SSIs = re.findall(r'(<!--#include)(\s*)(virtual=)"(.*?)"(-->)', tmp)
				
				for x in SSIs:
				
					current_ssi_path = x[3]
					ssi_call = ''.join(str(i) for i in x)
					ssi_call = ssi_call.replace(current_ssi_path, ('"'+current_ssi_path+'"')) #puts quotes where they should be
				
					try:
						if (current_ssi_path[0]) == '/':	
							#absolute path
							to_include = [line for line in open(os.path.expanduser('~/Scripts/includes/std-docs' + current_ssi_path))] #local
							changed += 1
						else:
							#relative path
							to_include = [line for line in open(subdir + '/' + current_ssi_path)]
							changed += 1

						ssi_code = ''.join(str(i) for i in to_include)
						tmp = tmp.replace(ssi_call, ssi_code)
						
					except:
						errors.write("FAILED TO REPLACE " + current_ssi_path + ' INTO ' + full_path_to_html + '\n\n')
						error_count += 1

				new_file = open(full_path_to_html, 'w')
				new_file.write(tmp)

			if (i%1500) == 0:
				#loading bar stuff
				print '\b=',
				sys.stdout.flush()
			i += 1

	print "> Done!"
	print "HTML Files changed: " + str(changed)
	print "Errors: " + str(error_count)
	print "Time Taken: " + str(int(time.time() - start_time)) + ' seconds'
