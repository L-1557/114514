package com.waterapproval.service;

import com.waterapproval.model.entity.FileEntity;
import com.waterapproval.repository.FileRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import jakarta.servlet.http.HttpServletRequest;
import java.io.IOException;
import java.nio.file.*;
import java.time.LocalDateTime;
import java.util.*;

/**
 * 文件服务类
 */
@Service
public class FileService {
    
    @Autowired
    private FileRepository fileRepository;
    
    @Autowired
    private HttpServletRequest request;
    
    // 上传目录
    private static final String UPLOAD_DIR = "uploads/";
    
    // 允许的文件类型
    private static final List<String> ALLOWED_CONTENT_TYPES = Arrays.asList(
        "application/pdf",
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "image/jpeg",
        "image/png",
        "image/jpg"
    );
    
    // 最大文件大小：10MB
    private static final long MAX_FILE_SIZE = 10 * 1024 * 1024;
    
    /**
     * 上传文件
     */
    public Map<String, Object> uploadFile(MultipartFile file, Long applicationId) throws IOException {
        // 验证文件
        validateFile(file);
        
        // 生成唯一文件名
        String fileName = generateFileName(file.getOriginalFilename());
        
        // 创建上传目录
        Path uploadPath = Paths.get(UPLOAD_DIR);
        if (!Files.exists(uploadPath)) {
            Files.createDirectories(uploadPath);
        }
        
        // 保存文件
        Path filePath = uploadPath.resolve(fileName);
        Files.copy(file.getInputStream(), filePath, StandardCopyOption.REPLACE_EXISTING);
        
        // 创建文件实体
        FileEntity fileEntity = new FileEntity();
        fileEntity.setFileName(fileName);
        fileEntity.setOriginalName(file.getOriginalFilename());
        fileEntity.setContentType(file.getContentType());
        fileEntity.setFileSize(file.getSize());
        fileEntity.setFilePath(filePath.toString());
        fileEntity.setApplicationId(applicationId);
        fileEntity.setUploadTime(LocalDateTime.now());
        fileEntity.setUploadIp(getClientIp());
        fileEntity.setDownloadCount(0);
        fileEntity.setIsDeleted(false);
        
        // 保存到数据库
        fileRepository.save(fileEntity);
        
        // 返回文件信息
        Map<String, Object> fileInfo = new HashMap<>();
        fileInfo.put("id", fileEntity.getId());
        fileInfo.put("fileName", fileName);
        fileInfo.put("originalName", file.getOriginalFilename());
        fileInfo.put("contentType", file.getContentType());
        fileInfo.put("size", file.getSize());
        fileInfo.put("sizeFormatted", formatFileSize(file.getSize()));
        fileInfo.put("uploadTime", fileEntity.getUploadTime().toString());
        fileInfo.put("downloadUrl", "/api/files/" + fileName);
        
        return fileInfo;
    }
    
    /**
     * 批量上传文件
     */
    public List<Map<String, Object>> uploadFiles(MultipartFile[] files, Long applicationId) throws IOException {
        List<Map<String, Object>> fileInfos = new ArrayList<>();
        
        for (MultipartFile file : files) {
            if (!file.isEmpty()) {
                fileInfos.add(uploadFile(file, applicationId));
            }
        }
        
        return fileInfos;
    }
    
    /**
     * 获取文件信息
     */
    public Optional<FileEntity> getFileById(Long id) {
        return fileRepository.findById(id);
    }
    
    /**
     * 获取文件信息（根据文件名）
     */
    public Optional<FileEntity> getFileByFileName(String fileName) {
        return fileRepository.findByFileName(fileName);
    }
    
    /**
     * 获取申请的所有文件
     */
    public List<FileEntity> getFilesByApplicationId(Long applicationId) {
        return fileRepository.findByApplicationIdAndIsDeletedFalseOrderByUploadTimeDesc(applicationId);
    }
    
    /**
     * 删除文件
     */
    public boolean deleteFile(Long id) throws IOException {
        Optional<FileEntity> fileOpt = fileRepository.findById(id);
        if (fileOpt.isPresent()) {
            FileEntity fileEntity = fileOpt.get();
            
            // 物理删除文件
            Path filePath = Paths.get(fileEntity.getFilePath());
            if (Files.exists(filePath)) {
                Files.delete(filePath);
            }
            
            // 逻辑删除数据库记录
            fileEntity.setIsDeleted(true);
            fileRepository.save(fileEntity);
            
            return true;
        }
        return false;
    }
    
    /**
     * 增加下载次数
     */
    public void incrementDownloadCount(Long id) {
        fileRepository.findById(id).ifPresent(fileEntity -> {
            fileEntity.setDownloadCount(fileEntity.getDownloadCount() + 1);
            fileRepository.save(fileEntity);
        });
    }
    
    /**
     * 验证文件
     */
    private void validateFile(MultipartFile file) {
        // 检查文件是否为空
        if (file.isEmpty()) {
            throw new RuntimeException("文件不能为空");
        }
        
        // 检查文件大小
        if (file.getSize() > MAX_FILE_SIZE) {
            throw new RuntimeException("文件大小不能超过 10MB");
        }
        
        // 检查文件类型
        String contentType = file.getContentType();
        if (contentType == null || !ALLOWED_CONTENT_TYPES.contains(contentType.toLowerCase())) {
            throw new RuntimeException("不支持的文件类型：" + contentType);
        }
        
        // 检查文件名
        String originalName = file.getOriginalFilename();
        if (originalName == null || originalName.trim().isEmpty()) {
            throw new RuntimeException("文件名不能为空");
        }
        
        // 安全检查：防止路径遍历攻击
        if (originalName.contains("..") || originalName.contains("/") || originalName.contains("\\")) {
            throw new RuntimeException("非法的文件名");
        }
    }
    
    /**
     * 生成唯一文件名
     */
    private String generateFileName(String originalName) {
        String uuid = UUID.randomUUID().toString().replace("-", "");
        String extension = "";
        
        int lastDotIndex = originalName.lastIndexOf(".");
        if (lastDotIndex > 0) {
            extension = originalName.substring(lastDotIndex);
        }
        
        return uuid + extension;
    }
    
    /**
     * 格式化文件大小
     */
    private String formatFileSize(long size) {
        if (size < 1024) {
            return size + " B";
        } else if (size < 1024 * 1024) {
            return String.format("%.2f KB", size / 1024.0);
        } else if (size < 1024 * 1024 * 1024) {
            return String.format("%.2f MB", size / (1024.0 * 1024.0));
        } else {
            return String.format("%.2f GB", size / (1024.0 * 1024.0 * 1024.0));
        }
    }
    
    /**
     * 获取客户端 IP
     */
    private String getClientIp() {
        String xfHeader = request.getHeader("X-Forwarded-For");
        if (xfHeader != null) {
            return xfHeader.split(",")[0];
        }
        return request.getRemoteAddr();
    }
    
    /**
     * 获取上传目录
     */
    public String getUploadDir() {
        return UPLOAD_DIR;
    }
}
