create
database panda;
use
panda;
CREATE TABLE IF NOT EXISTS `video`
(
    `id`
    INT
    UNSIGNED
    AUTO_INCREMENT,
    `video_title`
    VARCHAR
(
    100
) NOT NULL,
    `video_cover` VARCHAR
(
    200
) NOT NULL,
    `video_url` VARCHAR
(
    200
) NOT NULL,
    `video_author` VARCHAR
(
    40
) NOT NULL,
    `video_description` VARCHAR
(
    400
) NOT NULL,
    `submission_date` DATETIME_INTERVAL_CODE ,
    PRIMARY KEY
(
    `video_id`
)
    );
CREATE TABLE IF NOT EXISTS `course_sentence`
(
    `id`
    INT
    UNSIGNED
    AUTO_INCREMENT,
    `sentence_content`
    VARCHAR
(
    100
) NOT NULL,
    `sentence_English` VARCHAR
(
    200
) NOT NULL,
    `sentence_pronunciation` VARCHAR
(
    200
) NOT NULL,
    primary key
(
    `id`
)
    );
