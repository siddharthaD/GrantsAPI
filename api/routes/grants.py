from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, UploadFile, Form
from sqlalchemy.orm import Session
from starlette import status

from api.dependencies import get_current_user
from core.models.app_models import User, GrantStatus, ApplicationBase, ApplicationCreate, ApplicationFilesBase
from core.repository import GrantRepository
from core.repository import ApplicationRepository
from core.repository import OrganisationRepository
from database.db import get_session

grants = APIRouter(tags=["Grants"])


@grants.get("/{grant_id}")
async def get_grant_details(grant_id: int, db: Annotated[Session, Depends(get_session)]):
    return GrantRepository.get_grant_by_id(db, grant_id)


@grants.post("/{grant_id}/apply")
async def create_grant_application(grant_id: int,
                                   title:Annotated[str, Form()],
                                   description: Annotated[str, Form()],
                                   application: ApplicationBase,
                                   files: List[UploadFile],
                                   db: Annotated[Session, Depends(get_session)],
                                   current_user: Annotated[User, Depends(get_current_user)]):
    grant_details = GrantRepository.get_grant_by_id(db=db, grant_id=grant_id)
    if not grant_details:
        raise HTTPException(status_code=status.HTTP_404_BAD_REQUEST,
                            detail="This grant couldn't be found")

    if grant_details.status != GrantStatus.APPLICATION:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                            detail="This grant is not accepting any submissions"
                            )

    # Verify if the user is eligible to apply for the grant
    if not OrganisationRepository.is_user_member_organisation(db=db, user_id=current_user.id,
                                                              organisation_id=grant_details.organisation_id):
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                            detail="You are not allowed to apply for this grant"
                            )
    org_details = OrganisationRepository.get_org_by_id(db=db, id=grant_details.organisation_id)
    if org_details.super_admin_id == current_user.id:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                            detail="You are not allowed to apply for a grant with this organisation"
                            )

    application_id = -1
    try:
        appl_create_det = ApplicationCreate(grant_id=grant_id,
                                            applicant_id=current_user.id,
                                            title=title,
                                            description=description)

        application_id = ApplicationRepository.create_application(db, appl_create_det)
        for file in files:
            app_file = ApplicationFilesBase()
            app_file.description = file.filename
            app_file.file_storage_key = file.read(1024)
            ApplicationRepository.upload_file(db, app_file, application_id, current_user.id)
    except Exception as e:
        if application_id > 0:
            return {"message": f"Application with {application_id} to the grant is created. You need to retry "
                               f"uploading supporting documents"}
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Unavoidable problem occured. Retry later"
                            )
    return {"message": f"Application with {application_id} to the grant is created. You can manage the application"}
