from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI(title="Microservicio Historial Médico")

DB_CONFIG = {
    "host": "localhost",
    "dbname": "clinical_historial",
    "user": "ms_clinical_historial",
    "password": "Ms_Clinical_Historial",
    "port": 5432,
}


def get_connection():
    return psycopg2.connect(
        host=DB_CONFIG["host"],
        dbname=DB_CONFIG["dbname"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        port=DB_CONFIG["port"],
        cursor_factory=RealDictCursor
    )


class MedicalRecordCreate(BaseModel):
    patient_id: int = Field(alias="patientId")
    doctor_id: int = Field(alias="doctorId")
    diagnosis: str
    treatment: str
    date: Optional[str] = None

    class Config:
        populate_by_name = True


app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def home():
    return FileResponse("static/index.html")


@app.get("/records/{patient_id}")
def get_records(patient_id: int):
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT
                id,
                patient_id,
                doctor_id,
                diagnosis,
                treatment,
                record_date AS date
            FROM medical_records
            WHERE patient_id = %s
            ORDER BY record_date DESC, id DESC
        """, (patient_id,))

        rows = cur.fetchall()

        cur.close()
        conn.close()

        return rows

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/records")
def create_record(record: MedicalRecordCreate):
    try:
        conn = get_connection()
        cur = conn.cursor()

        if record.date:
            cur.execute("""
                INSERT INTO medical_records
                (patient_id, doctor_id, diagnosis, treatment, record_date)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
            """, (
                record.patient_id,
                record.doctor_id,
                record.diagnosis,
                record.treatment,
                record.date
            ))
        else:
            cur.execute("""
                INSERT INTO medical_records
                (patient_id, doctor_id, diagnosis, treatment)
                VALUES (%s, %s, %s, %s)
                RETURNING id
            """, (
                record.patient_id,
                record.doctor_id,
                record.diagnosis,
                record.treatment
            ))

        row = cur.fetchone()
        new_id = row["id"]

        conn.commit()

        cur.close()
        conn.close()

        return {
            "message": "Registro médico creado correctamente",
            "record_id": new_id
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))