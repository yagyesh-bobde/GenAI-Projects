package com.example.income_tax_chatbot;

import android.content.Intent;
import android.os.Bundle;
import android.text.TextUtils;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ProgressBar;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import com.google.android.gms.tasks.OnFailureListener;
import com.google.android.gms.tasks.OnSuccessListener;
import com.google.firebase.auth.AuthResult;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.firestore.FirebaseFirestore;

import java.util.HashMap;
import java.util.Map;

public class SignUpActivity extends AppCompatActivity {

    TextView txtSignIn;

    EditText edtFullName, edtEmail, edtMobile, edtPassword, edtConfirmPassword;

    ProgressBar progressBar;

    Button btnSignUp;

    String strFullName, strEmail, strMobile, strPassword, strConfirmPassword;

    String emailPattern = "[a-zA-Z0-9._-]+@[a-z]+\\.+[a-z]+";

    FirebaseAuth mAuth;

    FirebaseFirestore db;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_sign_up);

        txtSignIn = findViewById(R.id.txtSignIn);
        edtFullName = findViewById(R.id.edtSignUpFullName);
        edtEmail = findViewById(R.id.edtSignUpEmail);
        edtMobile = findViewById(R.id.edtSignUpMobile);
        edtPassword = findViewById(R.id.edtSignUpPassword);
        edtConfirmPassword = findViewById(R.id.edtSignUpConfirmPassword);
        progressBar = findViewById(R.id.signUpProgressBar);
        btnSignUp = findViewById(R.id.btnSignUp);

        mAuth = FirebaseAuth.getInstance();
        db = FirebaseFirestore.getInstance();

        txtSignIn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(SignUpActivity.this, LoginActivity.class);
                startActivity(intent);
            }
        });

        btnSignUp.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                strFullName = edtFullName.getText().toString();
                strEmail = edtEmail.getText().toString().trim();
                strMobile = edtMobile.getText().toString().trim();
                strPassword = edtPassword.getText().toString();
                strConfirmPassword = edtConfirmPassword.getText().toString();

                if (isValidate()) {
                    SignUp();
                }
            }
        });

    }

    private void SignUp() {
        btnSignUp.setVisibility(View.INVISIBLE);
        progressBar.setVisibility(View.VISIBLE);

        mAuth.createUserWithEmailAndPassword(strEmail, strPassword).addOnSuccessListener(new OnSuccessListener<AuthResult>() {
            @Override
            public void onSuccess(AuthResult authResult) {

                Map<String, Object> user = new HashMap<>();
                user.put("FullName", strFullName);
                user.put("Email", strEmail);
                user.put("Mobile", strMobile);

                db.collection("Users")
                        .document(strEmail)
                        .set(user)
                        .addOnSuccessListener(new OnSuccessListener<Void>() {
                            @Override
                            public void onSuccess(Void unused) {
                                Intent intent = new Intent(SignUpActivity.this, MainActivity.class);
                                startActivity(intent);
                                finish();
                            }
                        }).addOnFailureListener(new OnFailureListener() {
                            @Override
                            public void onFailure(@NonNull Exception e) {
                                Toast.makeText(SignUpActivity.this, "Error - " + e.getMessage(), Toast.LENGTH_SHORT).show();
                                btnSignUp.setVisibility(View.VISIBLE);
                                progressBar.setVisibility(View.INVISIBLE);
                            }
                        });
            }
        }).addOnFailureListener(new OnFailureListener() {
            @Override
            public void onFailure(@NonNull Exception e) {
                Toast.makeText(SignUpActivity.this, "Error - " + e.getMessage(), Toast.LENGTH_SHORT).show();
                btnSignUp.setVisibility(View.VISIBLE);
                progressBar.setVisibility(View.INVISIBLE);
            }
        });
    }

    private boolean isValidate() {
        if (TextUtils.isEmpty(strFullName)) {
            edtFullName.setError("FullName Field can't be Empty !");
            return false;
        }

        if (TextUtils.isEmpty(strEmail)) {
            edtEmail.setError("Email Field can't be Empty !");
            return false;
        }

        if (!strEmail.matches(emailPattern)) {
            edtEmail.setError("Enter a valid Email ID !");
            return false;
        }

        if (TextUtils.isEmpty(strMobile)) {
            edtMobile.setError("Mobile Field can't be Empty !");
            return false;
        }

        if (TextUtils.isEmpty(strPassword)) {
            edtPassword.setError("Password Field can't be Empty !");
            return false;
        }

        if (TextUtils.isEmpty(strConfirmPassword)) {
            edtConfirmPassword.setError("Confirm Password Field can't be Empty !");
            return false;
        }

        if (!strPassword.equals(strPassword)) {
            edtConfirmPassword.setError("Confirm Password and Password should be same !");
            return false;
        }

        return true;
    }
}