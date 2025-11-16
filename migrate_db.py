"""
数据库迁移脚本
为现有数据库添加新字段：
- keys 表添加 is_disabled, daily_request_count, last_reset_date
"""

import sqlite3
import os
from datetime import datetime

DB_PATH = 'windsurf_pool.db'

def migrate():
    if not os.path.exists(DB_PATH):
        print(f"❌ 数据库文件不存在: {DB_PATH}")
        return
    
    print(f"🔄 开始迁移数据库: {DB_PATH}")
    
    # 创建备份
    backup_path = f"{DB_PATH}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    import shutil
    shutil.copy2(DB_PATH, backup_path)
    print(f"✅ 已创建备份: {backup_path}")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # 检查并添加 is_disabled 字段
        cursor.execute("PRAGMA table_info(keys)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'is_disabled' not in columns:
            print("📝 添加 is_disabled 字段...")
            cursor.execute("""
                ALTER TABLE keys ADD COLUMN is_disabled BOOLEAN NOT NULL DEFAULT 0
            """)
            print("✅ is_disabled 字段已添加")
        else:
            print("ℹ️ is_disabled 字段已存在，跳过")
        
        # 检查并添加 daily_request_count 字段
        if 'daily_request_count' not in columns:
            print("📝 添加 daily_request_count 字段...")
            cursor.execute("""
                ALTER TABLE keys ADD COLUMN daily_request_count INTEGER NOT NULL DEFAULT 0
            """)
            print("✅ daily_request_count 字段已添加")
        else:
            print("ℹ️ daily_request_count 字段已存在，跳过")
        
        # 检查并添加 last_reset_date 字段
        if 'last_reset_date' not in columns:
            print("📝 添加 last_reset_date 字段...")
            cursor.execute("""
                ALTER TABLE keys ADD COLUMN last_reset_date DATE
            """)
            print("✅ last_reset_date 字段已添加")
        else:
            print("ℹ️ last_reset_date 字段已存在，跳过")
        
        conn.commit()
        print("\n🎉 数据库迁移完成！")
        
        # 显示更新后的表结构
        print("\n📊 更新后的 keys 表结构:")
        cursor.execute("PRAGMA table_info(keys)")
        for col in cursor.fetchall():
            print(f"   {col[1]:25s} {col[2]:15s} {'NOT NULL' if col[3] else ''} {f'DEFAULT {col[4]}' if col[4] else ''}")
        
    except Exception as e:
        print(f"\n❌ 迁移失败: {e}")
        conn.rollback()
        print(f"💡 可以从备份恢复: {backup_path}")
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()
