
package com.example.demo.service;

import com.example.demo.model.User;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import org.springframework.stereotype.Service;

@Service
public class FirebaseService {

    private final DatabaseReference databaseReference;

    public FirebaseService() {
        // Connect to root node 'users' inside your Firebase database
        this.databaseReference = FirebaseDatabase.getInstance().getReference("users");
    }

    // Save user to Firebase
    public void saveUserToFirebase(User user) {
        if (user.getEmail() != null) {
            // Save using email as unique key (you can choose ID also)
            String safeEmailKey = user.getEmail().replace(".", "_"); // Replace '.' to avoid Firebase path issues
            databaseReference.child(safeEmailKey).setValueAsync(user);
        }
    }
}
