package com.waterapproval.controller;

import com.waterapproval.model.ReviewRequest;
import com.waterapproval.model.ReviewResponse;
import com.waterapproval.service.ReviewService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import reactor.core.publisher.Mono;

@RestController
@RequestMapping("/api")
@CrossOrigin(origins = "*")
public class ReviewController {

    @Autowired
    private ReviewService reviewService;

    @PostMapping("/review")
    public Mono<ResponseEntity<ReviewResponse>> reviewApplication(@RequestBody ReviewRequest request) {
        return reviewService.submitReview(request)
                .map(ResponseEntity::ok)
                .onErrorResume(e -> {
                    System.err.println("AI 审查失败：" + e.getMessage());
                    e.printStackTrace();
                    
                    ReviewResponse errorResponse = new ReviewResponse();
                    errorResponse.setStatus("error");
                    errorResponse.setApproved(false);
                    errorResponse.setRemarks("AI 审查失败：" + e.getMessage());
                    
                    return Mono.just(
                        ResponseEntity.status(500).body(errorResponse)
                    );
                });
    }

    @PostMapping("/review/stable")
    public Mono<ResponseEntity<ReviewResponse>> reviewApplicationStable(@RequestBody ReviewRequest request) {
        return reviewService.submitStableReview(request)
                .map(ResponseEntity::ok)
                .onErrorResume(e -> {
                    System.err.println("稳定性审查失败：" + e.getMessage());
                    e.printStackTrace();
                    
                    ReviewResponse errorResponse = new ReviewResponse();
                    errorResponse.setStatus("error");
                    errorResponse.setApproved(false);
                    errorResponse.setRemarks("稳定性审查失败：" + e.getMessage());
                    
                    return Mono.just(
                        ResponseEntity.status(500).body(errorResponse)
                    );
                });
    }

    @GetMapping("/health")
    public ResponseEntity<String> healthCheck() {
        return ResponseEntity.ok("Java backend is healthy");
    }
}
