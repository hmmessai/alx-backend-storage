-- creates a stored procedure ComputeAverageScoreForUser 
-- that computes and store the average score for a student
DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;
DELIMITER $$
CREATE PROCEDURE ComputeAverageScoreForUser(user_id INT)
BEGIN
	DECLARE average FLOAT DEFAULT 0;
	
	SELECT AVG(score)
	  INTO average
	  FROM corrections
	  WHERE `corrections`.`user_id` = user_id;

	UPDATE users
	  SET average_score = average
	  WHERE id = user_id;

END $$
DELIMITER ;
