from pydantic import BaseModel

class CaptchaResponse(BaseModel):
    captcha_id: str
    captcha_image: str  # base64 图片
