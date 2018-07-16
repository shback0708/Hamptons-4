For the business analytics file, we have used data about viewership per date and viewership per team to create our predictions.

Using Date

On the Date VPG sheet, we have organized it such that the numbers displayed are the average numbers of viewers per game per day. We have
then created graphs, one for each season, which creates a cubic trendline as well as a variance value.

Using Team

On the Team VPG sheet, we have organized it such that the numbers displayed are the average numbers of viewers per game per team. We have
then created graphs, one for each season, which creates a cubic trendline as well a variance value.

Combining Data

We will collect 3 data points and 3 variance values to predict the viewership for the game. From the two teams that are playing against
each other, we will use the appropriate team trendline from the Team VPG sheet to get an average viewership value from each team. From the
date of the game, we will use the appropriate date trendline from the Date VPG sheet to get an average viewership value for that specific
date. The average viewership values of the teams and the average viewership value of the date will make up the 3 data points, and the 2
variance values of the teams along with the variance value of the date will make up the variance 3 variance values. Then, to get the
final predicted viewership value, we will multiple each data point by the fraction of the inverse of its corresponding variance value over
the sum of all inversed variance values.
