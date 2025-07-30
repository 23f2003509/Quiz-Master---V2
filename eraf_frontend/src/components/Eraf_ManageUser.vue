<template>
  <div class="container mt-5">
    <h2 class="text-center text-primary mb-4">Registered Users</h2>

    <div class="mb-3 text-center">
      <router-link to="/admin" class="btn btn-outline-secondary">
        ← Back to Admin Dashboard
      </router-link>
    </div>

    <div class="row mb-4 justify-content-center">
      <div class="col-md-6">
        <input
          type="text"
          v-model="searchTerm"
          class="form-control"
          placeholder="Search by username, email, or name..."
        />
      </div>
    </div>

    <div v-if="loading" class="text-center text-muted">Loading users...</div>

    <table v-else class="table table-bordered table-hover shadow-sm">
      <thead class="table-dark">
        <tr>
          <th>ID</th>
          <th>Username</th>
          <th>Full Name</th>
          <th>Email</th>
          <th>DOB</th>
          <th>Qualification</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="user in filteredUsers"
          :key="user.id"
        >
          <td>{{ user.id }}</td>
          <td>{{ user.username }}</td>
          <td>{{ user.fullname }}</td>
          <td>{{ user.email }}</td>
          <td>{{ formatDate(user.dob) }}</td>
          <td>{{ user.qualification }}</td>
        </tr>
      </tbody>
    </table>

    <div v-if="filteredUsers.length === 0 && !loading" class="text-center text-muted">
      No matching users found.
    </div>
  </div>
</template>

<script>
export default {
  name: "Eraf_AdminUsers",
  data() {
    return {
      users: [],
      loading: true,
      searchTerm: "",
    };
  },
  computed: {
    filteredUsers() {
      const term = this.searchTerm.toLowerCase();
      return this.users.filter((user) =>
        user.username.toLowerCase().includes(term) ||
        user.fullname.toLowerCase().includes(term) ||
        user.email.toLowerCase().includes(term)
      );
    },
  },
  methods: {
    async fetchUsers() {
      const token = localStorage.getItem("admin_token");
      try {
        const res = await fetch("http://127.0.0.1:5000/manage_users", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        if (res.ok) {
          this.users = await res.json();
        } else {
          alert("Failed to fetch users");
        }
      } catch (err) {
        console.error("Error fetching users:", err);
      } finally {
        this.loading = false;
      }
    },
    formatDate(dateString) {
      if (!dateString) return "-";
      const date = new Date(dateString);
      return date.toLocaleDateString("en-IN", {
        year: "numeric",
        month: "short",
        day: "numeric",
      });
    },
  },
  mounted() {
    this.fetchUsers();
  },
};
</script>

<style scoped>
.container {
  max-width: 1100px;
}
.table {
  font-size: 0.94rem;
}
input.form-control {
  border-radius: 0.5rem;
  padding: 0.5rem 1rem;
}
.btn-outline-secondary {
  border-radius: 0.5rem;
  font-weight: 500;
}
</style>
