CREATE TABLE IF NOT EXISTS Application (
    app_id INT AUTO_INCREMENT PRIMARY KEY,
    app_name VARCHAR(255) NOT NULL,
    app_avg FLOAT,
    app_ifeval FLOAT,
    app_bbh FLOAT,
    app_mathlvl5 FLOAT,
    app_gpqa FLOAT,
    app_musr FLOAT,
    app_mmlupro FLOAT
);

INSERT INTO Application (app_name, app_avg, app_ifeval, app_bbh, app_mathlvl5, app_gpqa, app_musr, app_mmlupro) 
VALUES
('APP1', 85.24, 84.32, 78.25, 94.65, 90.55, 76.32, 90.48),
('APP2', 88.54, 97.42, 65.02, 89.56, 85.56, 78.22, 84.54),
('APP3', 75.26, 75.19, 68.62, 85.78, 81.25, 85.26, 89.62),
('APP4', 98.54, 98.02, 78.78, 74.26, 84.05, 97.09, 76.49);

CREATE TABLE IF NOT EXISTS Storage (
    storage_id INT AUTO_INCREMENT PRIMARY KEY,
    ip_address VARCHAR(45) NOT NULL,  -- 45 chars to accommodate IPv6
    port INT NOT NULL
);