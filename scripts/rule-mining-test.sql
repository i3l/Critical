USE icu;
SET profiling = 1;

DROP TABLE IF EXISTS prec;
DROP TABLE IF EXISTS ante;

CREATE TEMPORARY TABLE prec
AS (
        SELECT DISTINCT id
        FROM vstats AS v INNER JOIN outcome AS o USING (id)
        WHERE dvalue != 0 AND var = "MAP" AND death = 0
);
CREATE TEMPORARY TABLE ante 
AS (
        SELECT DISTINCT id
        FROM vstats AS v LEFT JOIN outcome AS o USING (id)
        WHERE dvalue != 0 AND var = "pH" AND death = 0
);
SET @prec_count = (SELECT COUNT(id) * 0.01 FROM prec);

SELECT COUNT(tmp.id) / (
                SELECT COUNT(DISTINCT id) * 0.01
                FROM vstats AS v LEFT JOIN outcome AS o USING (id)
                WHERE death = 0
        ) AS support
FROM (
        SELECT id
        FROM prec
        INNER JOIN ante
        USING (id)
) AS tmp;

SELECT COUNT(tmp.id) / (@prec_count) AS confidence
FROM (
        SELECT id
        FROM prec
        INNER JOIN ante
        USING (id)
) AS tmp;
SELECT SUM(Duration) AS Duration FROM information_schema.profiling;
SET profiling = 0;
