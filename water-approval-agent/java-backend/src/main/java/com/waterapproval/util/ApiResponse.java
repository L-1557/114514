package com.waterapproval.util;

import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

/**
 * 统一 API 响应封装
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
public class ApiResponse<T> {
    
    /**
     * 响应状态
     */
    private String status;
    
    /**
     * 响应消息
     */
    private String message;
    
    /**
     * 响应数据
     */
    private T data;
    
    /**
     * 时间戳
     */
    private long timestamp;
    
    /**
     * 成功响应（带数据）
     */
    public static <T> ApiResponse<T> success(T data) {
        ApiResponse<T> response = new ApiResponse<>();
        response.setStatus("success");
        response.setMessage("操作成功");
        response.setData(data);
        response.setTimestamp(System.currentTimeMillis());
        return response;
    }
    
    /**
     * 成功响应（带消息和数据）
     */
    public static <T> ApiResponse<T> success(String message, T data) {
        ApiResponse<T> response = new ApiResponse<>();
        response.setStatus("success");
        response.setMessage(message);
        response.setData(data);
        response.setTimestamp(System.currentTimeMillis());
        return response;
    }
    
    /**
     * 错误响应
     */
    public static <T> ApiResponse<T> error(String message) {
        ApiResponse<T> response = new ApiResponse<>();
        response.setStatus("error");
        response.setMessage(message);
        response.setTimestamp(System.currentTimeMillis());
        return response;
    }
    
    /**
     * 错误响应（带数据）
     */
    public static <T> ApiResponse<T> error(String message, T data) {
        ApiResponse<T> response = new ApiResponse<>();
        response.setStatus("error");
        response.setMessage(message);
        response.setData(data);
        response.setTimestamp(System.currentTimeMillis());
        return response;
    }
}
