from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session
from sqlalchemy import or_
from slowapi import Limiter
from slowapi.util import get_remote_address

from auth import get_current_user, require_admin, get_password_hash
from database import get_db
import models
import schemas
from logger import logger  # 新增：导入日志模块

limiter = Limiter(key_func=get_remote_address)
router = APIRouter(prefix="/users", tags=["用户管理"])


@router.get("/me", response_model=schemas.ResponseModel[schemas.UserResponse], name="获取当前用户")
def get_current_user_info(current_user: models.User = Depends(get_current_user)):
    """获取当前登录用户的详细信息"""
    logger.debug(f"获取当前用户信息: user_id={current_user.id}, email={current_user.email}")
    return schemas.success_response(data=current_user)


@router.post("/", response_model=schemas.ResponseModel[schemas.UserResponse], name="创建用户")
@limiter.limit("10/minute")
def create_user(
    request: Request,
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
    _: models.User = Depends(require_admin)
):
    """管理员创建新用户"""
    logger.info(
        f"管理员创建用户 | admin_id={current_user.id} admin_email={current_user.email} | "
        f"new_user={user.email} name={user.name} role={user.role}"
    )
    
    existing = db.query(models.User).filter(models.User.email == user.email).first()
    if existing:
        logger.warning(f"创建用户失败: 邮箱已存在 - {user.email}")
        raise HTTPException(status_code=400, detail="邮箱已被注册")
    
    db_user = models.User(
        name=user.name,
        email=user.email,
        hashed_password=get_password_hash(user.password),
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    logger.info(f"用户创建成功 | new_user_id={db_user.id} email={db_user.email} role={db_user.role.value}")
    return schemas.success_response(data=db_user, message="用户创建成功")


@router.get("/", response_model=schemas.ResponseModel[schemas.PageResponse[schemas.UserResponse]], name="获取用户列表")
def get_users(
    page: int = Query(1, ge=1, description="页码，从1开始"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量，最大100"),
    keyword: str = Query("", description="搜索关键词，匹配姓名或邮箱"),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """分页获取用户列表，支持按姓名或邮箱模糊搜索"""
    logger.debug(
        f"查询用户列表 | user_id={current_user.id} | "
        f"page={page} page_size={page_size} keyword='{keyword}'"
    )
    
    query = db.query(models.User)
    
    if keyword:
        query = query.filter(
            or_(
                models.User.name.like(f"%{keyword}%"),
                models.User.email.like(f"%{keyword}%")
            )
        )
    
    total = query.count()
    offset = (page - 1) * page_size
    users = query.order_by(models.User.id.desc()).offset(offset).limit(page_size).all()
    
    logger.debug(f"查询用户列表完成 | total={total} returned={len(users)}")
    
    page_data = schemas.PageResponse(
        total=total,
        page=page,
        page_size=page_size,
        items=users
    )
    
    return schemas.success_response(data=page_data)


@router.get("/{user_id}", response_model=schemas.ResponseModel[schemas.UserResponse], name="获取单个用户")
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """根据 ID 获取单个用户信息"""
    logger.debug(f"查询单个用户 | requestor_id={current_user.id} target_id={user_id}")
    
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        logger.warning(f"查询用户失败: 用户不存在 - user_id={user_id}")
        raise HTTPException(status_code=404, detail="用户不存在")
    
    logger.debug(f"查询用户成功 | target_id={user_id} email={user.email}")
    return schemas.success_response(data=user)


@router.put("/{user_id}", response_model=schemas.ResponseModel[schemas.UserResponse], name="更新用户")
def update_user(
    user_id: int,
    user_update: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """更新用户信息"""
    logger.info(
        f"更新用户请求 | requestor_id={current_user.id} target_id={user_id} | "
        f"update_fields={list(user_update.model_dump(exclude_unset=True).keys())}"
    )
    
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        logger.warning(f"更新用户失败: 用户不存在 - user_id={user_id}")
        raise HTTPException(status_code=404, detail="用户不存在")
    
    # 记录原始值（用于日志对比）
    old_email = user.email
    old_name = user.name
    old_role = user.role.value if user.role else None
    
    update_data = user_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)
    
    db.commit()
    db.refresh(user)
    
    # 记录变更详情
    changes = []
    if old_email != user.email:
        changes.append(f"email: {old_email} -> {user.email}")
    if old_name != user.name:
        changes.append(f"name: {old_name} -> {user.name}")
    if old_role != user.role.value:
        changes.append(f"role: {old_role} -> {user.role.value}")
    
    logger.info(
        f"用户更新成功 | target_id={user_id} | "
        f"changes: {', '.join(changes) if changes else '无变更'}"
    )
    
    return schemas.success_response(data=user, message="用户更新成功")


@router.delete("/{user_id}", response_model=schemas.ResponseModel, name="删除用户")
@limiter.limit("10/minute")
def delete_user(
    request: Request,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
    _: models.User = Depends(require_admin)
):
    """管理员删除用户"""
    logger.warning(
        f"删除用户请求 | admin_id={current_user.id} admin_email={current_user.email} | "
        f"target_user_id={user_id}"
    )
    
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        logger.warning(f"删除用户失败: 用户不存在 - user_id={user_id}")
        raise HTTPException(status_code=404, detail="用户不存在")
    
    if user.id == current_user.id:
        logger.warning(f"删除用户失败: 尝试删除自己 - admin_id={current_user.id}")
        raise HTTPException(status_code=400, detail="不能删除自己")
    
    # 记录被删除用户的信息（用于审计）
    deleted_user_info = f"id={user.id} email={user.email} name={user.name} role={user.role.value}"
    
    db.delete(user)
    db.commit()
    
    logger.warning(f"用户已删除 | {deleted_user_info} | executed_by={current_user.id}")
    return schemas.success_response(message=f"用户 {user_id} 已删除")