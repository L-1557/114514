package com.waterapproval.controller;

import com.waterapproval.model.entity.FileEntity;
import com.waterapproval.service.FileService;
import com.waterapproval.util.ApiResponse;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.Resource;
import org.springframework.core.io.UrlResource;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.net.MalformedURLException;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * 文件上传控制器
 */
@RestController
@RequestMapping("/api/files")
@CrossOrigin(origins = "*")
public class FileUploadController {
    
    @Autowired
    private FileService fileService;
    
    /**
     * 上传单个文件
     */
    @PostMapping("/upload")
    public ResponseEntity<ApiResponse<Map<String, Object>>> uploadFile(
            @RequestParam("file") MultipartFile file,
            @RequestParam(value = "applicationId", required = false) Long applicationId) {
        
        try {
            Map<String, Object> fileInfo = fileService.uploadFile(file, applicationId);
            return ResponseEntity.ok(ApiResponse.success("上传成功", fileInfo));
        } catch (IOException e) {
            return ResponseEntity.badRequest()
                .body(ApiResponse.error("文件上传失败：" + e.getMessage()));
        } catch (RuntimeException e) {
            return ResponseEntity.badRequest()
                .body(ApiResponse.error(e.getMessage()));
        }
    }
    
    /**
     * 上传多个文件
     */
    @PostMapping("/uploads")
    public ResponseEntity<ApiResponse<List<Map<String, Object>>>> uploadFiles(
            @RequestParam("files") MultipartFile[] files,
            @RequestParam(value = "applicationId", required = false) Long applicationId) {
        
        try {
            List<Map<String, Object>> fileInfos = fileService.uploadFiles(files, applicationId);
            return ResponseEntity.ok(ApiResponse.success("上传成功", fileInfos));
        } catch (IOException e) {
            return ResponseEntity.badRequest()
                .body(ApiResponse.error("文件上传失败：" + e.getMessage()));
        } catch (RuntimeException e) {
            return ResponseEntity.badRequest()
                .body(ApiResponse.error(e.getMessage()));
        }
    }
    
    /**
     * 下载文件
     */
    @GetMapping("/{fileName}")
    public ResponseEntity<Resource> downloadFile(@PathVariable String fileName) {
        try {
            // 获取文件信息
            FileEntity fileEntity = fileService.getFileByFileName(fileName)
                .orElseThrow(() -> new RuntimeException("文件不存在"));
            
            // 增加下载次数
            fileService.incrementDownloadCount(fileEntity.getId());
            
            // 创建文件资源
            Path filePath = Paths.get(fileEntity.getFilePath());
            Resource resource = new UrlResource(filePath.toUri());
            
            if (resource.exists()) {
                return ResponseEntity.ok()
                    .contentType(MediaType.parseMediaType(fileEntity.getContentType()))
                    .header(HttpHeaders.CONTENT_DISPOSITION, 
                        "attachment; filename=\"" + fileEntity.getOriginalName() + "\"")
                    .header(HttpHeaders.CONTENT_LENGTH, String.valueOf(fileEntity.getFileSize()))
                    .body(resource);
            } else {
                return ResponseEntity.notFound().build();
            }
        } catch (MalformedURLException e) {
            return ResponseEntity.status(500).build();
        } catch (RuntimeException e) {
            return ResponseEntity.notFound().build();
        }
    }
    
    /**
     * 预览文件（直接在浏览器打开）
     */
    @GetMapping("/preview/{fileName}")
    public ResponseEntity<Resource> previewFile(@PathVariable String fileName) {
        try {
            // 获取文件信息
            FileEntity fileEntity = fileService.getFileByFileName(fileName)
                .orElseThrow(() -> new RuntimeException("文件不存在"));
            
            // 创建文件资源
            Path filePath = Paths.get(fileEntity.getFilePath());
            Resource resource = new UrlResource(filePath.toUri());
            
            if (resource.exists()) {
                return ResponseEntity.ok()
                    .contentType(MediaType.parseMediaType(fileEntity.getContentType()))
                    .header(HttpHeaders.CONTENT_DISPOSITION, 
                        "inline; filename=\"" + fileEntity.getOriginalName() + "\"")
                    .body(resource);
            } else {
                return ResponseEntity.notFound().build();
            }
        } catch (MalformedURLException e) {
            return ResponseEntity.status(500).build();
        } catch (RuntimeException e) {
            return ResponseEntity.notFound().build();
        }
    }
    
    /**
     * 获取文件列表（根据申请 ID）
     */
    @GetMapping("/application/{applicationId}")
    public ResponseEntity<ApiResponse<List<FileEntity>>> getFilesByApplicationId(
            @PathVariable Long applicationId) {
        List<FileEntity> files = fileService.getFilesByApplicationId(applicationId);
        return ResponseEntity.ok(ApiResponse.success(files));
    }
    
    /**
     * 获取文件信息
     */
    @GetMapping("/info/{id}")
    public ResponseEntity<ApiResponse<FileEntity>> getFileById(@PathVariable Long id) {
        return fileService.getFileById(id)
            .map(file -> ResponseEntity.ok(ApiResponse.success(file)))
            .orElse(ResponseEntity.notFound().build());
    }
    
    /**
     * 删除文件
     */
    @DeleteMapping("/{id}")
    public ResponseEntity<ApiResponse<Void>> deleteFile(@PathVariable Long id) {
        try {
            boolean deleted = fileService.deleteFile(id);
            if (deleted) {
                return ResponseEntity.ok(ApiResponse.success("删除成功", null));
            } else {
                return ResponseEntity.notFound().build();
            }
        } catch (IOException e) {
            return ResponseEntity.status(500)
                .body(ApiResponse.error("删除失败：" + e.getMessage()));
        }
    }
    
    /**
     * 获取所有文件
     */
    @GetMapping("/all")
    public ResponseEntity<ApiResponse<List<FileEntity>>> getAllFiles() {
        List<FileEntity> files = fileService.getFilesByApplicationId(null);
        return ResponseEntity.ok(ApiResponse.success(files));
    }
}
