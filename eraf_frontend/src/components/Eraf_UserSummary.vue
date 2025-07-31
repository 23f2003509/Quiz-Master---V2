<template>
  <div class="container mt-5">
    <h2 class="text-center text-primary mb-4">📊 Your Quiz Summary</h2>
    <div class="text-center mb-4">
      <router-link to="/user" class="btn btn-outline-primary">
        ← Back to Dashboard
      </router-link>
    </div>

    <div class="text-center mb-3">
      <p class="text-muted">Here's a summary of your quiz performance:</p>
      <button @click="exportToCSV" class="btn btn-outline-success">
        Download Summary as CSV
      </button>
    </div>

    <div class="row mb-5">
      <div class="col-md-6 mb-4">
        <h5 class="text-center text-success">Quizzes per Subject</h5>
        <canvas ref="pieChart"></canvas>
      </div>

      <div class="col-md-6 mb-4">
        <h5 class="text-center text-info">Scores per Quiz</h5>
        <canvas ref="barChart"></canvas>
      </div>
    </div>

    <table class="table table-bordered table-hover">
      <thead class="table-dark">
        <tr>
          <th>S.No</th>
          <th>Quiz Name</th>
          <th>Subject</th>
          <th>Chapter</th>
          <th>Score</th>
          <th>Total</th>
          <th>Percentage</th>
          <th>Date</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(score, index) in scores" :key="index">
          <td>{{ index + 1 }}</td>
          <td>{{ score.quiz_name }}</td>
          <td>{{ score.subject_name }}</td>
          <td>{{ score.chapter_name }}</td>
          <td>{{ score.score }}</td>
          <td>{{ score.total_score }}</td>
          <td>{{ score.percentage_score.toFixed(2) }}%</td>
          <td>{{ new Date(score.timestamp).toLocaleString() }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import { Chart, registerables } from "chart.js";
Chart.register(...registerables);

export default {
  name: "Eraf_UserSummary",
  data() {
    return {
      scores: [],
      pieChart: null,
      barChart: null,
    };
  },
  methods: {
    async fetchScores() {
      const token = localStorage.getItem("user_token");
      const res = await fetch("http://127.0.0.1:5000/get_scores", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (res.ok) {
        this.scores = await res.json();
        this.$nextTick(() => {
          this.renderCharts();
        });
      } else {
        alert("Failed to load scores");
      }
    },

    async exportToCSV() {
      const token = localStorage.getItem("user_token");
      const res = await fetch("http://127.0.0.1:5000/export_details", {
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (res.ok) {
        alert("Your report is being prepared and will be emailed shortly.");
      } else {
        alert("Failed to trigger email export.");
      }
    },

    renderCharts() {
      if (this.pieChart) this.pieChart.destroy();
      if (this.barChart) this.barChart.destroy();

      const subjectCounts = {};
      this.scores.forEach((s) => {
        subjectCounts[s.subject_name] = (subjectCounts[s.subject_name] || 0) + 1;
      });

      const pieCtx = this.$refs.pieChart.getContext("2d");
      this.pieChart = new Chart(pieCtx, {
        type: "pie",
        data: {
          labels: Object.keys(subjectCounts),
          datasets: [
            {
              data: Object.values(subjectCounts),
              backgroundColor: [
                "#007bff", "#28a745", "#ffc107", "#dc3545", "#6610f2", "#17a2b8",
              ],
            },
          ],
        },
        options: {
          responsive: true,
        },
      });

      // Prepare bar chart
      const quizScores = {};
      this.scores.forEach((s) => {
        quizScores[s.quiz_name] = parseFloat(s.percentage_score.toFixed(2));
      });

      const barLabels = Object.keys(quizScores).sort();
      const barValues = barLabels.map(label => quizScores[label]);

      const dynamicColors = barLabels.map((_, i) => {
        const colorList = ["#17a2b8", "#ffc107", "#007bff", "#28a745", "#dc3545", "#6610f2"];
        return colorList[i % colorList.length];
      });

      const barCtx = this.$refs.barChart.getContext("2d");
      this.barChart = new Chart(barCtx, {
        type: "bar",
        data: {
          labels: barLabels,
          datasets: [
            {
              label: "Percentage Score",
              data: barValues,
              backgroundColor: dynamicColors,
            },
          ],
        },
        options: {
          responsive: true,
          scales: {
            y: {
              beginAtZero: true,
              max: 100,
              title: {
                display: true,
                text: "Percentage (%)",
              },
            },
          },
        },
      });
    },
  },
  mounted() {
    this.fetchScores();
  },
};
</script>

<style scoped>
.container {
  max-width: 1000px;
}
canvas {
  background: #fff;
  padding: 10px;
  border-radius: 10px;
  box-shadow: 0 0 8px rgba(0, 0, 0, 0.1);
}
</style>
