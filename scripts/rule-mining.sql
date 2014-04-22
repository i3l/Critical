USE icu;

DELIMITER //
DROP PROCEDURE IF EXISTS setup_mining;
CREATE PROCEDURE setup_mining ()
BEGIN
        DECLARE rPercent INT;
        DECLARE rVar TEXT;
        DECLARE endOfResults INT;
        DECLARE cur CURSOR FOR SELECT DISTINCT var FROM vstats;
        DECLARE CONTINUE HANDLER FOR NOT FOUND SET endOfResults = 1;

        OPEN cur;
        SET endOfResults = 0;
        WHILE endOfResults = 0 DO
                FETCH cur INTO rVar;
                        
                SET @s = CONCAT('DROP TABLE IF EXISTS ', rVar);
                PREPARE stmt FROM @s;
                EXECUTE stmt;
                DEALLOCATE PREPARE stmt;

                SET @s = CONCAT('CREATE TABLE ', rVar, ' ',
                        'AS ( ',
                        'SELECT DISTINCT id, death, dvalue ',
                        'FROM vstats AS v ',
                        'INNER JOIN outcome AS o ',
                        'USING (id) ',
                        'WHERE ',
                        'var = "', rVar, '" ',
                        ')');
                PREPARE stmt FROM @s;
                EXECUTE stmt;
                DEALLOCATE PREPARE stmt;

                SET @s = CONCAT('CREATE INDEX id_ind ',
                        'ON ', rVar, ' ',
                        '(id)');
                PREPARE stmt FROM @s;
                EXECUTE stmt;
                DEALLOCATE PREPARE stmt;

                SET @s = CONCAT('CREATE INDEX dval_ind ',
                        'ON ', rVar, ' ',
                        '(dvalue)');
                PREPARE stmt FROM @s;
                EXECUTE stmt;
                DEALLOCATE PREPARE stmt;

                SET @s = CONCAT('CREATE INDEX death_ind ',
                        'ON ', rVar, ' ',
                        '(death)');
                PREPARE stmt FROM @s;
                EXECUTE stmt;
                DEALLOCATE PREPARE stmt;
        END WHILE;
        CLOSE cur;
END//
DELIMITER ;

DELIMITER //
DROP PROCEDURE IF EXISTS mine_rules;
CREATE PROCEDURE mine_rules ()
BEGIN
        DECLARE endOfResults INT;
        DECLARE dval INT;
        DECLARE dead INT;
        DECLARE var1 TEXT;
        DECLARE var2 TEXT;

        DECLARE cur_rule CURSOR FOR
                SELECT v1.var AS prec, v2.var AS ante FROM (
                        SELECT DISTINCT var FROM vstats
                ) AS v1
                CROSS JOIN
                (
                        SELECT DISTINCT var FROM vstats
                ) AS v2
                WHERE v1.var <> v2.var;
        DECLARE CONTINUE HANDLER FOR NOT FOUND SET endOfResults = 1;

        OPEN cur_rule;
        SET endOfResults = 0;

        SELECT COUNT(id) * 0.01 INTO @d0_total
        FROM vstats INNER JOIN outcome USING (id) 
        WHERE death = 0;

        SELECT COUNT(id) * 0.01 INTO @d1_total
        FROM vstats INNER JOIN outcome USING (id) 
        WHERE death = 1;

        WHILE endOfResults = 0 DO
                FETCH cur_rule INTO var1, var2;

                SET @pval = -1;
                WHILE @pval <= 1 DO
                SET @pflag = CASE @pval
                        WHEN -1 THEN '_lo'
                        WHEN 0 THEN '_norm'
                        WHEN 1 THEN '_hi'
                END;
                SET @aval = -1;
                WHILE @aval <= 1 DO
                SET @aflag = CASE @aval
                        WHEN -1 THEN '_lo'
                        WHEN 0 THEN '_norm'
                        WHEN 1 THEN '_hi'
                END;

                SET @s = CONCAT('SELECT COUNT(id) INTO @d0_count ',
                        'FROM ', var1, ' AS p ',
                        'INNER JOIN ',
                        var2, ' AS a ',
                        'USING (id) ',
                        'WHERE p.death = 0 AND p.dvalue = ', @pval, ' ',
                        'AND a.dvalue = ', @aval);
                PREPARE stmt FROM @s;
                EXECUTE stmt;
                DEALLOCATE PREPARE stmt;

                SET @s = CONCAT('SELECT COUNT(id) INTO @d1_count ',
                        'FROM ', var1, ' AS p ',
                        'INNER JOIN ',
                        var2, ' AS a ',
                        'USING (id) ',
                        'WHERE p.death = 1 AND p.dvalue = ', @pval, ' ',
                        'AND a.dvalue = ', @aval);
                PREPARE stmt FROM @s;
                EXECUTE stmt;
                DEALLOCATE PREPARE stmt;

                SET @s = CONCAT('SELECT COUNT(id) INTO @ccount ',
                        'FROM ', var1, ' AS p ',
                        'INNER JOIN ',
                        var2, ' AS a ',
                        'USING (id) ',
                        'WHERE p.dvalue = ', @pval, ' ',
                        'AND a.dvalue = ', @aval);
                PREPARE stmt FROM @s;
                EXECUTE stmt;
                DEALLOCATE PREPARE stmt;

                INSERT INTO rules (prec, ante, supp0, conf0, supp1, conf1)
                VALUES (
                        CONCAT(var1, @pflag),
                        CONCAT(var2, @aflag),
                        @d0_count,
                        @d0_count / (@ccount * 0.01),
                        @d1_count,
                        @d1_count / (@ccount * 0.01)
                );
                SET @aval = @aval + 1;
                END WHILE;
                SET @s = CONCAT('SELECT COUNT(id) INTO @d0_count ',
                        'FROM ', var1, ' AS p ',
                        'INNER JOIN ',
                        var2, ' AS a ',
                        'USING (id) ',
                        'WHERE p.death = 0 AND p.dvalue = ', @pval, ' ',
                        'AND a.dvalue <> 0');
                PREPARE stmt FROM @s;
                EXECUTE stmt;
                DEALLOCATE PREPARE stmt;
                SET @s = CONCAT('SELECT COUNT(id) INTO @d1_count ',
                        'FROM ', var1, ' AS p ',
                        'INNER JOIN ',
                        var2, ' AS a ',
                        'USING (id) ',
                        'WHERE p.death = 1 AND p.dvalue = ', @pval, ' ',
                        'AND a.dvalue <> 0');
                PREPARE stmt FROM @s;
                EXECUTE stmt;
                DEALLOCATE PREPARE stmt;
                SET @s = CONCAT('SELECT COUNT(id) INTO @ccount ',
                        'FROM ', var1, ' AS p ',
                        'INNER JOIN ',
                        var2, ' AS a ',
                        'USING (id) ',
                        'WHERE p.dvalue = ', @pval, ' ',
                        'AND a.dvalue <> 0');
                PREPARE stmt FROM @s;
                EXECUTE stmt;
                DEALLOCATE PREPARE stmt;

                INSERT INTO rules (prec, ante, supp0, conf0, supp1, conf1)
                VALUES (
                        CONCAT(var1, @pflag),
                        CONCAT(var2, '_ab'),
                        @d0_count,
                        @d0_count / (@ccount * 0.01),
                        @d1_count,
                        @d1_count / (@ccount * 0.01)
                );
                SET @pval = @pval + 1;
                END WHILE;
                SET @s = CONCAT('SELECT COUNT(id) INTO @d0_count ',
                        'FROM ', var1, ' AS p ',
                        'INNER JOIN ',
                        var2, ' AS a ',
                        'USING (id) ',
                        'WHERE p.death = 0 AND p.dvalue <> 0 ',
                        'AND a.dvalue <> 0');
                PREPARE stmt FROM @s;
                EXECUTE stmt;
                DEALLOCATE PREPARE stmt;
                SET @s = CONCAT('SELECT COUNT(id) INTO @d1_count ',
                        'FROM ', var1, ' AS p ',
                        'INNER JOIN ',
                        var2, ' AS a ',
                        'USING (id) ',
                        'WHERE p.death = 1 AND p.dvalue <> 0 ',
                        'AND a.dvalue <> 0');
                PREPARE stmt FROM @s;
                EXECUTE stmt;
                DEALLOCATE PREPARE stmt;
                SET @s = CONCAT('SELECT COUNT(id) INTO @ccount ',
                        'FROM ', var1, ' AS p ',
                        'INNER JOIN ',
                        var2, ' AS a ',
                        'USING (id) ',
                        'WHERE p.dvalue <> 0 '
                        'AND a.dvalue <> 0');
                PREPARE stmt FROM @s;
                EXECUTE stmt;
                DEALLOCATE PREPARE stmt;

                INSERT INTO rules (prec, ante, supp0, conf0, supp1, conf1)
                VALUES (
                        CONCAT(var1, '_ab'),
                        CONCAT(var2, '_ab'),
                        @d0_count,
                        @d0_count / (@ccount * 0.01),
                        @d1_count,
                        @d1_count / (@ccount * 0.01)
                );
        END WHILE;
        CLOSE cur_rule;
END//
DELIMITER ;
