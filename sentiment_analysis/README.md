Sentiment Analysis
==================

The code (sentiment_analysis.py) is implemented according
to the bernouli document model explanined at [1]

The dataset used here was downloaded from [2] and normalized
using data_normalization.py.

The normalization algorithm removes punctuations, urls, mentions
and hashs. It also removes the 'source' column from the dataset
to reduce the amout of data that is loaded to memory.

After the normalization a sample containing 10 thousand lines
was extracted to be used with the algorithm.

__Links__:

[1] - http://www.inf.ed.ac.uk/teaching/courses/inf2b/learnnotes/inf2b-learn-note07-2up.pdf

[2] - http://thinknook.com/twitter-sentiment-analysis-training-corpus-dataset-2012-09-22/
