#This script will traverse through a directory heirarchy starting at the current directory
#and change all Server Side Includes in .html files to the actual HTML they represent
#
#Sort of functions as an alternative to the server side include mechanism, but does it
#statically instead of dynamically
#
#Author: Jaron Thatcer
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
						else:
							#relative path
							to_include = [line for line in open(subdir + '/' + current_ssi_path)]

						ssi_code = ''.join(str(i) for i in to_include)
						tmp = tmp.replace(ssi_call, '\n<!-- REPLACEMENT OF ' + current_ssi_path + ' -->\n' + ssi_code + '<!-- END REPLACEMENT OF ' + current_ssi_path + ' -->\n')
						changed += 1


					except:
						errors.write("FAILED TO REPLACE " + current_ssi_path + ' INTO ' + full_path_to_html + '\n\n')

				new_file = open(full_path_to_html, 'w')
				new_file.write(tmp)

			if (i%900) == 0:
				#loading bar stuff
				print '#',
				sys.stdout.flush()
			i += 1

	print " Done!"
	print "HTML Files changed: " + str(changed)
	print "Time Taken: " + str(time.time() - start_time)
