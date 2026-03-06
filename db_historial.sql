
CREATE ROLE ms_clinical_historial
WITH LOGIN PASSWORD 'Ms_Clinical_Historial';

CREATE DATABASE clinical_historial
OWNER ms_clinical_historial
ENCODING 'UTF8';

GRANT ALL PRIVILEGES
ON DATABASE clinical_historial
TO ms_clinical_historial;

CREATE TABLE medical_records (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER NOT NULL,
    doctor_id INTEGER NOT NULL,
    diagnosis VARCHAR(255) NOT NULL,
    treatment TEXT NOT NULL,
    record_date DATE NOT NULL DEFAULT CURRENT_DATE
);

GRANT USAGE ON SCHEMA public TO ms_clinical_historial;

GRANT SELECT, INSERT, UPDATE, DELETE
ON TABLE medical_records
TO ms_clinical_historial;

GRANT USAGE, SELECT
ON SEQUENCE medical_records_id_seq
TO ms_clinical_historial;

INSERT INTO medical_records
(patient_id, doctor_id, diagnosis, treatment, record_date)
VALUES
(1, 2, 'Gripe', 'Medicamento X', '2026-04-01');

SELECT * FROM medical_records;



