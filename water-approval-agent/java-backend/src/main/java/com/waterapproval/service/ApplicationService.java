package com.waterapproval.service;

import com.waterapproval.model.entity.Application;
import com.waterapproval.repository.ApplicationRepository;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

/**
 * 申请服务类
 */
@Service
@Transactional
public class ApplicationService {
    
    @Autowired
    private ApplicationRepository applicationRepository;
    
    @Autowired
    private ObjectMapper objectMapper;
    
    /**
     * 创建申请
     */
    public Application createApplication(Application application) {
        application.generateApplicationNumber();
        return applicationRepository.save(application);
    }
    
    /**
     * 获取所有申请
     */
    @Transactional(readOnly = true)
    public List<Application> getAllApplications() {
        return applicationRepository.findAllByOrderBySubmittedAtDesc();
    }
    
    /**
     * 根据 ID 获取申请
     */
    @Transactional(readOnly = true)
    public Optional<Application> getApplicationById(Long id) {
        return applicationRepository.findById(id);
    }
    
    /**
     * 根据编号获取申请
     */
    @Transactional(readOnly = true)
    public Optional<Application> getApplicationByNumber(String applicationNumber) {
        return applicationRepository.findByApplicationNumber(applicationNumber);
    }
    
    /**
     * 更新申请
     */
    public Application updateApplication(Long id, Application application) {
        Application existingApp = applicationRepository.findById(id)
            .orElseThrow(() -> new RuntimeException("申请不存在"));
        
        // 更新字段
        existingApp.setProjectName(application.getProjectName());
        existingApp.setApplicantName(application.getApplicantName());
        existingApp.setWaterSource(application.getWaterSource());
        existingApp.setWaterPurpose(application.getWaterPurpose());
        existingApp.setApplicationPeriod(application.getApplicationPeriod());
        existingApp.setWaterVolume(application.getWaterVolume());
        existingApp.setProjectDescription(application.getProjectDescription());
        existingApp.setDocuments(application.getDocuments());
        existingApp.setFiles(application.getFiles());
        
        return applicationRepository.save(existingApp);
    }
    
    /**
     * 删除申请
     */
    public void deleteApplication(Long id) {
        applicationRepository.deleteById(id);
    }
    
    /**
     * 审查申请
     */
    public Application reviewApplication(Long id, String reviewResult) {
        Application application = applicationRepository.findById(id)
            .orElseThrow(() -> new RuntimeException("申请不存在"));
        
        application.setReviewResult(reviewResult);
        application.setReviewedAt(LocalDateTime.now());
        
        // 根据审查结果设置状态
        try {
            var reviewData = objectMapper.readTree(reviewResult);
            var results = reviewData.get("results");
            if (results != null) {
                int criticalIssues = results.get("critical_issues").asInt(0);
                application.setStatus(criticalIssues == 0 ? "approved" : "rejected");
            }
        } catch (JsonProcessingException e) {
            application.setStatus("rejected");
        }
        
        return applicationRepository.save(application);
    }
    
    /**
     * 更新申请状态
     */
    public Application updateStatus(Long id, String status) {
        Application application = applicationRepository.findById(id)
            .orElseThrow(() -> new RuntimeException("申请不存在"));
        
        application.setStatus(status);
        return applicationRepository.save(application);
    }
    
    /**
     * 搜索申请
     */
    @Transactional(readOnly = true)
    public List<Application> searchApplications(String keyword) {
        return applicationRepository.searchByProjectName(keyword);
    }
    
    /**
     * 获取待审查申请列表
     */
    @Transactional(readOnly = true)
    public List<Application> getPendingApplications() {
        return applicationRepository.findByStatusOrderBySubmittedAtDesc("pending");
    }
    
    /**
     * 统计各状态申请数量
     */
    @Transactional(readOnly = true)
    public ApplicationStatistics getStatistics() {
        List<Object[]> results = applicationRepository.countByStatus();
        
        ApplicationStatistics stats = new ApplicationStatistics();
        stats.setTotal(applicationRepository.count());
        
        for (Object[] result : results) {
            String status = (String) result[0];
            Long count = (Long) result[1];
            
            switch (status) {
                case "pending" -> stats.setPending(count);
                case "reviewing" -> stats.setReviewing(count);
                case "approved" -> stats.setApproved(count);
                case "rejected" -> stats.setRejected(count);
            }
        }
        
        return stats;
    }
    
    /**
     * 申请统计内部类
     */
    public static class ApplicationStatistics {
        private long total;
        private long pending;
        private long reviewing;
        private long approved;
        private long rejected;
        
        // Getters and Setters
        public long getTotal() { return total; }
        public void setTotal(long total) { this.total = total; }
        public long getPending() { return pending; }
        public void setPending(long pending) { this.pending = pending; }
        public long getReviewing() { return reviewing; }
        public void setReviewing(long reviewing) { this.reviewing = reviewing; }
        public long getApproved() { return approved; }
        public void setApproved(long approved) { this.approved = approved; }
        public long getRejected() { return rejected; }
        public void setRejected(long rejected) { this.rejected = rejected; }
    }
}
