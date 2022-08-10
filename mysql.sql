CREATE DATABASE IF NOT EXISTS `sauravlogin` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `sauravlogin`;

CREATE TABLE IF NOT EXISTS `Account`(
	`id` int(65) NOT NULL auto_increment,
    `name` varchar(50) NOT NULL,
    `username` varchar(50) NOT NULL,
    `password` varchar(255) NOT NULL,
    `email` varchar(100) NOT NULL,
    `nickname` varchar(50) NOT NULL,
    `hobby` varchar(500) NOT NULL,
    
    PRIMARY KEY (`id`) 
    )ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
 
 
 
 ALTER TABLE comments
 ADD cid int(65); 
 
 ALTER TABLE comments
 DROP PRIMARY KEY,
 ADD PRIMARY KEY (cid);
 use sauravlogin;
 drop table comments;
 
 CREATE TABLE IF NOT EXISTS `comments` (
	`cid` int(65) NOT NULL auto_increment,
	`Name` varchar(50) NOT NULL,
    `message` varchar(6000) NOT NULL,
    PRIMARY KEY (`cid`) 
 )ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
 
 use sauravlogin;
 
 ALTER TABLE Account
 add confirm  varchar(255) not null;
 show tables;
 describe Account;
 select* from Account;
 ALTER TABLE Account
  DROP COLUMN confirm;
use sauravlogin;
show tables;
truncate table comments;
describe comments;
select * from comments;

 

    