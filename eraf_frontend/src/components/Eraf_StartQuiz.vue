<template>
  <div class="container mt-5 bg-light p-4 rounded shadow">
    <div>
      <router-link to="/user" class="btn btn-outline-primary">
        <i class="bi bi-arrow-left"></i> Back to Quizzes
      </router-link>
    </div>
    <div class="d-flex justify-content-between align-items-center mb-3">
      <h2 class="text-primary text-center w-100">
        Quiz: {{ quiz.name }}
      </h2>
      <span class="badge bg-warning text-dark fs-5 ms-3">
        {{ formattedTime }}
      </span>
    </div>

    <p class="text-center">{{ quiz.description }}</p>

    <form @submit.prevent="submitQuiz" v-if="!result && quiz.questions.length > 0">
      <div
        v-for="(q, index) in quiz.questions"
        :key="q.id"
        class="card p-3 mb-3 border-left border-primary"
      >
        <p><strong>Q{{ index + 1 }}:</strong> {{ q.question_statement }}</p>
        <div v-for="n in 4" :key="n" class="form-check">
          <input
            class="form-check-input"
            type="radio"
            :name="'question_' + q.id"
            :value="q['option' + n]"
            v-model="answers['question_' + q.id]"
            :disabled="isSubmitted"
          />
          <label class="form-check-label">
            {{ q['option' + n] }}
          </label>
        </div>
      </div>
      <button type="submit" class="btn btn-success" :disabled="isSubmitted">
        Submit Quiz
      </button>
    </form>

    <div
      class="modal fade show"
      tabindex="-1"
      style="display: block"
      v-if="result && showResultModal"
    >
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header bg-success text-white">
            <h5 class="modal-title">Quiz Completed!</h5>
          </div>
          <div class="modal-body">
            <p><strong>Score:</strong> {{ result.score }} / {{ result.total_score }}</p>
            <p><strong>Percentage:</strong> {{ result.percentage_score.toFixed(2) }}%</p>
          </div>
          <div class="modal-footer">
            <button class="btn btn-primary" @click="redirectToDashboard">
              Go to Dashboard
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Eraf_StartQuiz",
  data() {
    return {
      quiz: {
        questions: [],
      },
      answers: {},
      result: null,
      timeLeft: 0, 
      timerInterval: null,
      isSubmitted: false,
      showResultModal: false,
    };
  },
  computed: {
    formattedTime() {
      const minutes = Math.floor(this.timeLeft / 60).toString().padStart(2, "0");
      const seconds = (this.timeLeft % 60).toString().padStart(2, "0");
      return `${minutes}:${seconds}`;
    },
  },
  methods: {
    async fetchQuiz() {
      const token = localStorage.getItem("user_token");
      const quizId = this.$route.params.quizId;
      const res = await fetch(`http://127.0.0.1:5000/start_quiz/${quizId}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      
      if (res.ok) {
        const data = await res.json();
        this.quiz = data;
        this.timeLeft = data.duration * 60; 
        this.startTimer();
      } else {
        
        alert("Failed to load quiz dont add question");
      }
    },
    startTimer() {
      this.timerInterval = setInterval(() => {
        if (this.timeLeft > 0) {
          this.timeLeft--;
        } else {
          clearInterval(this.timerInterval);
          this.submitQuiz(); 
        }
      }, 1000);
    },
    async submitQuiz() {
      clearInterval(this.timerInterval);
      if (this.isSubmitted) return;
      this.isSubmitted = true;

      const token = localStorage.getItem("user_token");
      const quizId = this.$route.params.quizId;

      const res = await fetch(`http://127.0.0.1:5000/start_quiz/${quizId}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(this.answers),
      });

      if (res.ok) {
        this.result = await res.json();
        this.showResultModal = true;
      } else {
        alert("Submission failed");
      }
    },
    redirectToDashboard() {
      this.$router.push("/user");
    },
  },
  mounted() {
    this.fetchQuiz();
  },
  beforeUnmount() {
    clearInterval(this.timerInterval);
  },
};
</script>

<style scoped>
.container {
  max-width: 800px;
  background-color: #ffffff;
}
.modal {
  background: rgba(0, 0, 0, 0.6);
}
</style>
