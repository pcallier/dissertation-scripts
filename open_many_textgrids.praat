# This script will open all TextGrids in a specified directory.
# You can filter the files, and just open the files starting with "File_filter" (cf. below)
#
# A modified version of 
# "open_all_files_in_folder.praat" by Mietta Lennes 24.1.2002
#
# 07.05.2002 John Tøndering
# modified 15.05.2003 John Tøndering - Praat ver. 4.0.52 (Win)
# johtnd@cphling.dk


directory_manual$ = ""
file_filter$ =  ""

directory$ = "/home/patrick/dissertation/scripts/textgrids/"
# If directory is chosen manually, select this directory
if length(directory_manual$) > 0
    directory$ = directory_manual$
endif

#Create Strings as file list... fileList /home/patrick/dissertation/scripts/textgrids/
Create Strings as file list... list 'directory$'*
numberOfFiles = Get number of strings
for ifile to numberOfFiles
    filename$ = Get string... ifile
    printline 'filename$'
   # Checking the left side of the file name
    filter$ = file_filter$
    filterlaengde = length(file_filter$)
    if left$ (filename$, 'filterlaengde') = filter$

        # The next line gives the rule for the filename: if its 9 rightmost
        # characters are ".TextGrid", then go on and read the file.
        if right$ (filename$, 9) = ".textgrid"
            Read from file... 'directory$''filename$'
        endif
    endif
select Strings list
endfor

select Strings list
Remove



#The filter could be just a simple if-then-construction: if a filename 
#fulfils a criterion, then read the file, otherwise move on to the next 
#filename. Here's an example that will only select filenames ending with 
#exactly the string ".TextGrid". Just add the if...-line to the script 
#(because the corresponding endif-line was in the previous script by 
#mistake). You can make different versions of the script to open 
#different file types. See the Praat manual on how to use more complex 
#criteria for string variables.

...
#for ifile to numberOfFiles
#filename$ = Get string... ifile
# The next line gives the rule for the filename: if its 9 rightmost
# characters are ".TextGrid", then go on and read the file.
#if right$ (filename$, 9) = ".TextGrid"
#Read from file... 'directory$''filename$'
# by the way, if you have no filename filter (starting with if),
# the next endif line is not necessary at all... sorry!
#endif
#select Strings list
#endfor
#...

