USE SNS_Mining

CREATE TABLE twitter_reply(
	Twitter_ID varchar(50) not null,
	Screen_Name varchar(50) not null,
	Date datetime not null,
	URL varchar(50) not null,
	Contents varchar(500) not null,
	Favorite int,
	Retweet int,
	Origin_ID varchar(50) not null,
	Origin_Screen_Name varchar(50) not null,
	Origin_URL varchar(50) not null,
	
	PRIMARY KEY(URL)
)
