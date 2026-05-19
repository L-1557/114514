package com.waterapproval.repository;

import com.waterapproval.model.entity.FileEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

/**
 * 文件数据访问接口
 */
@Repository
public interface FileRepository extends JpaRepository<FileEntity, Long> {
    
    /**
     * 根据文件名查找
     */
    Optional<FileEntity> findByFileName(String fileName);
    
    /**
     * 根据申请 ID 查找文件列表
     */
    List<FileEntity> findByApplicationIdOrderByUploadTimeDesc(Long applicationId);
    
    /**
     * 根据申请 ID 查找所有未删除的文件
     */
    List<FileEntity> findByApplicationIdAndIsDeletedFalseOrderByUploadTimeDesc(Long applicationId);
    
    /**
     * 统计申请的文件数量
     */
    long countByApplicationId(Long applicationId);
    
    /**
     * 查找所有未删除的文件
     */
    List<FileEntity> findByIsDeletedFalseOrderByUploadTimeDesc();
    
    /**
     * 统计文件总数
     */
    long countByIsDeletedFalse();
    
    /**
     * 统计文件总大小
     */
    @Query("SELECT SUM(f.fileSize) FROM FileEntity f WHERE f.isDeleted = false")
    Long sumFileSizeByIsDeletedFalse();
}
