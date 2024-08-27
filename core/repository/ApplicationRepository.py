import datetime

from sqlalchemy.orm import Session
from core.models.app_models import Applications, ApplicationCreate, ApplicationFiles, ApplicationHistory,ApplicationFilesBase
from database.models import Applications as AppSchema, ApplicationFiles as AppFilesSchema, \
    ApplicationHistory as AppHistorySchema,ApplicationStatus


def get_application_by_id(db: Session, application_id: int) -> Applications | None:
    application = db.query(AppSchema).where(AppSchema.id == application_id).one_or_none()
    if not application:
        return None

    output = Applications(**application.__dict__)
    output.files = [ApplicationFiles(**file.__dict__) for file in
                    db.query(AppFilesSchema).where(AppFilesSchema.application_id == application_id)]
    output.history = [ApplicationHistory(**file.__dict__) for file in
                      db.query(AppHistorySchema).where(AppHistorySchema.application_id == application_id)]
    return output


def upload_file(db: Session, application_file: ApplicationFilesBase, application_id: int, user_id: int) -> bool:
    app_file = AppFilesSchema(**application_file.__dict__)
    app_file.application_id = application_id
    app_file.created_at = datetime.datetime.utcnow()
    db.add(app_file)

    app_history = AppHistorySchema(application_id=application_id)
    app_history.changed_at = datetime.datetime.utcnow()
    app_history.changed_by = user_id
    db.add(app_history)
    return True


def update_application_status(db: Session, application_id: int, user_id: int, application_status: str) -> bool:
    application = db.query(AppSchema).where(AppSchema.id == application_id).one_or_none()
    if not application:
        return False
    application.status = application_status
    application.changed_at = datetime.datetime.utcnow()
    application.changed_by = user_id

    app_history = AppHistorySchema(application_id=application_id)
    app_history.changed_at = datetime.datetime.utcnow()
    app_history.changed_by = user_id


def update_application(db: Session, appl_data: Applications, user_id: int) -> bool:
    try:
        appl_db = db.query(AppSchema).where(AppSchema.id == id).one_or_none()

        if appl_db.description != appl_data.description:
            appl_db.description = appl_data.description

        if appl_db.title != appl_data.title:
            appl_db.title = appl_data.title

        appl_db.changed_at = datetime.datetime.utcnow()
        appl_db.changed_by = user_id
        db.commit()
    except Exception as e:
        return False
    return True


def create_application(db: Session, appl_data: ApplicationCreate) -> int:
    appl = AppSchema(**appl_data.__dict__)
    appl.created_at = datetime.datetime.utcnow()
    appl.status = ApplicationStatus.CREATED
    appl.changed_by = appl_data.applicant_id
    db.add(appl)
    db.commit()
    db.refresh(appl)
    return appl.id
