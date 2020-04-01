/*
Store Procedure to calculate margin over time
*/

USE `psdataengineer`;
DROP procedure IF EXISTS `margin_last_hour_insert`;

DELIMITER $$
USE `psdataengineer`$$
CREATE PROCEDURE `margin_last_hour_insert` ()
BEGIN
    INSERT INTO Margin
    SELECT	NOW() AS job_time,
            DATE(created_at) AS created_at_date, 
            HOUR(created_at) as created_at_hour, 
            ad_type, payment_type, 
            ((price - payment_cost) / price) AS Margin 
    FROM    Classifieds
    WHERE   ad_type != 'NULL'  AND
            ad_type != 'Free'  AND
            created_at 
            BETWEEN 
                DATE_SUB(DATE_FORMAT(NOW(),'%Y-%m-%d %H:00:00') ,INTERVAL 1 HOUR) AND 
                DATE_SUB(DATE_FORMAT(NOW(),'%Y-%m-%d %H:00:00') ,INTERVAL 0 HOUR)
    GROUP BY 
            day(created_at), 
            hour(created_at), 
            ad_type, 
            payment_type;
END$$

DELIMITER ;
