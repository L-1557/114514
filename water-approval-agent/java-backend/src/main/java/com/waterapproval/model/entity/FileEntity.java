package com.waterapproval.model.entity;

import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;

/**
 * 文件实体类
 */
@Entity
@Table(name = "files")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class FileEntity {
    
    /**
     * 主键 ID
     */
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    /**
     * 文件名称（UUID 生成）
     */
    @Column(name = "file_name", nullable = false, length = 255)
    private String fileName;
    
    /**
     * 原始文件名
     */
    @Column(name = "original_name", nullable = false, length = 255)
    private String originalName;
    
    /**
     * 文件类型（MIME Type）
     */
    @Column(name = "content_type", nullable = false, length = 100)
    private String contentType;
    
    /**
     * 文件大小（字节）
     */
    @Column(name = "file_size", nullable = false)
    private Long fileSize;
    
    /**
     * 文件路径
     */
    @Column(name = "file_path", nullable = false, length = 500)
    private String filePath;
    
    /**
     * 关联的申请 ID
     */
    @Column(name = "application_id")
    private Long applicationId;
    
    /**
     * 文件描述
     */
    @Column(name = "description", length = 500)
    private String description;
    
    /**
     * 上传时间
     */
    @Column(name = "upload_time", nullable = false)
    private LocalDateTime uploadTime;
    
    /**
     * 上传 IP
     */
    @Column(name = "upload_ip", length = 50)
    private String uploadIp;
    
    /**
     * 下载次数
     */
    @Column(name = "download_count")
    private Integer downloadCount = 0;
    
    /**
     * 是否删除标记
     */
    @Column(name = "is_deleted")
    private Boolean isDeleted = false;
}
