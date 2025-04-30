package com.example.demo.model;

import jakarta.persistence.*;

@Entity
@Table(name = "users")
public class User {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    // Login
    @Column(unique = true, nullable = false)
    private String email;

    @Column(nullable = false)
    private String password;

    // Section 1: Personal Info
    private String fullName;
    private String dob; // CHANGED from LocalDate to String
    private String contactEmail;
    private String phone;
    private String location;
    private String preferredLanguages;

    // Section 2: Education
    private String educationLevel;
    private String institutionName;
    private String major;
    private String graduationDate; // CHANGED from LocalDate to String
    private Double gpa;
    private String achievements;
    private String coursework;
    private String academicCertifications;

    // Section 3: Aspirations
    private String careerInterests;
    private String industrySectors;
    private String shortTermGoals;
    private String longTermGoals;
    private String dreamJob;

    // Section 4: Skills
    private String programmingLanguages;
    private String softwareSkills;
    private String techCertifications;
    private String skillLevels;
    private String softSkills;

    // Section 5: Work Experience
    @Column(columnDefinition = "TEXT")
    private String workExperience;

    // Section 6: Networking
    private String linkedin;
    private String github;
    private String otherSocial;
    private String website;

    // ----------------- Getter and Setter Methods -----------------

    public String getEmail() {
        return this.email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public String getPassword() {
        return this.password;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    // Personal Info Section Getters and Setters
    public String getFullName() {
        return fullName;
    }

    public void setFullName(String fullName) {
        this.fullName = fullName;
    }

    public String getDob() {
        return dob;
    }

    public void setDob(String dob) {
        this.dob = dob;
    }

    public String getContactEmail() {
        return contactEmail;
    }

    public void setContactEmail(String contactEmail) {
        this.contactEmail = contactEmail;
    }

    public String getPhone() {
        return phone;
    }

    public void setPhone(String phone) {
        this.phone = phone;
    }

    public String getLocation() {
        return location;
    }

    public void setLocation(String location) {
        this.location = location;
    }

    public String getPreferredLanguages() {
        return preferredLanguages;
    }

    public void setPreferredLanguages(String preferredLanguages) {
        this.preferredLanguages = preferredLanguages;
    }

    // Education Section Getters and Setters
    public String getEducationLevel() {
        return educationLevel;
    }

    public void setEducationLevel(String educationLevel) {
        this.educationLevel = educationLevel;
    }

    public String getInstitutionName() {
        return institutionName;
    }

    public void setInstitutionName(String institutionName) {
        this.institutionName = institutionName;
    }

    public String getMajor() {
        return major;
    }

    public void setMajor(String major) {
        this.major = major;
    }

    public String getGraduationDate() {
        return graduationDate;
    }

    public void setGraduationDate(String graduationDate) {
        this.graduationDate = graduationDate;
    }

    public Double getGpa() {
        return gpa;
    }

    public void setGpa(Double gpa) {
        this.gpa = gpa;
    }

    public String getAchievements() {
        return achievements;
    }

    public void setAchievements(String achievements) {
        this.achievements = achievements;
    }

    public String getCoursework() {
        return coursework;
    }

    public void setCoursework(String coursework) {
        this.coursework = coursework;
    }

    public String getAcademicCertifications() {
        return academicCertifications;
    }

    public void setAcademicCertifications(String academicCertifications) {
        this.academicCertifications = academicCertifications;
    }

    // Aspirations Section Getters and Setters
    public String getCareerInterests() {
        return careerInterests;
    }

    public void setCareerInterests(String careerInterests) {
        this.careerInterests = careerInterests;
    }

    public String getIndustrySectors() {
        return industrySectors;
    }

    public void setIndustrySectors(String industrySectors) {
        this.industrySectors = industrySectors;
    }

    public String getShortTermGoals() {
        return shortTermGoals;
    }

    public void setShortTermGoals(String shortTermGoals) {
        this.shortTermGoals = shortTermGoals;
    }

    public String getLongTermGoals() {
        return longTermGoals;
    }

    public void setLongTermGoals(String longTermGoals) {
        this.longTermGoals = longTermGoals;
    }

    public String getDreamJob() {
        return dreamJob;
    }

    public void setDreamJob(String dreamJob) {
        this.dreamJob = dreamJob;
    }

    // Skills Section Getters and Setters
    public String getProgrammingLanguages() {
        return programmingLanguages;
    }

    public void setProgrammingLanguages(String programmingLanguages) {
        this.programmingLanguages = programmingLanguages;
    }

    public String getSoftwareSkills() {
        return softwareSkills;
    }

    public void setSoftwareSkills(String softwareSkills) {
        this.softwareSkills = softwareSkills;
    }

    public String getTechCertifications() {
        return techCertifications;
    }

    public void setTechCertifications(String techCertifications) {
        this.techCertifications = techCertifications;
    }

    public String getSkillLevels() {
        return skillLevels;
    }

    public void setSkillLevels(String skillLevels) {
        this.skillLevels = skillLevels;
    }

    public String getSoftSkills() {
        return softSkills;
    }

    public void setSoftSkills(String softSkills) {
        this.softSkills = softSkills;
    }

    // Work Experience Section Getters and Setters
    public String getWorkExperience() {
        return workExperience;
    }

    public void setWorkExperience(String workExperience) {
        this.workExperience = workExperience;
    }

    // Networking Section Getters and Setters
    public String getLinkedin() {
        return linkedin;
    }

    public void setLinkedin(String linkedin) {
        this.linkedin = linkedin;
    }

    public String getGithub() {
        return github;
    }

    public void setGithub(String github) {
        this.github = github;
    }

    public String getOtherSocial() {
        return otherSocial;
    }

    public void setOtherSocial(String otherSocial) {
        this.otherSocial = otherSocial;
    }

    public String getWebsite() {
        return website;
    }

    public void setWebsite(String website) {
        this.website = website;
    }
}
