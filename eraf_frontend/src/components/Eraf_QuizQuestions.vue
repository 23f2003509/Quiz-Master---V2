<template>
  <div class="container mt-4">
    <div class="mb-3">
      <button class="btn btn-outline-secondary" @click="$router.go(-1)">
        ← Back
      </button>
    </div>

    <h2 class="text-center mb-4">Questions for Quiz ID: {{ quizId }}</h2>

    <div class="card p-3 mb-4">
      <h4 class="mb-3">Add New Question</h4>
      <form @submit.prevent="addQuestion">
        <div class="mb-2">
          <input v-model="newQuestion.question_tag" class="form-control" placeholder="Question Tag" required />
        </div>
        <div class="mb-2">
          <textarea v-model="newQuestion.question_statement" class="form-control" placeholder="Question Statement" required></textarea>
        </div>
        <div class="mb-2">
          <input v-model="newQuestion.option1" class="form-control" placeholder="Option 1" required />
          <input v-model="newQuestion.option2" class="form-control mt-2" placeholder="Option 2" required />
          <input v-model="newQuestion.option3" class="form-control mt-2" placeholder="Option 3" required />
          <input v-model="newQuestion.option4" class="form-control mt-2" placeholder="Option 4" required />
        </div>
        <div class="mb-2">
          <input v-model="newQuestion.correct_answer" class="form-control" placeholder="Exact Correct Answer" required />
        </div>
        <button class="btn btn-success mt-2" type="submit">Add Question</button>
      </form>
    </div>

    <div class="card p-3">
      <h4 class="mb-3">All Questions</h4>
      <table class="table table-bordered table-striped">
        <thead class="table-dark">
          <tr>
            <th>ID</th>
            <th>Tag</th>
            <th>Statement</th>
            <th>Options</th>
            <th>Correct</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="q in questions" :key="q.id">
            <td>{{ q.id }}</td>
            <td>{{ q.question_tag }}</td>
            <td>{{ q.question_statement }}</td>
            <td>
              <ul class="mb-0">
                <li>1. {{ q.option1 }}</li>
                <li>2. {{ q.option2 }}</li>
                <li>3. {{ q.option3 }}</li>
                <li>4. {{ q.option4 }}</li>
              </ul>
            </td>
            <td>{{ q.correct_answer }}</td>
            <td>
              <button class="btn btn-sm btn-warning me-2" @click="startEdit(q)">Edit</button>
              <button class="btn btn-sm btn-danger" @click="deleteQuestion(q.id)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="editMode" class="card p-3 mt-4 bg-light">
      <h4 class="mb-3">Edit Question</h4>
      <form @submit.prevent="updateQuestion">
        <div class="mb-2">
          <input v-model="editQuestion.question_tag" class="form-control" placeholder="Question Tag" required />
        </div>
        <div class="mb-2">
          <textarea v-model="editQuestion.question_statement" class="form-control" placeholder="Question Statement" required></textarea>
        </div>
        <div class="mb-2">
          <input v-model="editQuestion.option1" class="form-control" placeholder="Option 1" required />
          <input v-model="editQuestion.option2" class="form-control mt-2" placeholder="Option 2" required />
          <input v-model="editQuestion.option3" class="form-control mt-2" placeholder="Option 3" required />
          <input v-model="editQuestion.option4" class="form-control mt-2" placeholder="Option 4" required />
        </div>
        <div class="mb-2">
          <input v-model="editQuestion.correct_answer" class="form-control" placeholder="Correct Answer" required />
        </div>
        <button class="btn btn-primary me-2" type="submit">Save</button>
        <button class="btn btn-secondary" @click="cancelEdit">Cancel</button>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: "Eraf_QuizQuestions",
  data() {
    return {
      quizId: this.$route.params.quizId,
      questions: [],

      newQuestion: {
        question_tag: "",
        question_statement: "",
        option1: "",
        option2: "",
        option3: "",
        option4: "",
        correct_answer: "",
      },

      editQuestion: null, 
      editMode: false,
    };
  },
  methods: {
    async fetchQuestions() {
      const token = localStorage.getItem("admin_token");
      const response = await fetch(`http://localhost:5000/add_question/${this.quizId}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      const data = await response.json();
      this.questions = data;
      console.log(this.questions);
    },


    async addQuestion() {
      const token = localStorage.getItem("admin_token");
      const response = await fetch(`http://localhost:5000/add_question/${this.quizId}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(this.newQuestion),
      });
      const result = await response.json();
      if (response.ok) {
        alert(result.message);
        this.newQuestion = {
          question_tag: "",
          question_statement: "",
          option1: "",
          option2: "",
          option3: "",
          option4: "",
          correct_answer: "",
        };
        this.fetchQuestions();
      } else {
        alert(result.message);
      }
    },
    startEdit(q) {
      this.editMode = true;
      this.editQuestion = { ...q }; 
    },
    async updateQuestion() {
      const token = localStorage.getItem("admin_token");
      const response = await fetch(`http://localhost:5000/edit_question/${this.editQuestion.id}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(this.editQuestion),
      });
      const result = await response.json();
      if (response.ok) {
        alert(result.message);
        this.cancelEdit();
        this.fetchQuestions();
      } else {
        alert(result.message);
      }
    },
    async deleteQuestion(questionId) {
      const token = localStorage.getItem("admin_token");
      const response = await fetch(`http://localhost:5000/delete_question/${questionId}`, {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      const result = await response.json();
      if (response.ok) {
        alert(result.message);
        this.fetchQuestions();
      } else {
        alert(result.message);
      }
    },
    cancelEdit() {
      this.editMode = false;
      this.editQuestion = null;
    },
  },
  mounted() {
    this.fetchQuestions();
  },
};
</script>

<style scoped>
textarea {
  resize: vertical;
}
</style>
