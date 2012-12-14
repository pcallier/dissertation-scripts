voice.data <- read.delim("data/voice_analysis/LS100197_mono_prelim.tsv")
#recodes
voice.data <- within(voice.data, {
	Tone <- factor(gsub("([^0-9])", "", levels(Syllable)[Syllable]))
	Syllable <- factor(gsub("[0-9]","",levels(Syllable)[Syllable]))
	Segment <- factor(gsub("[0-9]","",levels(Segment)[Segment]))
	Segment[Syllable == "YAN"] <- "EH"
	Segment[Syllable == "YE"] <- "EH"

	levels(Segment) <- c(levels(Segment), c("II","YU","IR","YW"))
	Segment[grepl("VE|VA",Syllable) & Segment=="IY"] <- "YW"
	Segment[grepl("([JQXY]V$)",Syllable) & Segment=="IY"] <- "YU"
	Segment[grepl("[ZCS]HI",Syllable) & Segment=="IY"] <- "IR"
	Segment[grepl("[ZCS]I",Syllable) & Segment=="IY"] <- "II"
	Segment[grepl(".I[AEIOU]",Syllable) & Segment=="IY"] <- "Y"

	Coda <- gsub(".+(NG?$)", "\\1", levels(Syllable)[Syllable])
	Coda[!Coda %in% c("N","NG")] <- ""
	Coda <- factor(Coda)
})

with(subset(voice.data, Segment=="V"),plot(F1_2 ~ F2_2, xlim=c(3000,900),ylim=c(1200, 200)))
with(droplevels(subset(voice.data, Segment %in% c("AA"))), table(Segment, Syllable))
with(voice.data, plot(F1_2 ~ F2_2, xlim=c(3000,700),ylim=c(1300, 200), pch =NA))
with(subset(voice.data,Coda =="" & Segment %in% c("IY","YU","UW","OW","AA","AO","EH","EY")), text(F1_2 ~ F2_2, labels = Segment))

# spectral tilt
with(subset(voice.data, !(Syllable %in% c("sp","{SL}","{LG}"))), {
	par(ask=TRUE)
	plot(H1.H2_1 ~ Tone)
	plot(H1.A1_1 ~ Tone)
	plot(H1.A3_1 ~ Tone)

	plot(H1.H2_1 ~ Coda)
	plot(H1.A1_1 ~ Coda)
	plot(H1.A3_1 ~ Coda)

	plot(H1.H2_2 ~ Tone)
	plot(H1.A1_2 ~ Tone)
	plot(H1.A3_2 ~ Tone)

	plot(H1.H2_2 ~ Coda)
	plot(H1.A1_2 ~ Coda)
	plot(H1.A3_2 ~ Coda)

	plot(H1.H2_3 ~ Tone)
	plot(H1.A1_3 ~ Tone)
	plot(H1.A3_3 ~ Tone)

	plot(H1.H2_3 ~ Coda)
	plot(H1.A1_3 ~ Coda)
	plot(H1.A3_3 ~ Coda)	
	par(ask=FALSE)
})