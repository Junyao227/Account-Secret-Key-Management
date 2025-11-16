"""
本地运行脚本
使用 SQLite 数据库，无需 Docker
"""
import os
import sys

# 加载本地环境变量
from dotenv import load_dotenv
load_dotenv('.env.local')

# 设置 SQLite 数据库 URL
os.environ['DATABASE_URL'] = 'sqlite:///./windsurf_pool.db'

if __name__ == "__main__":
    import uvicorn
    
    print("=" * 60)
    print("🚀 启动本地开发服务器")
    print("=" * 60)
    print(f"📊 数据库: SQLite (windsurf_pool.db)")
    print(f"🌐 地址: http://localhost:8000")
    print(f"📖 API文档: http://localhost:8000/docs")
    print(f"🔐 管理后台: http://localhost:8000/admin")
    print(f"👤 管理员账号: admin / admin123")
    print("=" * 60)
    print()
    
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )
