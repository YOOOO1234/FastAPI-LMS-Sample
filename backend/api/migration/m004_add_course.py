from sqlalchemy.ext.asyncio import AsyncSession
import datetime

import api.models.course as course_model

def add_course(db:AsyncSession):
    rows = [
            course_model.Course(
                id = 1,
                course_name = "sample_course",
                course_year = "2022年度",
                course_term = "後学期",
                subject_name = "sample_subject",
                course_week = "第1週",
                start_date_time = datetime.datetime(2022,2,10,0,0,0),
                end_date_time = datetime.datetime(2023,2,10,0,0,0),
                created = datetime.datetime(2022,2,10,0,0,0),
                created_by = 2
            )
    ]
    for row in rows:
        db.add(row)
    db.flush()
        