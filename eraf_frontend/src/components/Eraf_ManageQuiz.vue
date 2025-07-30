<template>
  <div class="container py-4">
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary mb-4">
      <div class="container-fluid">
        <router-link class="navbar-brand fw-bold" to="/">QuizMaster Admin</router-link>
        <div class="collapse navbar-collapse">
          <ul class="navbar-nav me-auto">
            <li class="nav-item">
              <router-link class="nav-link" to="/admin">Dashboard</router-link>
            </li>
          </ul>
          <ul class="navbar-nav ms-auto">
            <li class="nav-item">
              <router-link class="nav-link" to="/" @click="logout">Logout</router-link>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <!-- Header and Search -->
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2 class="fw-bold">Manage Quizzes</h2>
      <input v-model="searchQuery" class="form-control w-25" placeholder="Search quizzes..." />
      <button class="btn btn-success ms-3" @click="showQuizModal = true">
        <i class="bi bi-plus-circle"></i> Add Quiz
      </button>
    </div>

    <!-- Quiz Cards -->
    <div v-if="filteredQuizzes.length" class="row g-4">
      <div class="col-md-6" v-for="quiz in filteredQuizzes" :key="quiz.id">
        <div class="card shadow-sm rounded-4 border-0">
          <div class="card-body">
            <div class="d-flex justify-content-between mb-2">
              <div>
                <h5 class="fw-bold">{{ quiz.name }}</h5>
                <p class="text-muted small mb-1">{{ quiz.description }}</p>
                <p class="mb-1">
                  <strong>Subject:</strong> {{ quiz.subject }} <br>
                  <strong>Chapter:</strong> {{ quiz.chapter }}
                </p>
                <p class="mb-1">
                  <strong>Duration:</strong> {{ quiz.duration }} |
                  <strong>Single Attempt:</strong> {{ quiz.single_attempt ? 'Yes' : 'No' }}
                </p>
                <p><strong>Created:</strong> {{ quiz.date_created }}</p>
              </div>
              <div>
                <button class="btn btn-outline-primary btn-sm me-1" @click="editQuiz(quiz)">
                  Edit
                </button>
                <button class="btn btn-outline-danger btn-sm" @click="deleteQuiz(quiz.id)">
                  Delete
                </button>
              </div>
            </div>
            <button class="btn btn-outline-dark w-100 rounded-pill" @click="viewQuiz(quiz.id)">
              View Quiz
            </button>
          </div>
        </div>
      </div>
    </div>
    <div v-else class="text-center text-muted mt-5">No quizzes found.</div>

    <!-- Add/Edit Modal -->
    <div v-if="showQuizModal" class="modal d-block" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ editingQuizId ? 'Edit Quiz' : 'Add Quiz' }}</h5>
            <button class="btn-close" @click="cancelForm"></button>
          </div>
          <div class="modal-body">
            <input v-model="quizForm.name" class="form-control" placeholder="Quiz Name" />
            <input v-model="quizForm.description" class="form-control mt-2" placeholder="Description" />
            <input v-model="quizForm.duration" class="form-control mt-2" placeholder="HH:MM:SS" />
            <input v-model="quizForm.date_created" class="form-control mt-2" type="date" />
            <select v-model="quizForm.chapter_id" class="form-control mt-2">
              <option disabled value="">Select Chapter</option>
              <option v-for="chapter in chapterList" :value="chapter.id" :key="chapter.id">
                {{ chapter.name }} ({{ chapter.subject_name }})
              </option>
            </select>
            <div class="form-check mt-2">
              <input class="form-check-input" type="checkbox" v-model="quizForm.single_attempt" id="singleAttempt" />
              <label class="form-check-label" for="singleAttempt">Single Attempt</label>
            </div>
          </div>
          <div class="modal-footer">
            <button class="btn btn-secondary" @click="cancelForm">Cancel</button>
            <button class="btn btn-primary" @click="editingQuizId ? updateQuiz() : addQuiz()">
              {{ editingQuizId ? 'Update' : 'Add' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Eraf_ManageQuiz',
  data() {
    return {
      quizzes: [],
      chapterList: [],
      showQuizModal: false,
      editingQuizId: null,
      searchQuery: '',


      quizForm: {
        name: '',
        description: '',
        duration: '',
        date_created: '',
        chapter_id: '',
        single_attempt: false
      }
    };
  },
  computed: {
    filteredQuizzes() {
      if (!this.searchQuery) return this.quizzes;
      return this.quizzes.filter(q => q.name.toLowerCase().includes(this.searchQuery.toLowerCase()) || q.chapter.toLowerCase().includes(this.searchQuery.toLowerCase()) || q.subject.toLowerCase().includes(this.searchQuery.toLowerCase()));
    }
  },
  methods: {
    async fetchQuizzes() {
      const token = localStorage.getItem('admin_token');
      const res = await fetch('http://localhost:5000/add_quiz', {
        headers: { Authorization: `Bearer ${token}` }
      });
      const data = await res.json();
      this.quizzes = data;
      console.log(this.quizzes);
    },
    async fetchChapters() {
      const token = localStorage.getItem('admin_token');
      const res = await fetch('http://localhost:5000/subject', {
        headers: { Authorization: `Bearer ${token}` }
      });
      const data = await res.json();
      const allChapters = [];
      data.forEach(sub => {
        sub.chapters.forEach(chap => {
          allChapters.push({ ...chap, subject_name: sub.name });
        });
      });
      this.chapterList = allChapters;
    },
    cancelForm() {
      this.quizForm = {
        name: '', description: '', duration: '', date_created: '', chapter_id: '', single_attempt: false
      };
      this.editingQuizId = null;
      this.showQuizModal = false;
    },
    async addQuiz() {
      const token = localStorage.getItem('admin_token');
      const res = await fetch(`http://localhost:5000/add_quiz/${this.quizForm.chapter_id}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify(this.quizForm)
      });
      const data = await res.json();
      if (res.ok) {
        this.fetchQuizzes();
        this.cancelForm();
      } else {
        alert(data.message || 'Error adding quiz');
      }
    },
    editQuiz(quiz) {
      this.quizForm = { ...quiz };
      this.quizForm.single_attempt = Boolean(quiz.single_attempt);
      this.editingQuizId = quiz.id;
      this.showQuizModal = true;
    },
    async updateQuiz() {
      const token = localStorage.getItem('admin_token');
      const res = await fetch(`http://localhost:5000/edit_quiz/${this.editingQuizId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify(this.quizForm)
      });
      const data = await res.json();
      if (res.ok) {
        this.fetchQuizzes();
        this.cancelForm();
      } else {
        alert(data.message || 'Error updating quiz');
      }
    },
    async deleteQuiz(id) {
      if (!confirm('Are you sure you want to delete this quiz?')) return;
      const token = localStorage.getItem('admin_token');
      const res = await fetch(`http://localhost:5000/delete_quiz/${id}`, {
        method: 'DELETE',
        headers: { Authorization: `Bearer ${token}` }
      });
      const data = await res.json();
      if (res.ok) {
        this.fetchQuizzes();
      } else {
        alert(data.message || 'Error deleting quiz');
      }
    },
    viewQuiz(quizId) {
      this.$router.push(`/quiz_questions/${quizId}`);
    },
    logout() {
      localStorage.removeItem('admin_token');
      this.$router.push('/login');
    }
  },
  mounted() {
    this.fetchQuizzes();
    this.fetchChapters();
  }
};
</script>

<style scoped>
.modal {
  background-color: rgba(0, 0, 0, 0.5);
}
</style>
