Basketball Analytics

Looking at the data that was given to us, we felt that using Python would be the most efficient way to sort it. Thus, we first imported the data as csv/text
files, and worked from there. As the question described, we also needed to sort the play-by play data. This seemed easier for us to do on Microsoft Excel
using its various table sorting functions, so we did that there and imported it as a csv file. Then, we decided that it would be easiest for us to turn the 
strings that the data comes in into lists, sets, and dictionaries; that way, it would be easier for us to access. 
Upon working with the data in this form, we encountered some inefficiencies, and realized that running through the game and keeping track of a players' stats
would be simpler as objects. Thus, we wrote and added those new classes. From there, we just wrote functions to run through the play-by-play of each game 
and update statistics accordingly. Lastly, as required, we re-exported our data back as a csv file.