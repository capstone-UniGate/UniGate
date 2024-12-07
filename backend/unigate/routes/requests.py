import uuid

from fastapi import APIRouter, HTTPException
from unigate.crud.request_crud import request_crud
from unigate.models import Request

router = APIRouter()


@router.post("/{request_id}/approve", response_model=Request)
def approve_group_request(request_id: uuid.UUID) -> Request:
    request = request_crud.get(id=request_id)

    if not request:
        raise HTTPException(
            status_code=404, detail="Request not found or does not belong to the group."
        )

    return request_crud.approve_request(request_id=request_id)


@router.post("/{request_id}/reject", response_model=Request)
def reject_group_request(request_id: uuid.UUID) -> Request:
    request = request_crud.get(id=request_id)
    if not request:
        raise HTTPException(
            status_code=404, detail="Request not found or does not belong to the group."
        )

    return request_crud.reject_request(request_id=request_id)
