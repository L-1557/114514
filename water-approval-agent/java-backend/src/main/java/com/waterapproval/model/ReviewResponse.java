package com.waterapproval.model;

import lombok.Data;
import java.util.List;
import java.util.Map;

@Data
public class ReviewResponse {
    private String status;
    private Map<String, Object> results;
    private List<Map<String, Object>> issues;
    private List<String> recommendations;
    
    // 兼容字段
    private Boolean approved;
    private String remarks;
}
