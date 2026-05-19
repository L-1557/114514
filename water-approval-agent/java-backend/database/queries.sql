-- ============================================================
-- 常用 SQL 查询语句集合
-- 涉水审批材料合规性审查系统
-- ============================================================

-- ============================================================
-- 一、申请相关查询
-- ============================================================

-- 1.1 查看所有申请（按提交时间倒序）
SELECT 
    id,
    application_number,
    project_name,
    applicant_name,
    water_source,
    water_purpose,
    water_volume,
    status,
    submitted_at,
    reviewed_at
FROM applications
ORDER BY submitted_at DESC;

-- 1.2 查看待审查的申请
SELECT 
    id,
    application_number,
    project_name,
    applicant_name,
    water_source,
    water_purpose,
    water_volume,
    submitted_at
FROM applications
WHERE status = 'pending'
ORDER BY submitted_at DESC;

-- 1.3 查看审查中的申请
SELECT 
    id,
    application_number,
    project_name,
    applicant_name,
    status,
    reviewed_at
FROM applications
WHERE status = 'reviewing'
ORDER BY reviewed_at DESC;

-- 1.4 查看已通过的申请
SELECT 
    id,
    application_number,
    project_name,
    applicant_name,
    water_volume,
    reviewed_at
FROM applications
WHERE status = 'approved'
ORDER BY reviewed_at DESC;

-- 1.5 查看已拒绝的申请
SELECT 
    id,
    application_number,
    project_name,
    applicant_name,
    status,
    reviewed_at
FROM applications
WHERE status = 'rejected'
ORDER BY reviewed_at DESC;

-- 1.6 按项目名称模糊查询
SELECT * 
FROM applications
WHERE project_name LIKE '%关键词%'
ORDER BY submitted_at DESC;

-- 1.7 按申请人查询
SELECT * 
FROM applications
WHERE applicant_name LIKE '%申请人姓名%'
ORDER BY submitted_at DESC;

-- 1.8 查看申请详情（包括文件数量）
SELECT 
    a.*,
    COUNT(f.id) as file_count,
    SUM(f.file_size) as total_file_size
FROM applications a
LEFT JOIN files f ON a.id = f.application_id AND f.is_deleted = FALSE
WHERE a.id = 1
GROUP BY a.id;

-- ============================================================
-- 二、统计查询
-- ============================================================

-- 2.1 按状态统计申请数量
SELECT 
    status,
    COUNT(*) as count,
    SUM(water_volume) as total_water_volume
FROM applications
GROUP BY status;

-- 2.2 统计总申请数和总取水量
SELECT 
    COUNT(*) as total_applications,
    SUM(water_volume) as total_water_volume,
    AVG(water_volume) as avg_water_volume
FROM applications;

-- 2.3 统计各取水用途的数量
SELECT 
    water_purpose,
    COUNT(*) as count,
    SUM(water_volume) as total_volume
FROM applications
GROUP BY water_purpose
ORDER BY count DESC;

-- 2.4 统计各水源的使用情况
SELECT 
    water_source,
    COUNT(*) as count,
    SUM(water_volume) as total_volume,
    AVG(water_volume) as avg_volume
FROM applications
GROUP BY water_source
ORDER BY total_volume DESC;

-- 2.5 按月统计申请数量（最近 12 个月）
SELECT 
    DATE_FORMAT(submitted_at, '%Y-%m') as month,
    COUNT(*) as count
FROM applications
WHERE submitted_at >= DATE_SUB(NOW(), INTERVAL 12 MONTH)
GROUP BY DATE_FORMAT(submitted_at, '%Y-%m')
ORDER BY month;

-- ============================================================
-- 三、文件相关查询
-- ============================================================

-- 3.1 查看某个申请的所有文件
SELECT 
    id,
    original_name,
    content_type,
    file_size,
    file_size / 1024 as size_kb,
    upload_time,
    download_count
FROM files
WHERE application_id = 1 AND is_deleted = FALSE
ORDER BY upload_time DESC;

-- 3.2 查看所有文件（按上传时间倒序）
SELECT 
    f.id,
    f.original_name,
    f.content_type,
    f.file_size,
    f.upload_time,
    f.download_count,
    a.project_name,
    a.applicant_name
FROM files f
LEFT JOIN applications a ON f.application_id = a.id
WHERE f.is_deleted = FALSE
ORDER BY f.upload_time DESC;

-- 3.3 统计文件总数和总大小
SELECT 
    COUNT(*) as total_files,
    SUM(file_size) as total_bytes,
    SUM(file_size) / 1024 as total_kb,
    SUM(file_size) / 1024 / 1024 as total_mb
FROM files
WHERE is_deleted = FALSE;

-- 3.4 查看下载次数最多的文件
SELECT 
    f.original_name,
    f.download_count,
    a.project_name,
    f.upload_time
FROM files f
LEFT JOIN applications a ON f.application_id = a.id
WHERE f.is_deleted = FALSE
ORDER BY f.download_count DESC
LIMIT 10;

-- 3.5 查看未关联申请的文件（孤立文件）
SELECT * 
FROM files
WHERE application_id IS NULL AND is_deleted = FALSE;

-- ============================================================
-- 四、用户相关查询
-- ============================================================

-- 4.1 查看所有用户
SELECT 
    id,
    username,
    real_name,
    email,
    phone,
    role,
    department,
    status,
    last_login_time,
    created_at
FROM users
ORDER BY created_at DESC;

-- 4.2 查看管理员用户
SELECT * 
FROM users
WHERE role = 'admin';

-- 4.3 查看审查员用户
SELECT * 
FROM users
WHERE role = 'reviewer';

-- 4.4 统计各角色用户数量
SELECT 
    role,
    COUNT(*) as count
FROM users
GROUP BY role;

-- 4.5 查看活跃用户（最近 30 天登录过）
SELECT * 
FROM users
WHERE last_login_time >= DATE_SUB(NOW(), INTERVAL 30 DAY)
AND status = 'active';

-- ============================================================
-- 五、审查日志查询
-- ============================================================

-- 5.1 查看某个申请的审查日志
SELECT 
    l.id,
    l.action,
    l.old_status,
    l.new_status,
    l.remark,
    l.created_at,
    u.real_name as reviewer_name
FROM review_logs l
LEFT JOIN users u ON l.reviewer_id = u.id
WHERE l.application_id = 1
ORDER BY l.created_at DESC;

-- 5.2 查看所有审查操作（最近 100 条）
SELECT 
    l.id,
    a.project_name,
    l.action,
    l.old_status,
    l.new_status,
    l.remark,
    l.created_at,
    u.real_name as reviewer_name
FROM review_logs l
LEFT JOIN applications a ON l.application_id = a.id
LEFT JOIN users u ON l.reviewer_id = u.id
ORDER BY l.created_at DESC
LIMIT 100;

-- 5.3 统计审查员的审查数量
SELECT 
    u.real_name,
    COUNT(l.id) as review_count
FROM review_logs l
LEFT JOIN users u ON l.reviewer_id = u.id
WHERE l.action = 'review'
GROUP BY u.id, u.real_name
ORDER BY review_count DESC;

-- ============================================================
-- 六、高级查询
-- ============================================================

-- 6.1 申请详情（包含所有关联信息）
SELECT 
    a.id,
    a.application_number,
    a.project_name,
    a.applicant_name,
    a.water_source,
    a.water_purpose,
    a.application_period,
    a.water_volume,
    a.status,
    a.submitted_at,
    a.reviewed_at,
    a.project_description,
    COUNT(DISTINCT f.id) as file_count,
    SUM(f.file_size) as total_file_size,
    u.real_name as creator_name
FROM applications a
LEFT JOIN files f ON a.id = f.application_id AND f.is_deleted = FALSE
LEFT JOIN users u ON a.applicant_name = u.real_name
WHERE a.id = 1
GROUP BY a.id;

-- 6.2 查找相似项目（相同水源和用途）
SELECT 
    id,
    project_name,
    applicant_name,
    water_source,
    water_purpose,
    water_volume,
    status
FROM applications
WHERE water_source = '黄河' 
  AND water_purpose = '工业用水'
  AND id != 1
ORDER BY submitted_at DESC;

-- 6.3 申请审批时长统计
SELECT 
    id,
    project_name,
    submitted_at,
    reviewed_at,
    TIMESTAMPDIFF(HOUR, submitted_at, reviewed_at) as review_hours
FROM applications
WHERE status IN ('approved', 'rejected')
  AND reviewed_at IS NOT NULL
ORDER BY review_hours DESC;

-- 6.4 查找大型取水项目（年取水量超过 50000 立方米）
SELECT 
    id,
    project_name,
    applicant_name,
    water_source,
    water_volume,
    status,
    submitted_at
FROM applications
WHERE water_volume > 50000
ORDER BY water_volume DESC;

-- ============================================================
-- 七、数据维护查询
-- ============================================================

-- 7.1 查看孤立的文件（没有关联申请）
SELECT * 
FROM files
WHERE application_id IS NULL 
  AND is_deleted = FALSE
  AND upload_time < DATE_SUB(NOW(), INTERVAL 7 DAY);

-- 7.2 查看长期未审查的申请
SELECT * 
FROM applications
WHERE status = 'pending'
  AND submitted_at < DATE_SUB(NOW(), INTERVAL 30 DAY)
ORDER BY submitted_at;

-- 7.3 清理已删除标记的文件（物理删除）
-- DELETE FROM files WHERE is_deleted = TRUE;

-- 7.4 更新申请状态
-- UPDATE applications SET status = 'reviewing' WHERE id = 1;

-- 7.5 重置用户密码
-- UPDATE users SET password = '新密码哈希' WHERE username = 'admin';

-- ============================================================
-- 八、性能分析查询
-- ============================================================

-- 8.1 查看表大小
SELECT 
    TABLE_NAME,
    TABLE_ROWS,
    ROUND((DATA_LENGTH + INDEX_LENGTH) / 1024 / 1024, 2) AS 'Size(MB)'
FROM information_schema.TABLES
WHERE TABLE_SCHEMA = DATABASE()
ORDER BY TABLE_ROWS DESC;

-- 8.2 查看索引使用情况
SHOW INDEX FROM applications;
SHOW INDEX FROM files;

-- 8.3 分析查询性能（使用 EXPLAIN）
EXPLAIN SELECT * FROM applications WHERE status = 'pending';
EXPLAIN SELECT * FROM files WHERE application_id = 1;

-- ============================================================
-- 结束
-- ============================================================
