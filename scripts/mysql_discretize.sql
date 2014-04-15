USE icu;
UPDATE vstats AS v LEFT JOIN pinfo AS p ON v.id = p.id
SET v.dvalue =
        CASE
        WHEN v.var = "Albumin" THEN
                CASE
                WHEN v.value < 3.5 THEN -1
                WHEN v.value > 5 THEN 1
                ELSE 0
                END
        WHEN v.var = "ALP" THEN
                CASE
                WHEN v.value < 20 THEN -1
                WHEN v.value > 140 THEN 1
                ELSE 0
                END
        WHEN v.var = "ALT" THEN
                CASE
                WHEN gender = 0 THEN
                        CASE
                        WHEN v.value < 0 THEN -1
                        WHEN v.value > 34 THEN 1
                        ELSE 0
                        END
                ELSE
                        CASE
                        WHEN v.value < 0 THEN -1
                        WHEN v.value > 45 THEN 1
                        ELSE 0
                        END
                END
        WHEN v.var = "AST" THEN
                CASE
                WHEN gender = 0 THEN
                        CASE
                        WHEN v.value < 6 THEN -1
                        WHEN v.value > 34 THEN 1
                        ELSE 0
                        END
                ELSE
                        CASE
                        WHEN v.value < 8 THEN -1
                        WHEN v.value > 40 THEN 1
                        ELSE 0
                        END
                END
        WHEN v.var = "Bilirubin" THEN
                CASE
                WHEN v.value < 0 THEN -1
                WHEN v.value > 2.09 THEN 1
                ELSE 0
                END
        WHEN v.var = "BUN" THEN
                CASE
                WHEN v.value < 6 THEN -1
                WHEN v.value > 20 THEN 1
                ELSE 0
                END
        WHEN v.var = "Cholesterol" THEN
                CASE
                WHEN v.value < 0 THEN -1
                WHEN v.value > 200 THEN 1
                ELSE 0
                END
        WHEN v.var = "Creatinine" THEN
                CASE
                WHEN gender = 0 THEN
                        CASE
                        WHEN v.value < 0.5 THEN -1
                        WHEN v.value > 1 THEN 1
                        ELSE 0
                        END
                ELSE
                        CASE
                        WHEN v.value < 0.7 THEN -1
                        WHEN v.value > 1.2 THEN 1
                        ELSE 0
                        END
                END
        WHEN v.var = "DiasABP" THEN
                CASE
                WHEN v.value < 60 THEN -1
                WHEN v.value > 79 THEN 1
                ELSE 0
                END
        WHEN v.var = "FiO2" THEN
                CASE
                WHEN v.value < 0 THEN -1
                WHEN v.value > 1 THEN 1
                ELSE 0
                END
        WHEN v.var = "GCS" THEN
                CASE
                WHEN v.value < 3 THEN -1
                WHEN v.value > 15 THEN 1
                ELSE 0
                END
        WHEN v.var = "Glucose" THEN
                CASE
                WHEN v.value < 79.2 THEN -1
                WHEN v.value < 110 THEN 1
                ELSE 0
                END
        WHEN v.var = "HCO3" THEN
                CASE
                WHEN v.value < 18 THEN -1
                WHEN v.value < 23 THEN 1
                ELSE 0
                END
        WHEN v.var = "HCT" THEN
                CASE
                WHEN gender = 0 THEN
                        CASE
                        WHEN v.value < 35 THEN -1
                        WHEN v.value > 48 THEN 1
                        ELSE 0
                        END
                ELSE
                        CASE
                        WHEN v.value < 39 THEN -1
                        WHEN v.value > 62 THEN 1
                        ELSE 0
                        END
                END
        WHEN v.var = "HR" THEN
                CASE
                WHEN v.value < 60 THEN -1
                WHEN v.value > 100 THEN 1
                ELSE 0
                END
        WHEN v.var = "K" THEN
                CASE
                WHEN v.value < 3.5 THEN -1
                WHEN v.value > 5 THEN 1
                ELSE 0
                END
        WHEN v.var = "Lactate" THEN
                CASE
                WHEN v.value < 0.5 THEN -1
                WHEN v.value < 2 THEN 1
                ELSE 0
                END
        WHEN v.var = "Mg" THEN
                CASE
                WHEN v.value < 0.6 THEN -1
                WHEN v.value > 0.95 THEN 1
                ELSE 0
                END
        WHEN v.var = "MAP" THEN
                CASE
                WHEN v.value < 70 THEN -1
                WHEN v.value > 110 THEN 1
                ELSE 0
                END
        WHEN v.var = "MechVent" THEN v.value
        WHEN v.var = "Na" THEN
                CASE
                WHEN v.value < 135 THEN -1
                WHEN v.value > 147 THEN 1
                ELSE 0
                END
        WHEN v.var = "NIDiasABP" THEN
                CASE
                WHEN v.value < 60 THEN -1
                WHEN v.value > 79 THEN 1
                ELSE 0
                END
        WHEN v.var = "NIMAP" THEN
                CASE
                WHEN v.value < 70 THEN -1
                WHEN v.value > 110 THEN 1
                ELSE 0
                END
        WHEN v.var = "NISysABP" THEN
                CASE
                WHEN v.value < 90 THEN -1
                WHEN v.value > 110 THEN 1
                ELSE 0
                END
        WHEN v.var = "PaCO2" THEN
                CASE
                WHEN v.value < 35 THEN -1
                WHEN v.value > 45 THEN 1
                ELSE 0
                END
        WHEN v.var = "PaO2" THEN
                CASE
                WHEN v.value < 75 THEN -1
                WHEN v.value > 100 THEN 1
                ELSE 0
                END
        WHEN v.var = "pH" THEN
                CASE
                WHEN v.value < 7.34 THEN -1
                WHEN v.value > 7.44 THEN 1
                ELSE 0
                END
        WHEN v.var = "Platelets" THEN
                CASE
                WHEN v.value < 150 THEN -1
                WHEN v.value > 450 THEN 1
                ELSE 0
                END
        WHEN v.var = "RespRate" THEN
                CASE
                WHEN v.value < 18 THEN -1
                WHEN v.value > 22 THEN 1
                ELSE 0
                END
        WHEN v.var = "SaO2" THEN
                CASE
                WHEN v.value < 95 THEN -1
                WHEN v.value > 100 THEN 1
                ELSE 0
                END
        WHEN v.var = "SysABP" THEN
                CASE
                WHEN v.value < 90 THEN -1
                WHEN v.value > 119 THEN 1
                ELSE 0
                END
        WHEN v.var = "Temp" THEN
                CASE
                WHEN v.value < 36.3 THEN -1
                WHEN v.value > 37.3 THEN 1
                ELSE 0
                END
        WHEN v.var = "TropI" THEN
                CASE
                WHEN v.value < 0 THEN -1
                WHEN v.value > 10 THEN 1
                ELSE 0
                END
        WHEN v.var = "TropT" THEN
                CASE
                WHEN v.value < 0 THEN -1
                WHEN v.value > 0.1 THEN 1
                ELSE 0
                END
        WHEN v.var = "Urine" THEN 0
        WHEN v.var = "WBC" THEN
                CASE
                WHEN v.value < 3.5 THEN -1
                WHEN v.value > 11 THEN 1
                ELSE 0
                END
        WHEN v.var = "Weight" THEN 0
        END;
