# Codealpha-Task-3

1. Initialize the app with Flask and set up a secret key for session management.
2. Initialize the SQLite database and create a `users` table if it doesn't exist.
   - Add a default user (admin) with a hashed password for testing.

3. Define a route for the home page:
   - If the user is logged in (session exists), display a welcome message.
   - If not logged in, display links to the login and registration pages.

4. Define a route for the registration page:
   - Show a form where users can enter a username and password.
   - If the form is submitted:
   - Hash the password using bcrypt.
   - Check if the username already exists in the database.
   - If it doesn't exist, store the username and hashed password in the database.
   - Redirect to the login page after successful registration.

5. Define a route for the login page:
   - Show a form for the username and password.
   - If the form is submitted:
   - Retrieve the hashed password from the database.
   - Compare the entered password with the stored hash using bcrypt.
   - If valid, store the username in the session.
   - Redirect to the home page with a welcome message.

6. Define a route for the logout page:
   - Clear the session (remove the stored username).
   - Redirect to the home page.

7. Ensure passwords are hashed using bcrypt for secure storage.
8. Protect routes with session management, ensuring users stay logged in across requests.
9. Run the Flask app locally for testing.
10. (Optional) Add further improvements like session expiration or CSRF protection.
