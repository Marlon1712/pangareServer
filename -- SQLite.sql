-- SQLite
DROP TABLE IF EXISTS uip;

DELETE FROM uip WHERE id > 0;

SELECT DataHora, processados, produzidos, expulsos, porcentagem_expulsos FROM uip


INSERT INTO uip (DataHora, processados, produzidos, expulsos, porcentagem_expulsos) VALUES (datetime('now'), 10000, 9000, 1000, 1);

INSERT INTO uip (DataHora, processados, produzidos, expulsos, porcentagem_expulsos) VALUES (datetime('now'), abs(random()) % (10 - 1) + 1, abs(random()) % (10 - 1) + 1, abs(random()) % (10 - 1) + 1, abs(random()) % (10 - 1) + 1);