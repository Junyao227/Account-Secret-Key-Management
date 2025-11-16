from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from sqlalchemy import inspect, text
from dotenv import load_dotenv

# 从 .env 文件加载环境变量（如果存在）
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/windsurf_pool")

# SQLite 需要特殊配置
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """初始化数据库表"""
    Base.metadata.create_all(bind=engine)
    # 轻量迁移：确保 keys 表存在必要的列
    try:
        inspector = inspect(engine)
        columns = [col['name'] for col in inspector.get_columns('keys')]
        
        # 迁移 account_limit 列
        if 'account_limit' not in columns:
            with engine.begin() as conn:
                if engine.dialect.name == 'sqlite':
                    conn.execute(text("ALTER TABLE keys ADD COLUMN account_limit INTEGER NOT NULL DEFAULT 0"))
                else:
                    conn.execute(text("ALTER TABLE keys ADD COLUMN IF NOT EXISTS account_limit INTEGER NOT NULL DEFAULT 0"))
            print("✅ 已添加 account_limit 列")
        
        # 迁移 key_type 列
        if 'key_type' not in columns:
            with engine.begin() as conn:
                if engine.dialect.name == 'sqlite':
                    conn.execute(text("ALTER TABLE keys ADD COLUMN key_type VARCHAR NOT NULL DEFAULT 'limited'"))
                else:
                    conn.execute(text("ALTER TABLE keys ADD COLUMN IF NOT EXISTS key_type VARCHAR NOT NULL DEFAULT 'limited'"))
            print("✅ 已添加 key_type 列")
            
    except Exception as e:
        # 打印但不阻断启动
        print(f"⚠️ 数据库轻量迁移失败: {e}")
