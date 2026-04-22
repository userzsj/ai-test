import base64
import secrets
import uuid
from datetime import datetime, timedelta
from captcha.image import ImageCaptcha
from app.core.config import settings

# 内存存储验证码（生产环境建议用 Redis）
_captcha_store = {}

# 验证码配置
CAPTCHA_EXPIRE_SECONDS = 300  # 5 分钟
CAPTCHA_WIDTH = 160
CAPTCHA_HEIGHT = 60
CAPTCHA_LENGTH = 4  # 验证码字符数量


def generate_captcha() -> tuple[str, str, str]:
    # \"\"\"
    # 生成验证码
    # 返回: (captcha_id, captcha_text, captcha_image_base64)
    # \"\"\"
    # 生成随机验证码文本（数字+字母）
    chars = '23456789ABCDEFGHJKLMNPQRSTUVWXYZ'  # 去掉容易混淆的字符 0,1,O,I
    captcha_text = ''.join(secrets.choice(chars) for _ in range(CAPTCHA_LENGTH))
    
    # 生成验证码图片
    image = ImageCaptcha(width=CAPTCHA_WIDTH, height=CAPTCHA_HEIGHT)
    image_data = image.generate(captcha_text)
    
    # 转换为 base64
    image_base64 = base64.b64encode(image_data.getvalue()).decode('utf-8')
    
    # 生成唯一 ID
    captcha_id = str(uuid.uuid4())
    
    # 存入内存
    _captcha_store[captcha_id] = {
        'text': captcha_text,
        'expire_at': datetime.now() + timedelta(seconds=CAPTCHA_EXPIRE_SECONDS),
        'used': False
    }
    
    return captcha_id, captcha_text, f'data:image/png;base64,{image_base64}'


def verify_captcha(captcha_id: str, captcha_text: str) -> bool:
    # \"\"\"
    # 验证验证码
    # \"\"\"
    if captcha_id not in _captcha_store:
        return False
    
    record = _captcha_store[captcha_id]
    
    # 检查是否已使用
    if record['used']:
        return False
    
    # 检查是否过期
    if datetime.now() > record['expire_at']:
        del _captcha_store[captcha_id]
        return False
    
    # 验证（不区分大小写）
    if record['text'].upper() != captcha_text.upper():
        return False
    
    # 标记为已使用
    record['used'] = True
    return True


def clean_expired_captcha():
    # \"\"\"清理过期的验证码（可定期调用）\"\"\"
    now = datetime.now()
    expired_ids = [cid for cid, record in _captcha_store.items() if now > record['expire_at']]
    for cid in expired_ids:
        del _captcha_store[cid]
