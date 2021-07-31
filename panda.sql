create database panda;
use panda;
CREATE TABLE IF NOT EXISTS `video`(
   `id` INT UNSIGNED AUTO_INCREMENT,
   `video_title` VARCHAR(100) NOT NULL,
   `video_cover` VARCHAR(200) NOT NULL,
   `video_url` VARCHAR(200) NOT NULL,
   `video_author` VARCHAR(40) NOT NULL,
   `video_description` VARCHAR(400) NOT NULL,
   `submission_date` DATETIME_INTERVAL_CODE ,
   PRIMARY KEY ( `video_id` )
);
