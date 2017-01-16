USE SNS_Mining;

CREATE TABLE twitter_tweet(
	Twitter_ID varchar(50) not null,
	Screen_Name varchar(50) not null,
	Inclination int,
	Date datetime not null,
	URL varchar(50) not null,
	Contents varchar(500) not null,
	Favorite int,
	Retweet int,

	PRIMARY KEY(URL)
)
