import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session
from unigate.core.database import get_session
from unigate.crud.blocked_crud import blocked_crud
from unigate.crud.group_crud import group_crud
from unigate.crud.join_crud import join_crud
from unigate.crud.request_crud import request_crud
from unigate.crud.student_crud import student_crud
from unigate.models import Group, Student
from unigate.models.request_response_model import RequestResponse

router = APIRouter()


# routes/groups.py
@router.get(
    "/get",
    response_model=list[Group],
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "A list of all available groups", "model": list[Group]},
        500: {"description": "Unable to load groups due to a server error"},
    },
)
def get_groups() -> list[Group]:
    """
    Retrieve a list of all available groups.

    This endpoint fetches all group entries from the database.

    Returns:
    - **200 OK**: A list of all groups, each represented by a `Group` model.
    - **500 Internal Server Error**: An error occurred while attempting to load the groups.
    """
    try:
        return group_crud.get_multi()
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Unable to load groups.")


@router.post(
    "/create",
    response_model=Group,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Group successfully created", "model": Group},
        400: {"description": "Validation error while creating the group"},
        500: {"description": "An error occurred while creating the group"},
    },
)
def create_group(
    group_data: Group,
    session: Session = Depends(get_session),
) -> Group:
    """
    Creates a new group in the system.

    - **name**: The unique name of the group.
    - **description**: (Optional) A brief description of the group's purpose.
    - **category**: (Optional) The category this group belongs to.
    - **type**: The type of group, either "Public" or "Private".
    - **creator_id**: The ID of the user creating the group.

    This endpoint checks for duplicate group names before creating a new group.
    """
    try:
        return group_crud.create_group(session=session, group_data=group_data)
    except HTTPException:
        raise  # Re-raise any HTTPExceptions for client handling
    except Exception:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the group.",
        )


@router.get(
    "/{group_id}/get_members",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "List of all students in the group",
            "model": list[Student],
        },
        400: {
            "description": "You cannot visualize members of a private group of which you are not part of"
        },
        500: {"description": "An error occurred while creating the group"},
    },
)
def get_members(group_id: uuid.UUID) -> list[Student]:
    try:
        # Todo: it should be the authenticated user
        auth_user = uuid.uuid4()
        return student_crud.get_members(group_id=group_id, student_id=auth_user)

    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Internal server error.")


@router.post("/join_public_group", response_model=str)
def join_public_group(student_id: uuid.UUID, group_id: uuid.UUID) -> str:
    """
    Join a public group (if not already enrolled in another group for the same course).

    Args:
        student_id (UUID): student's user ID
        group_id (UUID): group's user ID

    Returns:
        bool: returns wether the join has failed ro not.

    Raises:
        HTTPException: Raises a 500 error if the query fails.
    """

    try:
        return join_crud.join_public_group(student_id, group_id)
    except HTTPException:
        # Reraise HTTPException to return appropriate error message
        raise
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Internal server error.")


@router.post("/join_private_group", response_model=str)
def join_private_group(student_id: uuid.UUID, group_id: uuid.UUID) -> str:
    try:
        # Check if the student is blocked in the group
        if blocked_crud.is_student_blocked(student_id, group_id):
            raise HTTPException(
                status_code=403,
                detail="The student is blocked from joining this group.",
            )
        # Proceed with creating the join request if the student is not blocked
        return join_crud.join_private_group(student_id, group_id)

    except HTTPException:
        raise
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Internal server error.")


@router.post("/get_student_groups", response_model=list[Group])
def get_student_groups(student_id: uuid.UUID) -> list[Group]:
    try:
        return join_crud.get_student_groups(student_id)
    except SQLAlchemyError:
        # Generic SQLAlchemy error handling
        raise HTTPException(status_code=500, detail="Internal server error.")


@router.get("/{id}", response_model=dict)
def get_group(id: uuid.UUID) -> dict:
    group = group_crud.get(id=id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found.")
    group_dict = group.model_dump()
    group_dict["is_super_student"] = group.is_super_student
    group_dict["is_member_of"] = group.is_member_of

    return group_dict


@router.get("/{group_id}/requests", response_model=list[RequestResponse])
def get_group_requests(group_id: uuid.UUID) -> list[RequestResponse]:
    group = group_crud.get(id=group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found.")

    return request_crud.get_all_requests_for_group(group_id=group_id)


@router.post("/{group_id}/leave", response_model=str)
def leave_group(group_id: uuid.UUID, student_id: uuid.UUID) -> str:
    return join_crud.remove_student(group_id=group_id, student_id=student_id)


@router.get("/{group_id}/blocked_users", response_model=list[dict])
def get_blocked_users(group_id: uuid.UUID) -> list[dict]:
    """
    Retrieve a list of blocked users for a specific group.

    Args:
        group_id (UUID): The ID of the group.

    Returns:
        list[dict]: A list of dictionaries containing the names and surnames of the blocked students.

    Raises:
        HTTPException: If the group does not exist or if there is an internal server error.
    """
    try:
        # Check if the group exists
        group = group_crud.get(id=group_id)
        if not group:
            raise HTTPException(status_code=404, detail="Group not found.")

        # Fetch blocked students for the group
        return blocked_crud.get_blocked_students(group_id=group_id)
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Internal server error.")


@router.post("/{group_id}/unblock_user", response_model=str)
def unblock_user(group_id: uuid.UUID, student_id: uuid.UUID) -> str:
    """
    Unblock a student from a group.

    Args:
        group_id (UUID): The ID of the group.
        student_id (UUID): The ID of the student to unblock.

    Returns:
        str: A message indicating the success or failure of the operation.

    Raises:
        HTTPException: If the group does not exist, if the student is not blocked, or if there is an internal server error.
    """
    try:
        # Check if the group exists
        group = group_crud.get(id=group_id)
        if not group:
            raise HTTPException(status_code=404, detail="Group not found.")

        # Check if the student exists
        student = student_crud.get_by_id(id=student_id)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found.")

        # Unblock the student
        return blocked_crud.unblock_student(student_id=student_id, group_id=group_id)
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Internal server error.")


@router.post("/{group_id}/block_user", response_model=dict)
def block_student(student_id: uuid.UUID, group_id: uuid.UUID):
    try:
        result = blocked_crud.block_student(student_id=student_id, group_id=group_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    if result == "The group doesn't exist" or result == "The student doesn't exist":
        raise HTTPException(status_code=404, detail=result)
    if result == "The student is already blocked in this group":
        raise HTTPException(status_code=409, detail=result)

    return {"message": result}
