# Extracts mean formant values, H1, H2, and spectral tilt measures
# dynamically across an duration defined by the textgrid. 
# The number of interval values extracted is equal to numintervals below.
# Writes results to a textfile.
# Christian DiCanio, 2007

numintervals = 12
#Number of intervals you wish to extract pitch from.

form Extract Formant data from labelled points
   sentence Directory_name: C:\Users\Patrick\Documents\audio\2012interviews\working\
   sentence Objects_name: LS100197_mono_350
   sentence Interval_label AA1
   sentence Log_file AA
   positive Labeled_tier_number 1
   positive Analysis_points_time_step 0.005
   positive Record_with_precision 1
   comment Formant Settings:
   positive Analysis_time_step 0.005
   positive Maximum_formant 5500
   positive Number_formants 3
   positive F1_ref 500
   positive F2_ref 1485
   positive F3_ref 2475
   positive F4_ref 3550
   positive F5_ref 4650
   positive Window_length 0.005
   comment Pitch Settings:
   positive Pitch_floor 75
   positive Pitch_ceiling 600
endform

maxf =maximum_formant

# If your sound files are in a different format, you can insert that format instead of wav below.
# Resampling done for LPC analysis.
Read from file... 'directory_name$''objects_name$'.wav
soundID_bf = selected("Sound")
select 'soundID_bf'
Resample... 16000 50
soundID = selected("Sound")
select 'soundID'
Read from file... 'directory_name$''objects_name$'.TextGrid
textGridID = selected("TextGrid")
num_labels = Get number of intervals... labeled_tier_number

fileappend 'directory_name$''log_file$'.txt label'tab$'
for i to numintervals
	fileappend 'directory_name$''log_file$'.txt 'i'F1'tab$''i'F2'tab$''i'F3'tab$'
	fileappend 'directory_name$''log_file$'.txt 'i'H1hz'tab$''i'H2hz'tab$'
	fileappend 'directory_name$''log_file$'.txt 'i'H1-H2'tab$''i'H1-A1'tab$''i'H1-A2'tab$''i'H1-A3'tab$'
endfor
fileappend 'directory_name$''log_file$'.txt 'newline$'


for i to num_labels
	select 'textGridID'
	label$ = Get label of interval... labeled_tier_number i
		if label$ = interval_label$
			fileappend 'directory_name$''log_file$'.txt 'objects_name$''tab$'
      			intvl_start = Get starting point... labeled_tier_number i
			intvl_end = Get end point... labeled_tier_number i
			select 'soundID'
			Extract part... intvl_start intvl_end Rectangular 1 no
			intID = selected("Sound")	
			To Pitch (ac)...  'analysis_points_time_step' 'pitch_floor' 15 no  0.03 0.45 0.01 0.35 0.14 'pitch_ceiling'
			invl_pitch = selected("Pitch")
			chunkID  = (intvl_end-intvl_start)/numintervals

			for j to numintervals

				#Getting formants and frequency boundaries 10% away from them. Writing to data file.

				select 'intID'
				Extract part... (j-1)*chunkID j*chunkID Rectangular 1 no
				chunk_part = selected("Sound")
				form_chunk = To Formant (burg)... 0 5 'maxf' 'window_length' 50
				formantID_bf = selected("Formant")
				Track... 'number_formants' 'f1_ref' 'f2_ref' 'f3_ref' 'f4_ref' 'f5_ref' 1 1 1
				formantID = selected("Formant")
				f1 = Get mean... 1 0 0 Hertz
				f1_a = f1-(f1/10)
				f1_b = f1+(f1/10)
				f2 = Get mean... 2 0 0 Hertz
				f2_a = f2-(f2/10)
				f2_b = f2+(f2/10)
				f3 = Get mean... 3 0 0 Hertz
				f3_a = f3-(f3/10)
				f3_b = f3+(f3/10)
					if j = numintervals
					fileappend 'directory_name$''log_file$'.txt
 	           			... 'f1''tab$''f2''tab$''f3'
					else
					fileappend 'directory_name$''log_file$'.txt
   	         			... 'f1''tab$''f2''tab$''f3'
					endif
				select 'intID'
				select 'formantID_bf'
				select 'formantID'
				Remove

				#Getting H1 and H2 values by extracting pitch values. Then getting the frequency
				#boundaries 10% away from them. Writes H1 and H2 measures to data file.

				select 'invl_pitch'
				h1hz = Get mean... (j-1)*chunkID j*chunkID Hertz
				h1hz_a = h1hz-(h1hz/10)
				h1hz_b = h1hz+(h1hz/10)
				h2hz = h1hz*2
				h2hz_a = h2hz-(h2hz/10)
				h2hz_b = h2hz+(h2hz/10)
					if j = numintervals
					fileappend 'directory_name$''log_file$'.txt
 	           			... 'tab$''h1hz''tab$''h2hz'
					else
					fileappend 'directory_name$''log_file$'.txt
   	         			... 'tab$''h1hz''tab$''h2hz'
					endif

				#Converting each chunk in interval to a long term average spectrum. Then queries
				#the maximum amplitude within a frequency region specified by the frequency
				#boundaries around H1, H2, F1, F2, and F3. The difference between these maxima
				#is a measure of spectral tilt which is then written to the data file.

				select 'chunk_part'
				To Ltas... 100
				ltasID = selected("Ltas")
				h1db = Get maximum... h1hz_a h1hz_b None
				h2db = Get maximum... h2hz_a h2hz_b None
				a1db = Get maximum... f1_a f1_b None
				a2db = Get maximum... f2_a f2_b None
				a3db = Get maximum... f3_a f3_b None
				h1_h2 = h1db - h2db
				h1_a1 = h1db - a1db
				h1_a2 = h1db - a2db
				h1_a3 = h1db - a3db
					if j = numintervals
					fileappend 'directory_name$''log_file$'.txt
 	           			... 'tab$''h1_h2''tab$''h1_a1''tab$''h1_a2''tab$''h1_a3''newline$'
					else
					fileappend 'directory_name$''log_file$'.txt
   	         			... 'tab$''h1_h2''tab$''h1_a1''tab$''h1_a2''tab$''h1_a3''tab$'
					endif
				select 'ltasID'
				Remove
			endfor
		select 'intID'
		select 'invl_pitch'
		Remove
		else
			#do nothing
   		endif
endfor
