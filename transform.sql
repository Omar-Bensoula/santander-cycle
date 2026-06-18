CREATE TABLE journeys AS 
SELECT 
	number_id,
	TO_TIMESTAMP(start_date, 'YYYY-MM-DD HH24:MI') AS start_date,
	start_station_number,
	start_station,
	TO_TIMESTAMP(end_date, 'YYYY-MM-DD HH24:MI') AS end_date,
	end_station_number::BIGINT,
	end_station,
	bike_number::INT,
	CASE 
	    WHEN bike_model = 'CLASSIC' THEN 'standard'
	    WHEN bike_model = 'PBSC_EBIKE' THEN 'e-bike'
	    ELSE 'other'
	END AS bike_model,
	total_duration::INTERVAL,
	total_duration_ms::BIGINT
FROM journeys_raw;

DROP TABLE journeys_raw;