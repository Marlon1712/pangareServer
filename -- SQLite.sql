-- SQLite
DROP TABLE IF EXISTS uip;

DELETE FROM uip WHERE id > 0;

SELECT DataHora, processados, produzidos, expulsos, porcentagem_expulsos FROM uip

SELECT * FROM uip

INSERT INTO uip (DataHora, processados, produzidos, expulsos, porcentagem_expulsos) VALUES (datetime('now'), 10000, 9000, 1000, 1);

INSERT INTO uip (DataHora, processados, produzidos, expulsos, porcentagem_expulsos) VALUES (datetime('now'), abs(random()) % (10 - 1) + 1, abs(random()) % (10 - 1) + 1, abs(random()) % (10 - 1) + 1, abs(random()) % (10 - 1) + 1);

UPDATE uip SET processados = 110077, porcentagem_processados = 80 WHERE id = 10