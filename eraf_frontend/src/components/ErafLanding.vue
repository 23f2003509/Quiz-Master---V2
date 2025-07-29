<template>
  <div>
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark px-4">
      <div class="container-fluid">
        <a class="navbar-brand fw-bold" href="#">📚 Quiz Master</a>
        <div class="ms-auto">
          <router-link to="/login" class="btn btn-outline-light me-2">Login</router-link>
          <router-link to="/signup" class="btn btn-warning">Sign Up</router-link>
        </div>
      </div>
    </nav>

    <!-- Hero Section -->
    <section class="bg-light text-dark py-5">
      <div class="container text-center">
        <h1 class="display-4 fw-bold">Welcome to Quiz Master!</h1>
        <p class="lead mt-3 mb-4">
          A powerful platform to test your knowledge, practice quizzes, and track your performance.
        </p>
        <router-link to="/signup" class="btn btn-lg btn-primary px-4 me-2">Get Started</router-link>
        <router-link to="/login" class="btn btn-lg btn-outline-secondary px-4">Login</router-link>
      </div>
    </section>

    <!-- Features Section -->
    <section class="container my-5">
      <div class="row text-center">
        <div class="col-md-4 mb-4">
          <i class="bi bi-bar-chart-fill display-4 text-primary"></i>
          <h4 class="mt-3">Track Progress</h4>
          <p>Monitor your quiz history and performance analytics with ease.</p>
        </div>
        <div class="col-md-4 mb-4">
          <i class="bi bi-person-lines-fill display-4 text-success"></i>
          <h4 class="mt-3">Admin Dashboard</h4>
          <p>Admins can manage quizzes, questions, and users with full control.</p>
        </div>
        <div class="col-md-4 mb-4">
          <i class="bi bi-lightbulb-fill display-4 text-warning"></i>
          <h4 class="mt-3">Smart Practice</h4>
          <p>AI-based suggestions to help you improve where it matters most.</p>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="bg-dark text-light py-3 text-center">
      <small>&copy; 2025 Quiz Master | Built by Eraf Ali</small>
    </footer>
  </div>
</template>

<script>
export default {
  name: "ErafLanding",
};
</script>

<style scoped>
.hero-section {
  background: linear-gradient(to right, #1e3c72, #2a5298);
  color: white;
}
</style>
