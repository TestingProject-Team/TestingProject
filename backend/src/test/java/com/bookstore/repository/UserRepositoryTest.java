package com.bookstore.repository;

import com.bookstore.entity.AuthProvider;
import com.bookstore.entity.Role;
import com.bookstore.entity.User;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.test.context.ActiveProfiles;

import java.util.Optional;

import static org.assertj.core.api.Assertions.assertThat;
import static org.junit.jupiter.api.Assertions.assertThrows;

@DataJpaTest
@ActiveProfiles("test")
class UserRepositoryTest {

    @Autowired
    private UserRepository userRepository;

    private User sampleUser;

    @BeforeEach
    void setUp() {
        sampleUser = User.builder()
                .username("testuser")
                .password("password123")
                .fullName("Test User")
                .email("testuser@example.com")
                .phone("0987654321")
                .provider(AuthProvider.LOCAL)
                .role(Role.USER)
                .build();
    }

    @Test
    @DisplayName("Save user and find by username - Success")
    void testSaveAndFindByUsernameSuccess() {
        User savedUser = userRepository.save(sampleUser);
        assertThat(savedUser.getId()).isNotNull();

        Optional<User> found = userRepository.findByUsername("testuser");
        assertThat(found).isPresent();
        assertThat(found.get().getFullName()).isEqualTo("Test User");
    }

    @Test
    @DisplayName("Find user by email - Success")
    void testFindByEmailSuccess() {
        userRepository.save(sampleUser);

        Optional<User> found = userRepository.findByEmail("testuser@example.com");
        assertThat(found).isPresent();
        assertThat(found.get().getUsername()).isEqualTo("testuser");
    }

    @Test
    @DisplayName("Find user by phone - Success")
    void testFindByPhoneSuccess() {
        userRepository.save(sampleUser);

        Optional<User> found = userRepository.findByPhone("0987654321");
        assertThat(found).isPresent();
        assertThat(found.get().getUsername()).isEqualTo("testuser");
    }

    @Test
    @DisplayName("Find user by email and provider - Success")
    void testFindByEmailAndProviderSuccess() {
        userRepository.save(sampleUser);

        Optional<User> found = userRepository.findByEmailAndProvider("testuser@example.com", AuthProvider.LOCAL);
        assertThat(found).isPresent();

        Optional<User> foundGoogle = userRepository.findByEmailAndProvider("testuser@example.com", AuthProvider.GOOGLE);
        assertThat(foundGoogle).isEmpty();
    }

    @Test
    @DisplayName("Check existsByUsername, existsByEmail, existsByPhone")
    void testExistsByUsernameEmailPhone() {
        userRepository.save(sampleUser);

        assertThat(userRepository.existsByUsername("testuser")).isTrue();
        assertThat(userRepository.existsByEmail("testuser@example.com")).isTrue();
        assertThat(userRepository.existsByPhone("0987654321")).isTrue();

        assertThat(userRepository.existsByUsername("nonexistent")).isFalse();
        assertThat(userRepository.existsByEmail("nonexistent@example.com")).isFalse();
        assertThat(userRepository.existsByPhone("0000000000")).isFalse();
    }

    @Test
    @DisplayName("Find non-existent user returns empty Optional")
    void testFindNonExistentUserReturnsEmpty() {
        Optional<User> found = userRepository.findByUsername("unknown");
        assertThat(found).isEmpty();
    }

    @Test
    @DisplayName("Save duplicate username throws DataIntegrityViolationException")
    void testDuplicateUsernameThrowsException() {
        userRepository.save(sampleUser);
        userRepository.flush();

        User duplicateUser = User.builder()
                .username("testuser") // duplicate
                .password("pass456")
                .fullName("Another User")
                .email("another@example.com")
                .role(Role.USER)
                .build();

        assertThrows(DataIntegrityViolationException.class, () -> {
            userRepository.saveAndFlush(duplicateUser);
        });
    }

    @Test
    @DisplayName("Update and Delete User CRUD operations")
    void testUpdateAndDeleteUser() {
        User savedUser = userRepository.save(sampleUser);
        Long id = savedUser.getId();

        savedUser.setFullName("Updated Name");
        userRepository.save(savedUser);

        User updatedUser = userRepository.findById(id).orElseThrow();
        assertThat(updatedUser.getFullName()).isEqualTo("Updated Name");

        userRepository.deleteById(id);
        assertThat(userRepository.findById(id)).isEmpty();
    }
}
