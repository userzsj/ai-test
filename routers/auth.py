from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Query,Request
from sqlalchemy.orm import Session
from datetime import timedelta
import config
from database import get_db
import models
import schemas
from auth import get_password_hash, verify_password, create_access_token, get_current_user
from email_utils import send_verification_email, generate_verification_token, get_token_expiry
from datetime import datetime
from slowapi import Limiter
from slowapi.util import get_remote_address
from logger import logger
limiter = Limiter(key_func=get_remote_address)
router = APIRouter(prefix="/auth", tags=["认证"])


@router.post("/register", response_model=schemas.ResponseModel[schemas.UserResponse], name="用户注册")
@limiter.limit("3/minute")  # 同一 IP 每分钟最多注册 3 次
async def register(
    request: Request,  # 新增这个参数
    user_data: schemas.UserRegister,
    background_tasks: BackgroundTasks,  # 后台任务，不阻塞响应
    db: Session = Depends(get_db)
):
    """注册新用户，并发送验证邮件"""
    logger.info(f"用户注册请求: email={user_data.email}, name={user_data.name}")
    existing = db.query(models.User).filter(models.User.email == user_data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="邮箱已被注册")
    
    # 生成验证 Token
    verification_token = generate_verification_token()
    
    db_user = models.User(
        name=user_data.name,
        email=user_data.email,
        hashed_password=get_password_hash(user_data.password),
        role=models.UserRole.USER,
        is_verified=False,
        verification_token=verification_token,
        token_expires_at=get_token_expiry(hours=24)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # 后台发送验证邮件（不阻塞响应）
    background_tasks.add_task(
        send_verification_email,
        email=db_user.email,
        name=db_user.name,
        token=verification_token
    )
    logger.info(f"用户注册成功: user_id={db_user.id}, email={db_user.email}")
    return schemas.success_response(
        data=db_user, 
        message="注册成功！请查收邮件并点击链接验证邮箱。"
    )


@router.get("/verify", name="验证邮箱")
def verify_email(token: str = Query(..., description="验证 Token"), db: Session = Depends(get_db)):
    """通过 Token 验证邮箱"""
    logger.info(f"邮箱验证请求: token={token[:10]}...")
    user = db.query(models.User).filter(models.User.verification_token == token).first()
    
    if not user:
        raise HTTPException(status_code=400, detail="无效的验证链接")
    
    if user.is_verified:
        return schemas.success_response(message="邮箱已验证，无需重复验证")
    
    if user.token_expires_at < datetime.now():
        raise HTTPException(status_code=400, detail="验证链接已过期，请重新注册")
    
    # 验证通过
    user.is_verified = True
    user.verification_token = None
    user.token_expires_at = None
    db.commit()
    logger.info(f"邮箱验证成功: user_id={user.id}, email={user.email}")
    return schemas.success_response(message="邮箱验证成功！现在可以登录了。")

@router.post("/login", response_model=schemas.ResponseModel[schemas.LoginResponse], name="用户登录")
@limiter.limit("5/minute")
def login(
    request: Request,
    user_data: schemas.UserLogin,
    db: Session = Depends(get_db)
):
    logger.info(f"用户登录尝试: email={user_data.email}")
    
    user = db.query(models.User).filter(models.User.email == user_data.email).first()
    if not user:
        logger.warning(f"登录失败: 邮箱不存在 - {user_data.email}")
        raise HTTPException(status_code=401, detail="邮箱或密码错误")
    
    if not verify_password(user_data.password, user.hashed_password):
        logger.warning(f"登录失败: 密码错误 - {user_data.email}")
        raise HTTPException(status_code=401, detail="邮箱或密码错误")
    
    if not user.is_verified:
        logger.warning(f"登录失败: 邮箱未验证 - {user_data.email}")
        raise HTTPException(status_code=403, detail="邮箱未验证，请查收邮件并点击验证链接")
    
    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id), "role": user.role.value}
    )
    
    logger.info(f"用户登录成功: user_id={user.id}, email={user.email}, role={user.role.value}")
    
    login_response = schemas.LoginResponse(
        access_token=access_token,
        expires_in=config.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=schemas.UserResponse.model_validate(user)
    )
    
    return schemas.success_response(data=login_response, message="登录成功")


@router.post("/resend-verification", response_model=schemas.ResponseModel, name="重发验证邮件")
async def resend_verification(
    email: str = Query(..., description="注册邮箱"),
    background_tasks: BackgroundTasks = None,
    db: Session = Depends(get_db)
):
    """重发验证邮件"""
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    if user.is_verified:
        return schemas.success_response(message="邮箱已验证，无需重发")
    
    # 生成新的 Token
    user.verification_token = generate_verification_token()
    user.token_expires_at = get_token_expiry(hours=24)
    db.commit()
    
    # 发送邮件
    background_tasks.add_task(
        send_verification_email,
        email=user.email,
        name=user.name,
        token=user.verification_token
    )
    
    return schemas.success_response(message="验证邮件已重新发送，请查收")