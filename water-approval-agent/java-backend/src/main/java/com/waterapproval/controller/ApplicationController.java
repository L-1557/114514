package com.waterapproval.controller;

import com.waterapproval.model.entity.Application;
import com.waterapproval.service.ApplicationService;
import com.waterapproval.util.ApiResponse;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * 申请管理控制器
 */
@RestController
@RequestMapping("/api/applications")
@CrossOrigin(origins = "*")
public class ApplicationController {
    
    @Autowired
    private ApplicationService applicationService;
    
    /**
     * 获取所有申请
     */
    @GetMapping
    public ResponseEntity<ApiResponse<List<Application>>> getAllApplications() {
        List<Application> applications = applicationService.getAllApplications();
        return ResponseEntity.ok(ApiResponse.success(applications));
    }
    
    /**
     * 根据 ID 获取申请
     */
    @GetMapping("/{id}")
    public ResponseEntity<ApiResponse<Application>> getApplicationById(@PathVariable Long id) {
        return applicationService.getApplicationById(id)
            .map(app -> ResponseEntity.ok(ApiResponse.success(app)))
            .orElse(ResponseEntity.notFound().build());
    }
    
    /**
     * 创建申请
     */
    @PostMapping
    public ResponseEntity<ApiResponse<Application>> createApplication(@RequestBody Application application) {
        Application created = applicationService.createApplication(application);
        return ResponseEntity.ok(ApiResponse.success(created));
    }
    
    /**
     * 更新申请
     */
    @PutMapping("/{id}")
    public ResponseEntity<ApiResponse<Application>> updateApplication(
            @PathVariable Long id,
            @RequestBody Application application) {
        try {
            Application updated = applicationService.updateApplication(id, application);
            return ResponseEntity.ok(ApiResponse.success(updated));
        } catch (RuntimeException e) {
            return ResponseEntity.notFound().build();
        }
    }
    
    /**
     * 删除申请
     */
    @DeleteMapping("/{id}")
    public ResponseEntity<ApiResponse<Void>> deleteApplication(@PathVariable Long id) {
        applicationService.deleteApplication(id);
        return ResponseEntity.ok(ApiResponse.success(null));
    }
    
    /**
     * 审查申请
     */
    @PostMapping("/{id}/review")
    public ResponseEntity<ApiResponse<Application>> reviewApplication(
            @PathVariable Long id,
            @RequestBody Map<String, String> reviewData) {
        try {
            String reviewResult = reviewData.get("reviewResult");
            Application reviewed = applicationService.reviewApplication(id, reviewResult);
            return ResponseEntity.ok(ApiResponse.success(reviewed));
        } catch (RuntimeException e) {
            return ResponseEntity.notFound().build();
        }
    }
    
    /**
     * 更新申请状态
     */
    @PatchMapping("/{id}/status")
    public ResponseEntity<ApiResponse<Application>> updateStatus(
            @PathVariable Long id,
            @RequestBody Map<String, String> statusData) {
        try {
            String status = statusData.get("status");
            Application updated = applicationService.updateStatus(id, status);
            return ResponseEntity.ok(ApiResponse.success(updated));
        } catch (RuntimeException e) {
            return ResponseEntity.notFound().build();
        }
    }
    
    /**
     * 搜索申请
     */
    @GetMapping("/search")
    public ResponseEntity<ApiResponse<List<Application>>> searchApplications(
            @RequestParam String keyword) {
        List<Application> applications = applicationService.searchApplications(keyword);
        return ResponseEntity.ok(ApiResponse.success(applications));
    }
    
    /**
     * 获取待审查申请列表
     */
    @GetMapping("/pending")
    public ResponseEntity<ApiResponse<List<Application>>> getPendingApplications() {
        List<Application> applications = applicationService.getPendingApplications();
        return ResponseEntity.ok(ApiResponse.success(applications));
    }
    
    /**
     * 获取统计信息
     */
    @GetMapping("/statistics")
    public ResponseEntity<ApiResponse<Map<String, Object>>> getStatistics() {
        ApplicationService.ApplicationStatistics stats = applicationService.getStatistics();
        
        Map<String, Object> result = new HashMap<>();
        result.put("total", stats.getTotal());
        result.put("pending", stats.getPending());
        result.put("reviewing", stats.getReviewing());
        result.put("approved", stats.getApproved());
        result.put("rejected", stats.getRejected());
        
        return ResponseEntity.ok(ApiResponse.success(result));
    }
}
