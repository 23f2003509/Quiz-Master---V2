<template>
  <div class="container d-flex align-items-center justify-content-center vh-100">
    <div class="card shadow p-4" style="max-width: 400px; width: 100%">
      <h3 class="text-center mb-4 fw-bold">Login to Quiz Master</h3>

      <form @submit.prevent="handleLogin">
        <div class="mb-3">
          <label for="username" class="form-label">Username</label>
          <input
            v-model="username"
            type="text"
            class="form-control"
            id="username"
            required
          />
        </div>

        <div class="mb-3">
          <label for="password" class="form-label">Password</label>
          <input
            v-model="password"
            type="password"
            class="form-control"
            id="password"
            required
          />
        </div>

        <button type="submit" class="btn btn-primary w-100">Login</button>
      </form>

      <div class="mt-3 text-center">
        <small>Don't have an account?
          <router-link to="/signup">Sign Up</router-link>
        </small>
      </div>
      <div class="mt-3 text-center">
        <router-link to="/">Back to Home</router-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ErafLogin",
  data() {
    return {
      username: "",
      password: "",
    };
  },
  methods: {
    async handleLogin() {
      
      console.log("Logging in with:", this.username, this.password);
      const response=await fetch("http://127.0.0.1:5000/login", {
        method:"POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username: this.username,
          password: this.password,
        }),
      })

      const data=await response.json()
      console.log(data) // for checking
      if (response.ok) {
          if (data.username === "admin") {
            localStorage.setItem("admin_username", data.username);
            localStorage.setItem("admin_id", data.user_id);
            localStorage.setItem("admin_token", data.access_token);
            this.$router.push("/admin");
          } else {
            localStorage.setItem("username", data.username);
            localStorage.setItem("user_id", data.user_id);
            localStorage.setItem("user_token", data.access_token);
            this.$router.push("/user");
          }
      } else {
        alert(data.message);
      }

    },
  },
};
</script>

<style scoped>
body {
  background-color: #f8f9fa;
}
</style>
