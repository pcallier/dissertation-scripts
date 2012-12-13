# make textgrids into a table
# then make table into a textgrid
# collisions will be noted and rejected? TODO

clearinfo

procedure TextGridsToTable
Create Table with column names... starter 0 tmin tier text tmax
original = selected ("Table")
select all
num_of_tgs = numberOfSelected ("TextGrid")
while num_of_tgs > 0
	tg1 = selected ("TextGrid", 1)
	select tg1
	Down to Table... no 6 yes yes
	table1 = selected ("Table", 1)
	plus original
	Append
	appended = selected ("Table")
	select table1
	plus original
	Remove
	original = appended
	select original
	Sort rows... tmin
	Rename... result
	select tg1
	Remove
	select all
	num_of_tgs = numberOfSelected ("TextGrid")
endwhile
select original
endproc

procedure whichTierIs  tier_name_to_find$
	.its_on = -1
	number_of_tiers = Get number of tiers
	for i from 1 to number_of_tiers
		tier_name$ = Get tier name... 'i'
		if tier_name$ = tier_name_to_find$
			.its_on = i
		endif
	endfor
endproc

procedure TableToTextGrid
	tg_start = Get minimum... tmin
	tg_end = Get maximum... tmax
	closeness_epsilon = 0.001
	table_to_convert = selected ("Table")
	first_tier$ = Get value... 1 tier
	Create TextGrid... 'tg_start' 'tg_end' 'first_tier$'
	#Insert boundary... 1 'tg_start'
	Rename... result
	the_textgrid = selected ("TextGrid")
	
	select table_to_convert
	last_tmax1 = tg_start
	nrows = Get number of rows
	for row_i from 1 to nrows
		# Get row information
		tmin = Get value... 'row_i' tmin
		tmax = Get value... 'row_i' tmax
		tier$ = Get value... 'row_i' tier
		text$ = Get value... 'row_i' text
		
		# get tier number
		select the_textgrid
		call whichTierIs 'tier$'
		cur_tier = whichTierIs.its_on
		if whichTierIs.its_on = -1
			# create a new tier
			printline Creating new tier: 'tier$'
			ntiers = Get number of tiers
			tier_pos = ntiers + 1
			Insert interval tier... 'tier_pos' 'tier$'
			cur_tier = tier_pos
			# if the tier doesn't have an interval at the very start, then add a starting boundary
			if tmin <> tg_start
				Insert boundary... 'cur_tier' 'tmin'
			endif
			last_tmax'cur_tier' = tmin	
		endif


		
		# add the interval, checking for collisions
		last_tmax = last_tmax'cur_tier'
		if abs(tmin - last_tmax) < closeness_epsilon
			if  text$ <> "?"
				cur_interval = Get number of intervals... 'cur_tier'
				Set interval text... 'cur_tier' 'cur_interval' 'text$'
				if abs(tmax-tg_end) > closeness_epsilon
					Insert boundary... 'cur_tier' 'tmax'	
				endif		
			endif
		else
			# collision or gap
			
			# gap
			if tmin > last_tmax
				# put down a new left and right boundary
				Insert boundary... 'cur_tier' 'tmin'					
				cur_interval = Get number of intervals... 'cur_tier'
				Set interval text... 'cur_tier' 'cur_interval' 'text$'
				if abs(tmax-tg_end) > closeness_epsilon
					Insert boundary... 'cur_tier' 'tmax'
				endif
			else 
				printline Collision: 'tmin' 'tmax', 'tier$': 'text$'
				printline Last tmax: 'last_tmax', Current tier: 'cur_tier'
			endif
		endif
		# make sure the cursor moves, else nothing will make it on	
		last_tmax'cur_tier' = tmax
		select table_to_convert
	endfor
	select the_textgrid
endproc

call TextGridsToTable
call TableToTextGrid
Save as chronological text file... alignments_all.TextGrid
printline Done.