package com.waterapproval.model.entity;

import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.util.List;

/**
 * 涉水审批申请实体类
 */
@Entity
@Table(name = "applications")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class Application {
    
    /**
     * 主键 ID
     */
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    /**
     * 申请编号
     */
    @Column(name = "application_number", unique = true, nullable = false)
    private String applicationNumber;
    
    /**
     * 项目名称
     */
    @Column(name = "project_name", nullable = false, length = 200)
    private String projectName;
    
    /**
     * 申请人/单位名称
     */
    @Column(name = "applicant_name", nullable = false, length = 200)
    private String applicantName;
    
    /**
     * 取水水源
     */
    @Column(name = "water_source", nullable = false, length = 200)
    private String waterSource;
    
    /**
     * 取水用途
     */
    @Column(name = "water_purpose", nullable = false, length = 50)
    private String waterPurpose;
    
    /**
     * 申请期限
     */
    @Column(name = "application_period", nullable = false, length = 100)
    private String applicationPeriod;
    
    /**
     * 年取水量（立方米）
     */
    @Column(name = "water_volume", nullable = false)
    private Integer waterVolume;
    
    /**
     * 项目简介
     */
    @Column(name = "project_description", columnDefinition = "TEXT")
    private String projectDescription;
    
    /**
     * 文档类型列表（JSON 格式存储）
     */
    @Column(name = "documents", columnDefinition = "TEXT")
    private String documents;
    
    /**
     * 上传文件列表（JSON 格式存储）
     */
    @Column(name = "files", columnDefinition = "TEXT")
    private String files;
    
    /**
     * 申请状态：pending, reviewing, approved, rejected
     */
    @Column(name = "status", nullable = false, length = 20)
    private String status = "pending";
    
    /**
     * 审查结果（JSON 格式存储）
     */
    @Column(name = "review_result", columnDefinition = "TEXT")
    private String reviewResult;
    
    /**
     * 提交时间
     */
    @Column(name = "submitted_at")
    private LocalDateTime submittedAt;
    
    /**
     * 审查时间
     */
    @Column(name = "reviewed_at")
    private LocalDateTime reviewedAt;
    
    /**
     * 创建时间
     */
    @Column(name = "created_at", updatable = false)
    private LocalDateTime createdAt;
    
    /**
     * 更新时间
     */
    @Column(name = "updated_at")
    private LocalDateTime updatedAt;
    
    /**
     * 实体创建前回调
     */
    @PrePersist
    protected void onCreate() {
        createdAt = LocalDateTime.now();
        updatedAt = LocalDateTime.now();
        if (submittedAt == null) {
            submittedAt = LocalDateTime.now();
        }
    }
    
    /**
     * 实体更新前回调
     */
    @PreUpdate
    protected void onUpdate() {
        updatedAt = LocalDateTime.now();
    }
    
    /**
     * 生成申请编号
     */
    public void generateApplicationNumber() {
        this.applicationNumber = "APP" + String.format("%08d", System.currentTimeMillis() % 100000000);
    }
}
