from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.api import deps
from app.core.database import get_db
from app.core.security import get_password_hash
from app.core.limiter import limiter
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.schemas.common import ResponseModel, PageResponse
from app.utils.logger import logger

router = APIRouter(prefix="/users", tags=["用户管理"])


@router.get("/me", response_model=ResponseModel[UserResponse])
def get_me(current_user: User = Depends(deps.get_current_user)):
    logger.debug(f"获取当前用户: user_id={current_user.id}")
    return ResponseModel.success(data=current_user)


@router.post("/", response_model=ResponseModel[UserResponse])
@limiter.limit("10/minute")
def create_user(
    request: Request,
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user),
    _: User = Depends(deps.require_admin)
):
    logger.info(f"管理员创建用户: admin_id={current_user.id}, new_user={user_data.email}")
    
    existing = db.query(User).filter(User.email == user_data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="邮箱已被注册")
    
    db_user = User(
        name=user_data.name,
        email=user_data.email,
        hashed_password=get_password_hash(user_data.password),
        role=user_data.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    logger.info(f"用户创建成功: user_id={db_user.id}")
    return ResponseModel.success(data=db_user, message="用户创建成功")


@router.get("/", response_model=ResponseModel[PageResponse[UserResponse]])
def get_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    keyword: str = Query(""),
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    query = db.query(User)
    
    if keyword:
        query = query.filter(
            or_(
                User.name.like(f"%{keyword}%"),
                User.email.like(f"%{keyword}%")
            )
        )
    
    total = query.count()
    offset = (page - 1) * page_size
    users = query.order_by(User.id.desc()).offset(offset).limit(page_size).all()
    
    return ResponseModel.success(data=PageResponse(
        total=total, page=page, page_size=page_size, items=users
    ))


@router.get("/{user_id}", response_model=ResponseModel[UserResponse])
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return ResponseModel.success(data=user)


@router.put("/{user_id}", response_model=ResponseModel[UserResponse])
def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    update_data = user_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)
    
    db.commit()
    db.refresh(user)
    return ResponseModel.success(data=user, message="用户更新成功")


@router.delete("/{user_id}", response_model=ResponseModel)
@limiter.limit("10/minute")
def delete_user(
    request: Request,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user),
    _: User = Depends(deps.require_admin)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    if user.id == current_user.id:
        raise HTTPException(status_code=400, detail="不能删除自己")
    
    db.delete(user)
    db.commit()
    
    logger.warning(f"管理员删除用户: admin_id={current_user.id}, deleted_user_id={user_id}")
    return ResponseModel.success(message=f"用户 {user_id} 已删除")