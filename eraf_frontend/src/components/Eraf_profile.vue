<template>
  <div class="container mt-5">
    <h2 class="text-center text-primary mb-4">👤 User Profile</h2>

    <!-- Back Button -->
    <div class="text-center mb-4">
      <router-link to="/user" class="btn btn-outline-primary">
        ← Back to Dashboard
      </router-link>
    </div>

    <!-- User Info -->
    <div v-if="user" class="card mx-auto" style="max-width: 500px;">
      <div class="card-body">
        <h4 class="card-title text-center text-success">Welcome, {{ user.username }}</h4>
        <ul class="list-group list-group-flush mt-4">
          <li class="list-group-item">
            <strong>Email:</strong> {{ user.email }} <br>
            <strong>Full Name:</strong> {{ user.fullname }} <br>
            <strong>dob:</strong> {{ user.dob }} <br>
            <strong>qualification:</strong> {{ user.qualification }} <br>


          </li>
          <li class="list-group-item">
            <strong>Joined On:</strong> {{ formatDate(user.created_at) }}
          </li>
        </ul>
      </div>
    </div>

    <div v-else class="text-center text-muted mt-4">
      Loading user profile...
    </div>
  </div>
</template>

<script>
export default {
  name: "Eraf_UserProfile",
  data() {
    return {
      user: null,
    };
  },
  methods: {
    async fetchUserProfile() {
      const token = localStorage.getItem("user_token");
      try {
        const res = await fetch("http://127.0.0.1:5000/profile", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (!res.ok) throw new Error("Failed to fetch user profile");

        this.user = await res.json();
      } catch (err) {
        alert("Error: " + err.message);
      }
    },
    formatDate(dateStr) {
      const date = new Date(dateStr);
      return date.toLocaleDateString("en-IN", {
        year: "numeric",
        month: "long",
        day: "numeric",
      });
    },
  },
  mounted() {
    this.fetchUserProfile();
  },
};
</script>

<style scoped>
.card {
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}
</style>
