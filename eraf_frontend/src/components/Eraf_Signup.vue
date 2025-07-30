<template>
  <div class="container py-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card shadow p-4">
          <h2 class="text-center mb-4" >Sign Up to Quiz Master</h2>

          <form @submit.prevent="handleSignup">
            <div class="mb-3">
              <label for="fullname" class="form-label">Full Name</label>
              <input v-model="form.fullname" type="text" class="form-control" required />
            </div>

            <div class="mb-3">
              <label for="username" class="form-label">Username</label>
              <input v-model="form.username" type="text" class="form-control" required />
            </div>

            <div class="mb-3">
              <label for ="email" class="form-label">Email</label>
              <input v-model="form.email" type="email" class="form-control" required />
            </div>

            <div class="mb-3">
              <label for="password" class="form-label">Password</label>
              <input v-model="form.password" type="password" class="form-control" required />
            </div>

            <div class="mb-3">
              <label for="dob" class="form-label">Date of Birth</label>
              <input v-model="form.dob" type="date" class="form-control" required />
            </div>

            <div class="mb-3">
              <label for="qualification" class="form-label">Qualification</label>
              <input v-model="form.qualification" type="text" class="form-control" required />
            </div>

            <div class="d-grid">
              <button type="submit" class="btn btn-primary">Sign Up</button>
            </div>
          </form>

          <div class="text-center mt-3">
            <p>Already have an account?
              <router-link to="/login">Login here</router-link>
            </p>
          </div>
          <div class="text-center mt-3">
            <p>
              <router-link to="/">Back to Home</router-link>
            </p>
          </div>

          <div v-if="error" class="alert alert-danger mt-3" role="alert">
            {{ error }}
          </div>

          <div v-if="success" class="alert alert-success mt-3" role="alert">
            {{ success }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ErafSignup',
  data() {
    return {
      form: {
        fullname: '',
        username: '',
        email: '',
        password: '',
        dob: '',
        qualification: ''
      },
      error: '',
      success: ''
    };
  },
  methods: {
    async handleSignup() {
      this.error = '';
      this.success = '';

      try {
        const res = await fetch('http://localhost:5000/register', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(this.form)
        });

        const data = await res.json();

        if (res.status === 201) {
          this.success = data.message;
          setTimeout(() => this.$router.push('/login'), 2000);
        } else {
          this.error = data.message || 'Something went wrong';
        }
      } catch (err) {
        this.error = 'Server error. Please try again later.';
        console.error(err);
      }
    }
  }
};
</script>

<style scoped>
.card {
  border-radius: 1rem;
}
</style>
