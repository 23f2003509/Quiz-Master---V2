<template>
  <div>
        <nav class="navbar navbar-expand-lg navbar-light bg-light shadow-sm">
            <div class="container-fluid">
                <!-- Left side -->
                <div class="d-flex align-items-center">
                <router-link class="navbar-brand fw-bold me-4" to="/">Quiz Master</router-link>
                <router-link to="/" class="nav-link">Home</router-link>
                </div>

                <!-- Right side -->
                <div class="d-flex align-items-center">
                <router-link to="/profile" class="nav-link me-3">Profile</router-link>
                <a href="/login" class="nav-link text-danger" @click.prevent="logout">Logout</a>
                </div>
            </div>
        </nav>

    <!-- Dashboard Section -->
    <div class="container py-5">
      <h2 class="text-center fw-bold mb-5">Admin Dashboard</h2>

      <div class="row g-4">
        <!-- Manage Users Card -->
        <div class="col-md-4">
          <div class="card h-100 shadow border-0 text-center p-4 hover-card">
            <i class="bi bi-people-fill display-4 text-primary mb-3"></i>
            <h5 class="card-title">Manage Users</h5>
            <p class="card-text">View, edit, or delete registered users from the system.</p>
            <router-link to="/manage_users" class="btn btn-outline-primary mt-2 w-100">Go to Users</router-link>
          </div>
        </div>

        <!-- Manage Subjects Card -->
        <div class="col-md-4">
          <div class="card h-100 shadow border-0 text-center p-4 hover-card">
            <i class="bi bi-journal-bookmark-fill display-4 text-success mb-3"></i>
            <h5 class="card-title">Manage Subjects</h5>
            <p class="card-text">Add or edit subjects and chapters for quizzes.</p>
            <router-link to="/manage_subjects" class="btn btn-outline-success mt-2 w-100">Go to Subjects</router-link>
          </div>
        </div>

        <!-- Manage Quizzes Card -->
        <div class="col-md-4">
          <div class="card h-100 shadow border-0 text-center p-4 hover-card">
            <i class="bi bi-patch-question-fill display-4 text-warning mb-3"></i>
            <h5 class="card-title">Manage Quizzes</h5>
            <p class="card-text">Create, update, or remove quizzes for all subjects.</p>
            <router-link to="/manage_quizzes" class="btn btn-outline-warning mt-2 w-100">Go to Quizzes</router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ErafAdminDashboard',
  methods: {
    logout() {
      localStorage.removeItem('admin_token')
      sessionStorage.clear()
      this.$router.push('/login')
    }
  }
}
</script>

<style scoped>
.hover-card:hover {
  transform: scale(1.02);
  transition: 0.3s;
  cursor: pointer;
}
.navbar-brand {
  font-size: 1.4rem;
}
</style>
