from fastapi import APIRouter

from unigate import crud
from unigate.models import Group
from unigate.schemas.group import GroupRead

router = APIRouter()


@router.get(
    "",
    response_model=list[GroupRead],
)
def get_groups() -> list[Group]:
    return crud.group.get_multi()


# @router.post(
#     "/create",
#     response_model=Group,
#     status_code=status.HTTP_201_CREATED,
#     responses={
#         201: {"description": "Group successfully created", "model": Group},
#         400: {"description": "Validation error while creating the group"},
#         500: {"description": "An error occurred while creating the group"},
#     },
# )
# def create_group(
#     group_data: Group,
#     session: Session = Depends(get_session),
#     current_user: User = Depends(get_current_user),
# ) -> Group:
#     """
#     Creates a new group in the system.

#     - **name**: The unique name of the group.
#     - **description**: (Optional) A brief description of the group's purpose.
#     - **category**: (Optional) The category this group belongs to.
#     - **type**: The type of group, either "Public" or "Private".
#     - **creator_id**: The ID of the user creating the group.

#     This endpoint checks for duplicate group names before creating a new group.
#     """
#     try:
#         # TODO: remove session & tweak the crud to handle the current_user
#         group = Group(**group_data.model_dump(), creator_id=current_user.number)
#         return group.create_group(session=session, group_data=group)
#     except HTTPException:
#         raise  # Re-raise any HTTPExceptions for client handling
#     except Exception:
#         session.rollback()
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail="An error occurred while creating the group.",
#         )


# @router.get(
#     "/get_members",
#     status_code=status.HTTP_200_OK,
#     responses={
#         200: {
#             "description": "List of all students in the group",
#             "model": list[Student],
#         },
#         400: {
#             "description": "You cannot visualize members of a private group of which you are not part of"
#         },
#         500: {"description": "An error occurred while creating the group"},
#     },
# )
# def get_members(group_id: uuid.UUID, student_id: uuid.UUID | None) -> list[Student]:
#     try:
#         return student.get_members(group_id=group_id, student_id=student_id)

#     except SQLAlchemyError:
#         raise HTTPException(status_code=500, detail="Internal server error.")


# @router.post("/join_public_group", response_model=str)
# def join_public_group(student_id: uuid.UUID, group_id: uuid.UUID) -> str:
#     """
#     Join a public group (if not already enrolled in another group for the same course).

#     Args:
#         student_id (UUID): student's user ID
#         group_id (UUID): group's user ID

#     Returns:
#         bool: returns wether the join has failed ro not.

#     Raises:
#         HTTPException: Raises a 500 error if the query fails.
#     """

#     try:
#         return join_crud.join_public_group(student_id, group_id)
#     except HTTPException:
#         # Reraise HTTPException to return appropriate error message
#         raise
#     except SQLAlchemyError:
#         raise HTTPException(status_code=500, detail="Internal server error.")


# @router.post("/join_private_group", response_model=str)
# def join_private_group(student_id: uuid.UUID, group_id: uuid.UUID) -> str:
#     try:
#         # Use the create_request method from request_crud to create a new join request
#         return join_crud.join_private_group(student_id, group_id)

#         # Instead of returning the Request object, return a success message
#         # return "Join request submitted successfully."
#     except HTTPException:
#         # Reraise HTTPException to return appropriate error message
#         raise
#     except SQLAlchemyError:
#         # Generic SQLAlchemy error handling
#         raise HTTPException(status_code=500, detail="Internal server error.")


# @router.post("/get_student_groups", response_model=list[Group])
# def get_student_groups(student_id: uuid.UUID) -> list[Group]:
#     try:
#         return join_crud.get_student_groups(student_id)
#     except SQLAlchemyError:
#         # Generic SQLAlchemy error handling
#         raise HTTPException(status_code=500, detail="Internal server error.")


# @router.get("/{id}", response_model=dict)
# def get_group(id: uuid.UUID) -> dict:
#     group = group.get(id=id)
#     if not group:
#         raise HTTPException(status_code=404, detail="Group not found.")
#     group_dict = group.model_dump()
#     group_dict["is_super_student"] = group.is_super_student
#     group_dict["is_member_of"] = group.is_member_of

#     return group_dict


# @router.get("/{group_id}/requests", response_model=list[Request])
# def get_group_requests(group_id: uuid.UUID) -> list[Request]:
#     group = group.get(id=group_id)
#     if not group:
#         raise HTTPException(status_code=404, detail="Group not found.")

#     return request_crud.get_all_requests_for_group(group_id=group_id)