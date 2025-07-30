<template>
  <div class="container mt-5">
    <h2 class="text-center text-primary mb-4">Admin Summary Dashboard</h2>

    <div class="text-center mb-4">
      <router-link to="/admin" class="btn btn-outline-primary">
        ← Back to Admin Dashboard
      </router-link>
    </div>

    <div v-if="loading" class="text-center text-muted">Loading summary...</div>
    <div v-else>
      <div class="row">
        <div class="col-md-6 mb-4">
          <h5 class="text-center text-success">Quiz Attempts per Subject</h5>
          <canvas ref="pieChart"></canvas>
        </div>

        <div class="col-md-6 mb-4">
          <h5 class="text-center text-info">Top Scores by Users</h5>
          <canvas ref="barChart"></canvas>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Chart, registerables } from "chart.js"; 
Chart.register(...registerables);  

export default {
  name: "Eraf_AdminSummary",
  data() {
    return {
      loading: true,
      pieChart: null,
      barChart: null,
    };
  },
  methods: {
   async fetchSummary() {
        const token = localStorage.getItem("admin_token");

        try {
            const res = await fetch("http://127.0.0.1:5000/admin_summary", {
            headers: {
                Authorization: `Bearer ${token}`,
            },
            });

            if (!res.ok) throw new Error("Failed to fetch summary data");

            const data = await res.json();

            this.loading = false;

            this.$nextTick(() => {  
            this.renderCharts(data);
            });

        } catch (err) {
            alert("Error loading admin summary: " + err.message);
            this.loading = false; 
        }
    },
    renderCharts(data) {
        this.$nextTick(() => {
            if (this.pieChart) this.pieChart.destroy();
            if (this.barChart) this.barChart.destroy();

            const pieCtx = this.$refs.pieChart.getContext("2d");
            this.pieChart = new Chart(pieCtx, {
            type: "pie",
            data: {
                labels: data.pie_chart_data.labels,
                datasets: [
                {
                    data: data.pie_chart_data.values,
                    backgroundColor: [
                    "#007bff", // Blue
                    "#28a745", // Green
                    "#ffc107", //   Yellow
                    "#dc3545", // Red
                    "#6610f2", // Purple
                    "#17a2b8", // Teal
                    ],
                },
                ],
            },
            options: {
                responsive: true,
            },
            });

            const barCtx = this.$refs.barChart.getContext("2d"); 
            this.barChart = new Chart(barCtx, {
            type: "bar",
            data: {
                labels: data.bar_chart_data.labels,
                datasets: [
                {
                    label: "Top Scores",
                    data: data.bar_chart_data.values,
                    backgroundColor: "#17a2b8",
                },
                ],
            },
            options: {
                responsive: true,
                scales: {
                y: {
                    beginAtZero: true,
                    title: {
                    display: true,
                    text: "Score",
                    },
                },
                },
            },
            });
        });
    }

  },
  mounted() {
    this.fetchSummary();
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
