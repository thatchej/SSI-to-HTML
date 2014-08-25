SSI-to-HTML
===========

This script will traverse through a directory heirarchy starting at the current directory
and change all Server Side Includes in .html files to the actual HTML they represent

Sort of functions as an alternative to the server side include mechanism, but does it
statically instead of dynamically

Note: 99.999% of the time, you will have to change the directories in the open() calls. I could let you do this via the command line, but I don't know if anybody is ever going to use this. 
