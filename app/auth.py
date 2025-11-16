from fastapi import Depends, HTTPException, status, Request, Response
from fastapi.responses import RedirectResponse
from passlib.context import CryptContext
from itsdangerous import URLSafeTimedSerializer, BadSignature
import os
import secrets

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")

# Session序列化器
serializer = URLSafeTimedSerializer(SECRET_KEY)

def create_session(username: str) -> str:
    """创建Session Token"""
    return serializer.dumps(username, salt="admin-session")

def verify_session(token: str) -> str:
    """验证Session Token"""
    try:
        username = serializer.loads(token, salt="admin-session", max_age=86400)  # 24小时有效
        return username
    except BadSignature:
        return None

def verify_admin(request: Request):
    """验证管理员身份（从Cookie获取Session）"""
    session_token = request.cookies.get("admin_session")
    
    if not session_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="未登录"
        )
    
    username = verify_session(session_token)
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session已过期，请重新登录"
        )
    
    return username

def check_credentials(username: str, password: str) -> bool:
    """验证用户名密码"""
    correct_username = secrets.compare_digest(username, ADMIN_USERNAME)
    correct_password = secrets.compare_digest(password, ADMIN_PASSWORD)
    return correct_username and correct_password

def get_api_key(request: Request) -> str:
    """从请求头获取API密钥"""
    api_key = request.headers.get("X-API-Key")
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="缺少API密钥"
        )
    return api_key
