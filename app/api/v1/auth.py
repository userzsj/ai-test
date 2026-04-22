from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Query, Request
from sqlalchemy.orm import Session
from datetime import timedelta, datetime
from app.api import deps
from app.core.database import get_db
from app.core.config import settings
from app.core.security import get_password_hash, verify_password, create_access_token
from app.core.limiter import limiter
from app.models.user import User, UserRole
from app.schemas.user import UserRegister, UserResponse
from app.schemas.auth import UserLogin, LoginResponse
from app.schemas.common import ResponseModel
from app.utils.email import send_verification_email, generate_verification_token, get_token_expiry
from app.utils.logger import logger
from app.utils import generate_captcha, verify_captcha
from app.schemas.captcha import CaptchaResponse
router = APIRouter(prefix="/auth", tags=["认证"])


@router.post("/register", response_model=ResponseModel[UserResponse])
@limiter.limit("3/minute")
async def register(
    request: Request,
    user_data: UserRegister,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    logger.info(f"用户注册请求: email={user_data.email}, name={user_data.name}")
     # 验证验证码
    if not verify_captcha(user_data.captcha_id, user_data.captcha_text):
        raise HTTPException(status_code=400, detail="验证码错误或已过期")
    
    existing = db.query(User).filter(User.email == user_data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="邮箱已被注册")
    
    verification_token = generate_verification_token()
    
    db_user = User(
        name=user_data.name,
        email=user_data.email,
        hashed_password=get_password_hash(user_data.password),
        role=UserRole.USER,
        is_verified=False,
        verification_token=verification_token,
        token_expires_at=get_token_expiry(hours=24)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    background_tasks.add_task(
        send_verification_email,
        email=db_user.email,
        name=db_user.name,
        token=verification_token
    )
    
    logger.info(f"用户注册成功: user_id={db_user.id}, email={db_user.email}")
    return ResponseModel.success(data=db_user, message="注册成功！请查收邮件并点击链接验证邮箱。")


@router.get("/verify")
def verify_email(token: str = Query(...), db: Session = Depends(get_db)):
    logger.info(f"邮箱验证请求: token={token[:10]}...")
    
    user = db.query(User).filter(User.verification_token == token).first()
    if not user:
        raise HTTPException(status_code=400, detail="无效的验证链接")
    if user.is_verified:
        return ResponseModel.success(message="邮箱已验证，无需重复验证")
    if user.token_expires_at < datetime.now():
        raise HTTPException(status_code=400, detail="验证链接已过期，请重新注册")
    
    user.is_verified = True
    user.verification_token = None
    user.token_expires_at = None
    db.commit()
    
    logger.info(f"邮箱验证成功: user_id={user.id}, email={user.email}")
    return ResponseModel.success(message="邮箱验证成功！现在可以登录了。")


@router.post("/login", response_model=ResponseModel[LoginResponse])
@limiter.limit("5/minute")
def login(
    request: Request,
    user_data: UserLogin,
    db: Session = Depends(get_db)
):
    logger.info(f"用户登录尝试: email={user_data.email}")
    
    user = db.query(User).filter(User.email == user_data.email).first()
    if not user:
        raise HTTPException(status_code=401, detail="邮箱或密码错误")
    if not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="邮箱或密码错误")
    if not user.is_verified:
        raise HTTPException(status_code=403, detail="邮箱未验证，请查收邮件并点击验证链接")
    
    access_token = create_access_token(
        data={"sub": str(user.id), "role": user.role.value},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    logger.info(f"用户登录成功: user_id={user.id}, email={user.email}, role={user.role.value}")
    
    login_response = LoginResponse(
        access_token=access_token,
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=UserResponse.model_validate(user)
    )
    
    return ResponseModel.success(data=login_response, message="登录成功")


@router.post("/resend-verification", response_model=ResponseModel)
async def resend_verification(
    email: str = Query(...),
    background_tasks: BackgroundTasks = None,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    if user.is_verified:
        return ResponseModel.success(message="邮箱已验证，无需重发")
    
    user.verification_token = generate_verification_token()
    user.token_expires_at = get_token_expiry(hours=24)
    db.commit()
    
    background_tasks.add_task(
        send_verification_email,
        email=user.email,
        name=user.name,
        token=user.verification_token
    )
    
    return ResponseModel.success(message="验证邮件已重新发送，请查收")

@router.get("/captcha", response_model=ResponseModel[CaptchaResponse])
async def get_captcha():
    """获取图形验证码"""
    captcha_id, captcha_text, captcha_image = generate_captcha()
    logger.debug(f"生成验证码: id={captcha_id}, text={captcha_text}")
    
    return ResponseModel.success(
        data=CaptchaResponse(captcha_id=captcha_id, captcha_image=captcha_image),
        message="验证码获取成功"
    )