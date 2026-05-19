package com.waterapproval.model;

import lombok.Data;
import java.util.List;
import java.util.Map;

@Data
public class ReviewRequest {
    private Map<String, Object> applicationData;
    private List<String> documents;
    private String checkType = "full";
}
