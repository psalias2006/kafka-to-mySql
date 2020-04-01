/* 
Create the Margin table
*/


CREATE TABLE IF NOT EXISTS Margin (
    job_time        	DATETIME NOT NULL,
    created_at_date 	DATE NOT NULL,
    created_at_hour 	INT NOT NULL,
    ad_type		VARCHAR(32) NOT NULL,
    payment_type 	VARCHAR(32) NOT NULL,
    Margin 		FLOAT);

