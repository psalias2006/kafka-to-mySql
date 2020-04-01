/*
Create an event that call Margin procedure every hour
*/


CREATE EVENT calculate_margin_last_hour_insert
    ON SCHEDULE EVERY 1 HOUR 
    DO
      CALL `psdataengineer`.`margin_last_hour_insert`();
