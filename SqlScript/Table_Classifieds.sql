/*
Create the main Classifieds Table
*/

CREATE TABLE IF NOT EXISTS Classifieds (
    id 			VARCHAR(32) NOT NULL PRIMARY KEY,
    customer_id		VARCHAR(32) NOT NULL,
    created_at		DATETIME NOT NULL,
    text 		TEXT NOT NULL,
    ad_type 		VARCHAR(32),
    price 		decimal(15,2),
    currency 		VARCHAR(32),
    payment_type 	VARCHAR(32),
    payment_cost 	decimal(15,2)
    );
