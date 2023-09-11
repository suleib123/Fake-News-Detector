# Fake-News-Detector
This program aims to distinuish between real and fake news sources, whether via a title, excerpt from the article, or the entire article. This program utilizes a naive bayes approach to calculate the probability that a the input string is from a real or fake news source. It is trained on the "Real.csv" and "Fake.csv" file included in the repository. In its current state the model seems to be fairly accurate, however, it can fall short at times and wrongly classify some inputs as real or fake.

# Current Issues
In its current state the model seems to be fairly accurate, however, it can fall short at times and wrongly classify some inputs as real or fake. Unfortuantely the world can be crazy and so can the news within it, so some articles covering the outlandish events of the world can be classified as fake. This also works in the opposite direction as some crazy claims made can be seen as real. Hopefully with further training these issues can be ironed out.

# Future Goals
In the future the plan is to expand the data that the model is trained upon, possibly including some method of web scraping to constantly update the model with new data. In order to further increase the accuracy of the model it may be necessary to switch from a naive bayes classifier to a more complex form of classification. If necessary, that can be done.
