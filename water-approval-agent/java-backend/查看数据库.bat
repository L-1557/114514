@echo off
chcp 65001 >nul
echo ========================================
echo 数据库表结构查看工具
echo ========================================
echo.

echo 请在浏览器中打开以下地址：
echo.
echo H2 数据库控制台：http://localhost:8080/h2-console
echo.
echo 登录信息：
echo   JDBC URL: jdbc:h2:mem:waterdb
echo   用户名：sa
echo   密码：（留空）
echo.
echo ========================================
echo 常用 SQL 查询：
echo ========================================
echo.
echo 1. 查看所有表：
echo    SHOW TABLES;
echo.
echo 2. 查看申请表结构：
echo    DESCRIBE applications;
echo.
echo 3. 查看文件表结构：
echo    DESCRIBE files;
echo.
echo 4. 查看所有申请：
echo    SELECT * FROM applications ORDER BY submitted_at DESC;
echo.
echo 5. 查看所有文件：
echo    SELECT * FROM files ORDER BY upload_time DESC;
echo.
echo 6. 查看申请统计：
echo    SELECT status, COUNT(*) as count FROM applications GROUP BY status;
echo.
echo 7. 查看文件统计：
echo    SELECT COUNT(*) as total_files, SUM(file_size) as total_size FROM files WHERE is_deleted = false;
echo.
echo ========================================
pause
