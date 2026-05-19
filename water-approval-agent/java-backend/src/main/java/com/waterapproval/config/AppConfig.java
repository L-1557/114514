package com.waterapproval.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.cors.CorsConfiguration;
import org.springframework.web.cors.UrlBasedCorsConfigurationSource;
import org.springframework.web.filter.CorsFilter;
import org.springframework.web.reactive.function.client.WebClient;
import java.time.Duration;

@Configuration
public class AppConfig {

    @Value("${python.ai.service.url:http://localhost:8000}")
    private String pythonAiServiceUrl;

    @Bean
    public CorsFilter corsFilter() {
        CorsConfiguration corsConfiguration = new CorsConfiguration();
        corsConfiguration.setAllowCredentials(true);
        corsConfiguration.addAllowedOriginPattern("*");
        corsConfiguration.addAllowedMethod("*");
        corsConfiguration.addAllowedHeader("*");
        corsConfiguration.setMaxAge(3600L);
        
        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        source.registerCorsConfiguration("/**", corsConfiguration);
        return new CorsFilter(source);
    }
    
    @Bean
    public WebClient webClient() {
        return WebClient.builder()
                .baseUrl(pythonAiServiceUrl)
                .codecs(configurer -> configurer.defaultCodecs().maxInMemorySize(50 * 1024 * 1024))
                .build();
    }
    
    @Bean
    public WebClient fileUploadWebClient() {
        return WebClient.builder()
                .baseUrl(pythonAiServiceUrl)
                .codecs(configurer -> configurer.defaultCodecs().maxInMemorySize(100 * 1024 * 1024))
                .build();
    }
}
