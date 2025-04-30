package com.example.demo.controller;

import com.example.demo.model.User;
import com.example.demo.service.UserService;
import com.example.demo.model.JwtResponse;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/auth")
@CrossOrigin(origins = "*")
public class AuthController {

    @Autowired
    private UserService userService;

    // ✅ Register Endpoint
    @PostMapping("/register")
    public ResponseEntity<String> registerUser(@RequestBody User user) {
        try {
            userService.registerUser(user);  // Register the user
            return new ResponseEntity<>("User registered successfully!", HttpStatus.CREATED);
        } catch (Exception e) {
            return new ResponseEntity<>("Registration failed: " + e.getMessage(), HttpStatus.BAD_REQUEST);
        }
    }

    // 🔐 Login Endpoint (Fixed version that matches Postman + JWT idea)
    @PostMapping("/login")
    public ResponseEntity<?> loginUser(@RequestBody User loginRequest) {
        try {
            String email = loginRequest.getEmail();
            String password = loginRequest.getPassword();

            // Authenticate user and generate token
            String token = userService.authenticate(email, password); // Should return JWT or null

            if (token != null && !token.isEmpty()) {
                return ResponseEntity.ok(new JwtResponse("Login Successful", token));
            } else {
                return new ResponseEntity<>("Invalid credentials!", HttpStatus.UNAUTHORIZED);
            }
        } catch (Exception e) {
            return new ResponseEntity<>("Error during login: " + e.getMessage(), HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    // ✅ Profile Section Update Endpoints
    @PutMapping("/profile/{email}/personal-info")
    public ResponseEntity<String> updatePersonalInfo(@PathVariable String email, @RequestBody User updatedInfo) {
        return userService.updateSection(email, updatedInfo, "personal");
    }

    @PutMapping("/profile/{email}/education")
    public ResponseEntity<String> updateEducation(@PathVariable String email, @RequestBody User updatedInfo) {
        return userService.updateSection(email, updatedInfo, "education");
    }

    @PutMapping("/profile/{email}/aspirations")
    public ResponseEntity<String> updateAspirations(@PathVariable String email, @RequestBody User updatedInfo) {
        return userService.updateSection(email, updatedInfo, "aspirations");
    }

    @PutMapping("/profile/{email}/skills")
    public ResponseEntity<String> updateSkills(@PathVariable String email, @RequestBody User updatedInfo) {
        return userService.updateSection(email, updatedInfo, "skills");
    }

    @PutMapping("/profile/{email}/experience")
    public ResponseEntity<String> updateExperience(@PathVariable String email, @RequestBody User updatedInfo) {
        return userService.updateSection(email, updatedInfo, "experience");
    }

    @PutMapping("/profile/{email}/networking")
    public ResponseEntity<String> updateNetworking(@PathVariable String email, @RequestBody User updatedInfo) {
        return userService.updateSection(email, updatedInfo, "networking");
    }
}
