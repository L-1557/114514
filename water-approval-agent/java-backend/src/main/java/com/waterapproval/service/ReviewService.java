package com.waterapproval.service;

import com.waterapproval.model.ReviewRequest;
import com.waterapproval.model.ReviewResponse;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;
import org.springframework.web.reactive.function.client.WebClientRequestException;
import reactor.core.publisher.Mono;
import java.time.Duration;

@Service
public class ReviewService {

    @Autowired
    private WebClient webClient;

    private static final int MAX_RETRIES = 3;
    private static final Duration RETRY_DELAY = Duration.ofSeconds(1);

    public Mono<ReviewResponse> submitReview(ReviewRequest request) {
        return submitReviewWithRetry(request, 0);
    }

    private Mono<ReviewResponse> submitReviewWithRetry(ReviewRequest request, int retryCount) {
        return webClient.post()
                .uri("/api/review")
                .bodyValue(request)
                .retrieve()
                .bodyToMono(ReviewResponse.class)
                .timeout(Duration.ofSeconds(60))
                .onErrorResume(WebClientRequestException.class, e -> {
                    System.err.println("AI 服务请求失败：" + e.getMessage());
                    if (retryCount < MAX_RETRIES) {
                        System.out.println("重试 " + (retryCount + 1) + "/" + MAX_RETRIES);
                        return Mono.delay(RETRY_DELAY)
                                .flatMap(delay -> submitReviewWithRetry(request, retryCount + 1));
                    }
                    return Mono.error(new RuntimeException("AI 服务不可用，已重试 " + MAX_RETRIES + " 次"));
                })
                .onErrorResume(Exception.class, e -> {
                    System.err.println("AI 服务连接失败：" + e.getMessage());
                    if (retryCount < MAX_RETRIES) {
                        System.out.println("重试 " + (retryCount + 1) + "/" + MAX_RETRIES);
                        return Mono.delay(RETRY_DELAY)
                                .flatMap(delay -> submitReviewWithRetry(request, retryCount + 1));
                    }
                    return Mono.error(new RuntimeException("无法连接到 AI 服务，已重试 " + MAX_RETRIES + " 次"));
                });
    }

    public Mono<ReviewResponse> submitStableReview(ReviewRequest request) {
        return webClient.post()
                .uri("/api/review/stable")
                .bodyValue(request)
                .retrieve()
                .bodyToMono(ReviewResponse.class)
                .timeout(Duration.ofSeconds(60))
                .onErrorResume(Exception.class, e -> {
                    System.err.println("稳定性审查失败：" + e.getMessage());
                    return submitReview(request);
                });
    }
}
