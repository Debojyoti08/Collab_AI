package com.example.demo.model;

public class JwtResponse {
    private String message;
    private String token;

    // Constructor
    public JwtResponse(String message, String token) {
        this.message = message;
        this.token = token;
    }

    // Getters
    public String getMessage() {
        return message;
    }

    public String getToken() {
        return token;
    }

    // Setters
    public void setMessage(String message) {
        this.message = message;
    }

    public void setToken(String token) {
        this.token = token;
    }
}
