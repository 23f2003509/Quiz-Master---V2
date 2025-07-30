<template>
  <div>
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark shadow">
      <div class="container-fluid">
        <span class="navbar-brand fw-bold">
          <i class="bi bi-mortarboard"></i> Quiz Master - Dashboard
        </span>
        <div class="collapse navbar-collapse justify-content-end">
          <ul class="navbar-nav">
            <li class="nav-item">
              <router-link class="nav-link" to="/">
                <i class="bi bi-house"></i> Home
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/user_profile">
                <i class="bi bi-person-circle"></i> Profile
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/user_summary">
                <i class="bi bi-graph-up"></i> Quiz Summary
              </router-link>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="/login" @click.prevent="logout">
                <i class="bi bi-box-arrow-right"></i> Logout
              </a>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <!-- Welcome User -->
    <div class="container mt-5 text-center">
      <h4 class="fw-bold text-dark mb-3">Welcome, {{ localUsername }} 👋</h4>
      <h3 class="fw-bold mb-4 text-primary">
        <i class="bi bi-list-ul"></i> Available Quizzes
      </h3>
    </div>
    <!-- Search & Sort Controls -->
    <div class="container mb-4">
    <div class="d-flex flex-column flex-md-row justify-content-between align-items-center gap-3">
        <input
        type="text"
        class="form-control flex-fill"
        placeholder="🔍 Search quiz by name, subject, or chapter..."
        v-model="searchTerm"
        />

        <select class="form-select" v-model="sortOrder" style="max-width: 220px;">
        <option value="desc">📅 Newest First</option>
        <option value="asc">📆 Oldest First</option>
        </select>
    </div>
    </div>



    <!-- Quiz Cards -->
    <div class="container pb-5">
      <div class="row">
        <div class="col-lg-4 col-md-6 col-sm-12 mb-4" v-for="quiz in filteredQuizzes" :key="quiz.id">
          <div class="card quiz-card h-100 border-0">
            <div class="card-body d-flex flex-column">
              <h5 class="card-title text-dark fw-semibold mb-2">
                <i class="bi bi-journal-text text-primary me-1"></i> {{ quiz.name }}
              </h5>

              <p class="card-text text-muted mb-1">
                <i class="bi bi-info-circle me-1"></i> {{ quiz.description || 'No description' }}
              </p>

              <p class="card-text mb-1">
                <i class="bi bi-book me-1 text-secondary"></i>
                <strong>Subject:</strong> {{ quiz.subject || 'N/A' }}
              </p>

              <p class="card-text mb-1">
                <i class="bi bi-bookmark me-1 text-secondary"></i>
                <strong>Chapter:</strong> {{ quiz.chapter || 'N/A' }}
              </p>

              <p class="card-text mb-2 text-secondary">
                <i class="bi bi-calendar me-1"></i>
                <strong>Created on:</strong> {{ formatDate(quiz.date_created) }}
              </p>

              <span class="badge bg-info mb-3 align-self-start">
                <i class="bi bi-clock me-1"></i> {{ formatDuration(quiz.duration) }}
              </span>

              <button class="btn btn-outline-primary mt-auto w-100 fw-bold" @click="startQuiz(quiz.id)">
                <i class="bi bi-play-fill me-1"></i> Start Quiz
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Eraf_UserDashboard",
  data() {
    return {
      quizzes: [],
      searchTerm: "",
      sortOrder: "desc",
      localUsername: localStorage.getItem("username") || "User",
    };
  },
  methods: {
    async fetchQuizzes() {
      const token = localStorage.getItem("user_token");
      const response = await fetch("http://localhost:5000/add_quiz", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      const data = await response.json();
      console.log(data);
      if (response.ok) {
        this.quizzes = data;
      } else {
        alert(data.message || "Failed to fetch quizzes");
      }
    },
    startQuiz(quizId) {
      this.$router.push(`/start_quiz/${quizId}`);
    },
    logout() {
      localStorage.removeItem("user_token");
      localStorage.removeItem("username");
      localStorage.removeItem("user_id");
      this.$router.push("/");
    },
    formatDuration(durationStr) {
      const [hours, minutes, seconds] = durationStr.split(":").map(Number);
      let result = "";
      if (hours > 0) result += `${hours}h `;
      if (minutes > 0) result += `${minutes}m `;
      if (hours === 0 && minutes === 0) result += `${seconds}s`;
      return result.trim();
    },
    formatDate(dateStr) {
      const date = new Date(dateStr);
      return date.toLocaleDateString("en-IN", {
        day: "2-digit",
        month: "short",
        year: "numeric",
      });
    },
  },
  computed: {
    filteredQuizzes() {
        return this.quizzes
        .filter((q) =>
            q.name.toLowerCase().includes(this.searchTerm.toLowerCase()) || q.chapter.toLowerCase().includes(this.searchTerm.toLowerCase()) || q.subject.toLowerCase().includes(this.searchTerm.toLowerCase())
        )
        .sort((a, b) => {
            const dateA = new Date(a.date_created);
            const dateB = new Date(b.date_created);
            return this.sortOrder === "asc"
            ? dateA - dateB
            : dateB - dateA;
        });
    },
},
  mounted() {
    this.fetchQuizzes();
  },
};
</script>

<style scoped>
body {
  background: linear-gradient(135deg, #f0f4ff, #dbeafe);
  min-height: 100vh;
}

.quiz-card {
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(6px);
  border-radius: 1rem;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  border: 1px solid rgba(200, 200, 255, 0.4);
}

.quiz-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 0 20px rgba(0, 123, 255, 0.2);
}

.card-title {
  font-size: 1.25rem;
}

.badge {
  font-size: 0.9rem;
  padding: 0.5em 0.7em;
  background-color: #0dcaf0;
  color: #fff;
}

.btn-outline-primary {
  border-radius: 30px;
  font-weight: 600;
}


.form-control,
.form-select {
  border-radius: 10px;
}


</style>
