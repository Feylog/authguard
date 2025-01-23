from fastapi import APIRouter, Depends
from app.middlewares import verify_token

router = APIRouter()

@router.get("/admin/resource")
async def admin_resource(user=Depends(verify_token)):
    if user["role"] != "admin":
        return {"error": "Access denied"}
    return {"data": "This is a protected admin resource"}