USE SNS_Mining;

CREATE TABle politician(
	Name varchar(50) not null, 
	Screen_Name varchar(50) not null,
	Twitter_ID varchar(50) not null, 
	Inclination int, 

	PRIMARY KEY(Twitter_ID)
);

INSERT IGNORE INTO politician VALUES('남경필','yesKP','101674890','1');
INSERT IGNORE INTO politician VALUES('이재명','Jaemyung_Lee','106379129','2');
INSERT IGNORE INTO politician VALUES('원희룡','wonheeryong','109419315','1');
INSERT IGNORE INTO politician VALUES('정진석','js0904','123472468','1');
INSERT IGNORE INTO politician VALUES('김부겸','hopekbk','131983524','2');
INSERT IGNORE INTO politician VALUES('김성식','okkimss','155236262','2');
INSERT IGNORE INTO politician VALUES('원유철','won6767','159344594','1');
INSERT IGNORE INTO politician VALUES('박지원','jwp615','169290610','2');
INSERT IGNORE INTO politician VALUES('최경환','khwanchoi','181853552','1');
INSERT IGNORE INTO politician VALUES('박범계','bkfire1004','201168492','2');
INSERT IGNORE INTO politician VALUES('이준석','junseokandylee','218127029','1');
INSERT IGNORE INTO politician VALUES('박영선','Park_Youngsun','227597872','2');
INSERT IGNORE INTO politician VALUES('민병두','bdmin1958','259511532','2');
INSERT IGNORE INTO politician VALUES('서청원','scw0403','260704303','1');
INSERT IGNORE INTO politician VALUES('문재인','moonriver365','444465942','2');
INSERT IGNORE INTO politician VALUES('안희정','steelroot','47513674','2');
INSERT IGNORE INTO politician VALUES('정동영','coreacdy','47830455','2');
INSERT IGNORE INTO politician VALUES('천정배','jb_1000','47867311','2');
INSERT IGNORE INTO politician VALUES('심재철','cleanshim','49004147','1');
INSERT IGNORE INTO politician VALUES('김무성','kimmoosung','50879035','1');
INSERT IGNORE INTO politician VALUES('송영길','Bulloger','53031381','2');
INSERT IGNORE INTO politician VALUES('정우택','bigwtc','533756735','1');
INSERT IGNORE INTO politician VALUES('나경원','Nakw','58969192','1');
INSERT IGNORE INTO politician VALUES('추미애','choomiae','59686991','2');
INSERT IGNORE INTO politician VALUES('정세균','sk0926','68606927','2');
INSERT IGNORE INTO politician VALUES('진영','Chinyoung0413','715475108937076736','2');
INSERT IGNORE INTO politician VALUES('표창원','DrPyo','74048201','2');
INSERT IGNORE INTO politician VALUES('김진표','jinpyo_kim','74642156','2');
INSERT IGNORE INTO politician VALUES('박원순','wonsoonpark','76295962','2');
INSERT IGNORE INTO politician VALUES('안철수','cheolsoo0919','881373588','2');
INSERT IGNORE INTO politician VALUES('장제원','Changjewon','58356106','1');
INSERT IGNORE INTO politician VALUES('김진태','jtkim1013','181005654','1');
