package com.example.demo.service;

import com.example.demo.model.User;
import com.example.demo.repository.UserRepository;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.SignatureAlgorithm;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;

import java.util.Date;
import java.util.Optional;

@Service
public class UserService {

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private FirebaseService firebaseService; // Inject Firebase Service

    private final BCryptPasswordEncoder passwordEncoder = new BCryptPasswordEncoder();

    // JWT Secret Key
    @Value("${jwt.secret}")
    private String jwtSecret;

    // 🔐 Register a new user
    public User registerUser(User user) {
        Optional<User> existing = userRepository.findByEmailIgnoreCase(user.getEmail());
        if (existing.isPresent()) {
            throw new RuntimeException("Email already in use.");
        }

        // Log raw and encoded password
        System.out.println("Raw password before encoding: " + user.getPassword());

        String encoded = passwordEncoder.encode(user.getPassword());
        System.out.println("Encoded password: " + encoded);
        user.setPassword(encoded);

        // Save to MySQL database
        User savedUser = userRepository.save(user);

        // ALSO Save to Firebase Database
        firebaseService.saveUserToFirebase(savedUser);

        return savedUser;
    }

    // 🔑 Authenticate user for login
    public String authenticate(String email, String rawPassword) {
        Optional<User> userOpt = userRepository.findByEmailIgnoreCase(email.trim());

        if (userOpt.isPresent()) {
            User user = userOpt.get();

            // Debugging logs
            System.out.println("Authenticating user: " + email);
            System.out.println("Entered raw password: " + rawPassword);
            System.out.println("Stored hashed password: " + user.getPassword());
            System.out.println("Password match result: " + passwordEncoder.matches(rawPassword, user.getPassword()));

            if (passwordEncoder.matches(rawPassword, user.getPassword())) {
                System.out.println("Password matched successfully!");
                return generateToken(email);  // Return JWT token
            } else {
                System.out.println("Password did NOT match!");
            }
        } else {
            System.out.println("No user found with email: " + email);
        }

        throw new RuntimeException("Invalid credentials!");
    }

    // 📥 Generate JWT Token
    public String generateToken(String email) {
        long expirationTime = 1000 * 60 * 60 * 10; // 10 hours
        return Jwts.builder()
                .setSubject(email)
                .setExpiration(new Date(System.currentTimeMillis() + expirationTime))
                .signWith(SignatureAlgorithm.HS256, jwtSecret)
                .compact();
    }

    // 📥 Get user by email (optional)
    public Optional<User> getUserByEmail(String email) {
        return userRepository.findByEmailIgnoreCase(email);
    }

    // 📝 Update user profile sections
    public ResponseEntity<String> updateSection(String email, User updatedInfo, String section) {
        Optional<User> userOpt = userRepository.findByEmailIgnoreCase(email);
        if (userOpt.isEmpty()) {
            return new ResponseEntity<>("User not found", HttpStatus.NOT_FOUND);
        }

        User user = userOpt.get();

        // Handle different profile sections
        switch (section.toLowerCase()) {
            case "personal":
                user.setFullName(updatedInfo.getFullName());
                user.setDob(updatedInfo.getDob());
                user.setContactEmail(updatedInfo.getContactEmail());
                user.setPhone(updatedInfo.getPhone());
                user.setLocation(updatedInfo.getLocation());
                user.setPreferredLanguages(updatedInfo.getPreferredLanguages());
                break;
            case "education":
                user.setEducationLevel(updatedInfo.getEducationLevel());
                user.setInstitutionName(updatedInfo.getInstitutionName());
                user.setMajor(updatedInfo.getMajor());
                user.setGraduationDate(updatedInfo.getGraduationDate());
                user.setGpa(updatedInfo.getGpa());
                user.setAchievements(updatedInfo.getAchievements());
                user.setCoursework(updatedInfo.getCoursework());
                user.setAcademicCertifications(updatedInfo.getAcademicCertifications());
                break;
            case "aspirations":
                user.setCareerInterests(updatedInfo.getCareerInterests());
                user.setIndustrySectors(updatedInfo.getIndustrySectors());
                user.setShortTermGoals(updatedInfo.getShortTermGoals());
                user.setLongTermGoals(updatedInfo.getLongTermGoals());
                user.setDreamJob(updatedInfo.getDreamJob());
                break;
            case "skills":
                user.setProgrammingLanguages(updatedInfo.getProgrammingLanguages());
                user.setSoftwareSkills(updatedInfo.getSoftwareSkills());
                user.setTechCertifications(updatedInfo.getTechCertifications());
                user.setSkillLevels(updatedInfo.getSkillLevels());
                user.setSoftSkills(updatedInfo.getSoftSkills());
                break;
            case "experience":
                user.setWorkExperience(updatedInfo.getWorkExperience());
                break;
            case "networking":
                user.setLinkedin(updatedInfo.getLinkedin());
                user.setGithub(updatedInfo.getGithub());
                user.setOtherSocial(updatedInfo.getOtherSocial());
                user.setWebsite(updatedInfo.getWebsite());
                break;
            default:
                return new ResponseEntity<>("Invalid section", HttpStatus.BAD_REQUEST);
        }

        // Save the updated user data to the local MySQL database
        User updatedUser = userRepository.save(user);

        // Also update the user data in Firebase
        firebaseService.saveUserToFirebase(updatedUser);

        return new ResponseEntity<>("Profile updated successfully!", HttpStatus.OK);
    }
}
