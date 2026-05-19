# 数据库 SQL 文件说明

## 📁 文件列表

### 1️⃣ [init.sql](file://c:\Users\吕浩宇\Desktop\新建文件夹\water-approval-agent\java-backend\database\init.sql) - 数据库初始化脚本
**用途**：创建数据库表结构、插入测试数据

**包含内容**：
- ✅ 创建申请表 (applications)
- ✅ 创建文件表 (files)
- ✅ 创建用户表 (users) - 预留
- ✅ 创建审查日志表 (review_logs) - 预留
- ✅ 创建索引
- ✅ 创建视图
- ✅ 插入测试数据

**使用方法**：
```bash
# H2 控制台
1. 打开 http://localhost:8080/h2-console
2. 登录后
3. 复制 init.sql 内容
4. 粘贴到 SQL 输入框
5. 点击"Run"执行
```

---

### 2️⃣ [queries.sql](file://c:\Users\吕浩宇\Desktop\新建文件夹\water-approval-agent\java-backend\database\queries.sql) - 常用查询语句集合
**用途**：提供日常开发和维护中常用的 SQL 查询

**包含内容**：
- 📊 申请相关查询（7 个）
- 📈 统计查询（5 个）
- 📁 文件相关查询（5 个）
- 👤 用户相关查询（5 个）
- 📝 审查日志查询（3 个）
- 🔍 高级查询（4 个）
- 🛠️ 数据维护查询（5 个）
- ⚡ 性能分析查询（3 个）

**使用方法**：
```bash
# 需要查询时
1. 打开 queries.sql
2. 找到对应的查询
3. 复制到 H2 控制台
4. 修改参数（如 ID、关键词等）
5. 执行查询
```

---

## 🗂️ 数据库表结构

### 表 1：applications（申请表）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | BIGINT | 主键 ID（自增） |
| application_number | VARCHAR(50) | 申请编号（唯一） |
| project_name | VARCHAR(200) | 项目名称 |
| applicant_name | VARCHAR(200) | 申请人/单位 |
| water_source | VARCHAR(200) | 取水水源 |
| water_purpose | VARCHAR(50) | 取水用途 |
| application_period | VARCHAR(100) | 申请期限 |
| water_volume | INT | 年取水量（m³） |
| project_description | TEXT | 项目简介 |
| documents | TEXT | 文档列表（JSON） |
| files | TEXT | 文件列表（JSON） |
| status | VARCHAR(20) | 状态 |
| review_result | TEXT | 审查结果（JSON） |
| submitted_at | TIMESTAMP | 提交时间 |
| reviewed_at | TIMESTAMP | 审查时间 |
| created_at | TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | 更新时间 |

### 表 2：files（文件表）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | BIGINT | 主键 ID（自增） |
| file_name | VARCHAR(255) | 文件名（UUID） |
| original_name | VARCHAR(255) | 原始文件名 |
| content_type | VARCHAR(100) | MIME 类型 |
| file_size | BIGINT | 文件大小（字节） |
| file_path | VARCHAR(500) | 存储路径 |
| application_id | BIGINT | 关联申请 ID |
| description | VARCHAR(500) | 文件描述 |
| upload_time | TIMESTAMP | 上传时间 |
| upload_ip | VARCHAR(50) | 上传 IP |
| download_count | INT | 下载次数 |
| is_deleted | BOOLEAN | 删除标记 |

### 表 3：users（用户表）- 预留

| 字段 | 类型 | 说明 |
|------|------|------|
| id | BIGINT | 用户 ID |
| username | VARCHAR(50) | 用户名（唯一） |
| password | VARCHAR(255) | 密码（加密） |
| real_name | VARCHAR(100) | 真实姓名 |
| email | VARCHAR(100) | 邮箱 |
| phone | VARCHAR(20) | 手机号 |
| role | VARCHAR(20) | 角色（admin/reviewer/user） |
| department | VARCHAR(100) | 部门 |
| status | VARCHAR(20) | 状态 |
| last_login_time | TIMESTAMP | 最后登录时间 |
| last_login_ip | VARCHAR(50) | 最后登录 IP |
| created_at | TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | 更新时间 |

### 表 4：review_logs（审查日志表）- 预留

| 字段 | 类型 | 说明 |
|------|------|------|
| id | BIGINT | 日志 ID |
| application_id | BIGINT | 申请 ID |
| reviewer_id | BIGINT | 审查员 ID |
| action | VARCHAR(50) | 操作类型 |
| old_status | VARCHAR(20) | 原状态 |
| new_status | VARCHAR(20) | 新状态 |
| remark | TEXT | 备注 |
| review_result | TEXT | 审查结果（JSON） |
| created_at | TIMESTAMP | 创建时间 |

---

## 🚀 快速使用

### 方法 1：H2 控制台（推荐）

1. **启动 Java 后端**
   ```
   运行 WaterApprovalApplication.java
   ```

2. **打开 H2 控制台**
   ```
   浏览器访问：http://localhost:8080/h2-console
   ```

3. **登录信息**
   ```
   JDBC URL: jdbc:h2:mem:waterdb
   用户名：sa
   密码：（留空）
   ```

4. **执行 SQL**
   - 打开 init.sql 或 queries.sql
   - 复制需要的 SQL 语句
   - 粘贴到控制台
   - 点击"Run"

### 方法 2：前端页面

1. 访问：http://localhost:8080
2. 点击"数据库"标签
3. 查看统计信息
4. 点击"打开 H2 控制台"

### 方法 3：API 接口

```bash
# 查看统计信息
curl http://localhost:8080/api/applications/statistics

# 查看所有申请
curl http://localhost:8080/api/applications

# 查看所有文件
curl http://localhost:8080/api/files/all
```

---

## 📋 常用 SQL 速查

### 查看所有表
```sql
SHOW TABLES;
```

### 查看表结构
```sql
DESCRIBE applications;
DESCRIBE files;
DESCRIBE users;
DESCRIBE review_logs;
```

### 查看所有申请
```sql
SELECT * FROM applications ORDER BY submitted_at DESC;
```

### 查看待审查申请
```sql
SELECT * FROM applications WHERE status = 'pending' ORDER BY submitted_at DESC;
```

### 查看某个申请的文件
```sql
SELECT * FROM files WHERE application_id = 1 AND is_deleted = FALSE;
```

### 统计各状态申请数量
```sql
SELECT status, COUNT(*) as count FROM applications GROUP BY status;
```

### 统计文件总数和大小
```sql
SELECT 
    COUNT(*) as total_files,
    SUM(file_size) / 1024 / 1024 as total_mb
FROM files 
WHERE is_deleted = FALSE;
```

---

## 🎯 测试数据

init.sql 中已包含以下测试数据：

### 测试用户（3 个）
- admin（系统管理员）
- reviewer1（审查员）
- user1（普通用户）

### 测试申请（3 个）
1. **工业园区供水项目** - 已批准
2. **农业灌溉取水许可** - 审查中
3. **生活饮用水取水申请** - 待审查

### 测试文件（3 个）
- 申请表.pdf
- 营业执照.pdf
- 水资源论证报告.pdf

---

## 📊 视图说明

### v_application_statistics
申请统计视图，按状态分组统计数量和取水量。

### v_file_statistics
文件统计视图，统计文件总数、总大小、总下载次数。

### v_application_detail
申请详情视图，包含申请基本信息和文件统计。

---

## ⚠️ 注意事项

### 1. H2 内存数据库特性
- ⚠️ **重启后数据丢失**：内存数据库在应用重启后数据会清空
- ✅ **解决方案**：如需持久化，修改 application.properties 使用文件数据库

### 2. 切换到文件数据库
修改 application.properties：
```properties
# 使用文件数据库（重启后数据保留）
spring.datasource.url=jdbc:h2:file:./waterdb
```

### 3. 切换到 MySQL
修改 application.properties：
```properties
# 使用 MySQL
spring.datasource.url=jdbc:mysql://localhost:3306/water_approval
spring.datasource.driverClassName=com.mysql.cj.jdbc.Driver
spring.datasource.username=root
spring.datasource.password=your_password
```

### 4. 外键约束
- files.application_id 关联 applications.id
- 删除申请时，关联文件设置为 NULL
- review_logs.application_id 级联删除

---

## 📝 索引说明

### applications 表索引
- idx_app_status：状态索引
- idx_app_submitted_at：提交时间索引
- idx_app_project_name：项目名称索引
- idx_app_applicant：申请人索引

### files 表索引
- idx_file_application_id：申请 ID 索引
- idx_file_name：文件名索引
- idx_file_upload_time：上传时间索引
- idx_file_deleted：删除标记索引

### users 表索引
- idx_user_username：用户名索引
- idx_user_role：角色索引
- idx_user_status：状态索引

### review_logs 表索引
- idx_log_application_id：申请 ID 索引
- idx_log_reviewer_id：审查员 ID 索引
- idx_log_created_at：创建时间索引

---

## 🔧 数据库维护

### 清理已删除的文件
```sql
DELETE FROM files WHERE is_deleted = TRUE;
```

### 清理长期未审查的申请
```sql
-- 先查看
SELECT * FROM applications 
WHERE status = 'pending' 
  AND submitted_at < DATE_SUB(NOW(), INTERVAL 30 DAY);

-- 确认后可以更新状态或删除
```

### 备份数据库
```bash
# H2 文件数据库备份
复制 waterdb.mv.db 文件到备份目录
```

### 导入 SQL 文件
```bash
# 命令行方式
java -cp h2*.jar org.h2.tools.RunScript -url jdbc:h2:mem:waterdb -user sa -script init.sql
```

---

## 📖 相关文档

- [application.properties](file://c:\Users\吕浩宇\Desktop\新建文件夹\water-approval-agent\java-backend\src\main\resources\application.properties) - 数据库配置
- [Application.java](file://c:\Users\吕浩宇\Desktop\新建文件夹\water-approval-agent\java-backend\src\main\java\com\waterapproval\model\entity\Application.java) - 申请表实体
- [FileEntity.java](file://c:\Users\吕浩宇\Desktop\新建文件夹\water-approval-agent\java-backend\src\main\java\com\waterapproval\model\entity\FileEntity.java) - 文件表实体
- [查看数据库.bat](file://c:\Users\吕浩宇\Desktop\新建文件夹\water-approval-agent\java-backend\查看数据库.bat) - 快速查看工具

---

## 🎉 总结

现在您拥有了完整的 SQL 文件：

✅ **init.sql** - 创建表结构、插入测试数据  
✅ **queries.sql** - 37 个常用查询语句  
✅ **README.md** - 详细的使用说明文档  

**文件位置**：
```
java-backend/database/
├── init.sql          (表结构定义 + 测试数据)
├── queries.sql       (常用查询集合)
└── README.md         (使用说明)
```

**快速开始**：
1. 启动 Java 后端
2. 打开 H2 控制台
3. 执行 init.sql 创建表结构
4. 使用 queries.sql 进行查询

查看完整文档：[database/README.md](file://c:\Users\吕浩宇\Desktop\新建文件夹\water-approval-agent\java-backend\database\README.md)
