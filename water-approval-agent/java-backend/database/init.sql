
-- 设置客户端编码
SET MODE MySQL;

-- ============================================================
-- 1. 创建申请表 (applications)
-- ============================================================
CREATE TABLE IF NOT EXISTS applications (
    id BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '主键 ID',
    application_number VARCHAR(50) UNIQUE NOT NULL COMMENT '申请编号',
    project_name VARCHAR(200) NOT NULL COMMENT '项目名称',
    applicant_name VARCHAR(200) NOT NULL COMMENT '申请人/单位名称',
    water_source VARCHAR(200) NOT NULL COMMENT '取水水源',
    water_purpose VARCHAR(50) NOT NULL COMMENT '取水用途',
    application_period VARCHAR(100) NOT NULL COMMENT '申请期限',
    water_volume INT NOT NULL COMMENT '年取水量（立方米）',
    project_description TEXT COMMENT '项目简介',
    documents TEXT COMMENT '文档类型列表（JSON 格式）',
    files TEXT COMMENT '上传文件列表（JSON 格式）',
    status VARCHAR(20) NOT NULL DEFAULT 'pending' COMMENT '申请状态：pending-待审查，reviewing-审查中，approved-已通过，rejected-已拒绝',
    review_result TEXT COMMENT '审查结果（JSON 格式）',
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '提交时间',
    reviewed_at TIMESTAMP COMMENT '审查时间',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间'
) COMMENT '涉水审批申请表';

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_app_status ON applications(status);
CREATE INDEX IF NOT EXISTS idx_app_submitted_at ON applications(submitted_at DESC);
CREATE INDEX IF NOT EXISTS idx_app_project_name ON applications(project_name);
CREATE INDEX IF NOT EXISTS idx_app_applicant ON applications(applicant_name);

-- ============================================================
-- 2. 创建文件表 (files)
-- ============================================================
CREATE TABLE IF NOT EXISTS files (
    id BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '主键 ID',
    file_name VARCHAR(255) NOT NULL COMMENT '文件名称（UUID 生成）',
    original_name VARCHAR(255) NOT NULL COMMENT '原始文件名',
    content_type VARCHAR(100) NOT NULL COMMENT '文件类型（MIME Type）',
    file_size BIGINT NOT NULL COMMENT '文件大小（字节）',
    file_path VARCHAR(500) NOT NULL COMMENT '文件存储路径',
    application_id BIGINT COMMENT '关联的申请 ID',
    description VARCHAR(500) COMMENT '文件描述',
    upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '上传时间',
    upload_ip VARCHAR(50) COMMENT '上传 IP 地址',
    download_count INT DEFAULT 0 COMMENT '下载次数',
    is_deleted BOOLEAN DEFAULT FALSE COMMENT '删除标记：0-未删除，1-已删除',
    FOREIGN KEY (application_id) REFERENCES applications(id) ON DELETE SET NULL
) COMMENT '上传文件信息表';

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_file_application_id ON files(application_id);
CREATE INDEX IF NOT EXISTS idx_file_name ON files(file_name);
CREATE INDEX IF NOT EXISTS idx_file_upload_time ON files(upload_time DESC);
CREATE INDEX IF NOT EXISTS idx_file_deleted ON files(is_deleted);

-- ============================================================
-- 3. 创建用户表（预留）
-- ============================================================
CREATE TABLE IF NOT EXISTS users (
    id BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '用户 ID',
    username VARCHAR(50) UNIQUE NOT NULL COMMENT '用户名',
    password VARCHAR(255) NOT NULL COMMENT '密码（加密）',
    real_name VARCHAR(100) COMMENT '真实姓名',
    email VARCHAR(100) COMMENT '邮箱',
    phone VARCHAR(20) COMMENT '手机号',
    role VARCHAR(20) DEFAULT 'user' COMMENT '角色：admin-管理员，reviewer-审查员，user-普通用户',
    department VARCHAR(100) COMMENT '所属部门',
    status VARCHAR(20) DEFAULT 'active' COMMENT '状态：active-启用，inactive-禁用',
    last_login_time TIMESTAMP COMMENT '最后登录时间',
    last_login_ip VARCHAR(50) COMMENT '最后登录 IP',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间'
) COMMENT '用户信息表';

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_user_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_user_role ON users(role);
CREATE INDEX IF NOT EXISTS idx_user_status ON users(status);

-- ============================================================
-- 4. 创建审查日志表（预留）
-- ============================================================
CREATE TABLE IF NOT EXISTS review_logs (
    id BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '日志 ID',
    application_id BIGINT NOT NULL COMMENT '申请 ID',
    reviewer_id BIGINT COMMENT '审查员 ID',
    action VARCHAR(50) NOT NULL COMMENT '操作：create-创建，review-审查，update-更新，delete-删除',
    old_status VARCHAR(20) COMMENT '原状态',
    new_status VARCHAR(20) COMMENT '新状态',
    remark TEXT COMMENT '备注',
    review_result TEXT COMMENT '审查结果（JSON）',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    FOREIGN KEY (application_id) REFERENCES applications(id) ON DELETE CASCADE,
    FOREIGN KEY (reviewer_id) REFERENCES users(id) ON DELETE SET NULL
) COMMENT '审查日志表';

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_log_application_id ON review_logs(application_id);
CREATE INDEX IF NOT EXISTS idx_log_reviewer_id ON review_logs(reviewer_id);
CREATE INDEX IF NOT EXISTS idx_log_created_at ON review_logs(created_at DESC);

-- ============================================================
-- 5. 插入测试数据
-- ============================================================

-- 插入测试用户
INSERT INTO users (username, password, real_name, email, phone, role, department, status) 
VALUES 
('admin', '$2a$10$N.zmdr9k7uOCQb376NoUnuTJ8iKTm8AiVU5sZ0S1Q5J5J5J5J5J5J', '系统管理员', 'admin@waterapproval.com', '13800138000', 'admin', '管理部门', 'active'),
('reviewer1', '$2a$10$N.zmdr9k7uOCQb376NoUnuTJ8iKTm8AiVU5sZ0S1Q5J5J5J5J5J5J', '张审查', 'reviewer1@waterapproval.com', '13800138001', 'reviewer', '审查部门', 'active'),
('user1', '$2a$10$N.zmdr9k7uOCQb376NoUnuTJ8iKTm8AiVU5sZ0S1Q5J5J5J5J5J5J', '李申请', 'user1@example.com', '13800138002', 'user', '申请单位', 'active');

-- 插入测试申请
INSERT INTO applications (application_number, project_name, applicant_name, water_source, water_purpose, application_period, water_volume, project_description, documents, files, status, submitted_at) 
VALUES 
('APP00000001', '工业园区供水项目', '某某工业园区管委会', '黄河', '工业用水', '2024-01-01 至 2029-12-31', 50000, '本项目为工业园区提供生产用水，服务面积 10 平方公里，预计服务人口 5 万人。', '["application_form", "business_license", "water_resource_report"]', '["file1.pdf", "file2.pdf"]', 'approved', '2024-01-15 10:30:00'),
('APP00000002', '农业灌溉取水许可', '某某农业合作社', '地下水', '农业灌溉', '2024-03-01 至 2025-02-28', 20000, '用于农田灌溉，灌溉面积 500 亩，主要种植小麦和玉米。', '["application_form", "id_card", "land_proof"]', '["file3.pdf"]', 'reviewing', '2024-02-20 14:20:00'),
('APP00000003', '生活饮用水取水申请', '某某自来水公司', '长江', '生活用水', '2024-01-01 至 2034-12-31', 100000, '为城区居民提供生活饮用水，服务人口 20 万人，日供水能力 5 万吨。', '["application_form", "business_license", "water_resource_report", "commitment_letter"]', '["file4.pdf", "file5.pdf", "file6.pdf"]', 'pending', '2024-03-10 09:15:00');

-- 插入测试文件
INSERT INTO files (file_name, original_name, content_type, file_size, file_path, application_id, description, upload_ip, download_count) 
VALUES 
('abc123def456.pdf', '申请表.pdf', 'application/pdf', 102400, 'uploads/abc123def456.pdf', 1, '项目申请表', '127.0.0.1', 5),
('ghi789jkl012.pdf', '营业执照.pdf', 'application/pdf', 204800, 'uploads/ghi789jkl012.pdf', 1, '营业执照扫描件', '127.0.0.1', 3),
('mno345pqr678.pdf', '水资源论证报告.pdf', 'application/pdf', 512000, 'uploads/mno345pqr678.pdf', 1, '水资源论证报告全文', '127.0.0.1', 2);

-- ============================================================
-- 6. 创建视图（可选）
-- ============================================================

-- 申请统计视图
CREATE OR REPLACE VIEW v_application_statistics AS
SELECT 
    status,
    COUNT(*) as count,
    SUM(water_volume) as total_water_volume
FROM applications
WHERE is_deleted = FALSE
GROUP BY status;

-- 文件统计视图
CREATE OR REPLACE VIEW v_file_statistics AS
SELECT 
    COUNT(*) as total_files,
    SUM(file_size) as total_size,
    SUM(download_count) as total_downloads
FROM files
WHERE is_deleted = FALSE;

-- 申请详情视图
CREATE OR REPLACE VIEW v_application_detail AS
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
    COUNT(f.id) as file_count,
    SUM(f.file_size) as total_file_size
FROM applications a
LEFT JOIN files f ON a.id = f.application_id AND f.is_deleted = FALSE
WHERE a.is_deleted = FALSE
GROUP BY a.id, a.application_number, a.project_name, a.applicant_name, 
         a.water_source, a.water_purpose, a.application_period, 
         a.water_volume, a.status, a.submitted_at, a.reviewed_at;

-- ============================================================
-- 7. 常用查询示例
-- ============================================================

-- 查询所有申请
-- SELECT * FROM applications ORDER BY submitted_at DESC;

-- 查询待审查的申请
-- SELECT * FROM applications WHERE status = 'pending' ORDER BY submitted_at DESC;

-- 查询某个申请的所有文件
-- SELECT * FROM files WHERE application_id = 1 AND is_deleted = FALSE;

-- 查询申请及其文件数量
-- SELECT a.*, COUNT(f.id) as file_count 
-- FROM applications a 
-- LEFT JOIN files f ON a.id = f.application_id 
-- GROUP BY a.id 
-- ORDER BY a.submitted_at DESC;

-- 统计各状态申请数量
-- SELECT status, COUNT(*) as count FROM applications GROUP BY status;

-- 统计文件总大小
-- SELECT SUM(file_size) / 1024 / 1024 as total_mb FROM files WHERE is_deleted = FALSE;

-- ============================================================
-- 脚本结束
-- ============================================================
