package com.waterapproval.repository;

import com.waterapproval.model.entity.Application;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

/**
 * 申请数据访问接口
 */
@Repository
public interface ApplicationRepository extends JpaRepository<Application, Long> {
    
    /**
     * 根据申请编号查找
     */
    Optional<Application> findByApplicationNumber(String applicationNumber);
    
    /**
     * 获取所有申请，按提交时间降序
     */
    List<Application> findAllByOrderBySubmittedAtDesc();
    
    /**
     * 根据状态查找申请列表
     */
    List<Application> findByStatusOrderBySubmittedAtDesc(String status);
    
    /**
     * 根据项目名称模糊查询
     */
    @Query("SELECT a FROM Application a WHERE a.projectName LIKE %:keyword% ORDER BY a.submittedAt DESC")
    List<Application> searchByProjectName(@Param("keyword") String keyword);
    
    /**
     * 统计各状态申请数量
     */
    @Query("SELECT a.status, COUNT(a) FROM Application a GROUP BY a.status")
    List<Object[]> countByStatus();
    
    /**
     * 统计总申请数
     */
    long count();
    
    /**
     * 统计待审查数量
     */
    long countByStatus(String status);
}
