<template>
  <div class="container py-5">
    <div>
         <!-- Navbar -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
      <div class="container-fluid">
        <router-link class="navbar-brand fw-bold" to="/">QuizMaster Admin</router-link>

        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNav"
        >
          <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav me-auto">
            <li class="nav-item">
              <router-link class="nav-link" to="/admin">Dashboard</router-link>
            </li>
          </ul>
          <ul class="navbar-nav ms-auto">
            <li class="nav-item">
              <router-link class="nav-link" to="/profile">Profile</router-link>
            </li>
            <li class="nav-item">
                <router-link class="nav-link" to="/">Logout</router-link>
            </li>
          </ul>
        </div>
      </div>
    </nav>
    </div>
    <!-- Header -->
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2 class="fw-bold">Manage Subjects</h2>
      <input
        type="text"
        class="form-control w-25 ms-3"
        v-model="searchQuery"
        placeholder="Search subjects..."
        >
      <button class="btn btn-success" @click="showAddSubjectModal = true">
        <i class="bi bi-plus-circle"></i> Add Subject
      </button>
        

    </div>

    <!-- Subject Cards -->
    <div v-if="subjects.length" class="row g-4">
        <div class="col-md-6" v-for="subject in filteredSubjects" :key="subject.id">
            <div class="card shadow-lg rounded-4 border-0">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-start mb-2">
                    <div>
                        <h5 class="fw-bold mb-1 text-capitalize">{{ subject.name }}</h5>
                        <p class="text-muted small mb-0" v-if="subject.description">{{ subject.description }}</p>
                    </div>
                    <div>
                        <button class="btn btn-sm btn-outline-primary me-1 rounded-pill px-3" @click="editSubject(subject)">
                        <i class="bi bi-pencil"></i> Edit
                        </button>
                        <button class="btn btn-sm btn-outline-danger rounded-pill px-3" @click="deleteSubject(subject.id)">
                        <i class="bi bi-trash"></i> Delete
                        </button>
                    </div>
                    </div>

                    <!-- Chapters -->
                    <div v-if="subject.chapters.length">
                    <div v-for="chapter in subject.chapters" :key="chapter.id" class="bg-light rounded-3 px-3 py-2 mb-2 d-flex justify-content-between align-items-center">
                        <div>
                            <h5 class="fw-semibold text-dark">{{ chapter.name }}</h5>
                            <p class="text-muted small">{{ chapter.description }}</p>
                        </div>
                        <div>
                        <button class="btn btn-sm btn-outline-secondary me-1 rounded-pill" @click="editChapter(chapter, subject.id)">
                            Edit
                        </button>
                        <button class="btn btn-sm btn-outline-danger rounded-pill" @click="deleteChapter(chapter.id)">
                            Delete
                        </button>
                        </div>
                    </div>
                    </div>

                    <!-- Add Chapter Button -->
                    <button class="btn btn-outline-success w-100 mt-3 rounded-pill fw-semibold" @click="addChapter(subject.id)">
                    <i class="bi bi-plus-circle"></i> Add Chapter
                    </button>
                </div>
            </div>
        </div>
    </div>


    <div v-else class="text-center text-muted mt-5">No subjects found.</div>

    <!-- Add/Edit Subject Modal -->
        <div v-if="showAddSubjectModal" class="modal d-block" tabindex="-1">
        <div class="modal-dialog">
            <div class="modal-content">
            <!-- Header -->
            <div class="modal-header">
                <h5 class="modal-title">
                {{ editingSubjectId ? 'Edit Subject' : 'Add Subject' }}
                </h5>
                <button type="button" class="btn-close" @click="cancelSubjectForm"></button>
            </div>

            <!-- Body -->
            <div class="modal-body">
                <input
                v-model="newSubject"
                class="form-control"
                placeholder="Enter subject name"
                />
                <input
                type="text"
                v-model="newSubjectDescription"
                class="form-control mt-2"
                placeholder="Enter subject description"
                />
            </div>

            <!-- Footer -->
            <div class="modal-footer">
                <button class="btn btn-secondary" @click="cancelSubjectForm">Cancel</button>
                <button
                class="btn btn-primary"
                @click="editingSubjectId ? updateSubject() : submitSubject()"
                >
                {{ editingSubjectId ? 'Update' : 'Add' }}
                </button>
            </div>
            </div>
        </div>
        </div>



    <!-- Add/Edit Chapter Modal -->
    <div v-if="showChapterModal" class="modal d-block" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ editingChapter ? 'Edit' : 'Add' }} Chapter</h5>
            <button type="button" class="btn-close" @click="showChapterModal = false"></button>
          </div>
          <div class="modal-body">
            <input v-model="chapterName" class="form-control" placeholder="Enter chapter name">
            <input type="text" v-model="chapterDescription" class="form-control mt-2" placeholder="Enter chapter description">
          </div>
          <div class="modal-footer">
            <button class="btn btn-secondary" @click="showChapterModal = false">Cancel</button>
            <button class="btn btn-primary" @click="submitChapter">Save</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Eraf_ManageSubject',
  data() {
    return {
      subjects: [],
      showAddSubjectModal: false,
      newSubject: '',
      newSubjectDescription: '',
      editingSubjectId: null,

      showChapterModal: false,
      chapterName: '',
      chapterDescription: '',
      editingChapter: null,
      currentSubjectId: null,

      searchQuery: ''

    }
  },
  methods: {
    async fetchSubjects() {
      const token= localStorage.getItem('admin_token');
      const res = await fetch('http://localhost:5000/subject', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        }
      })
      if (!res.ok) {
        throw new Error('Failed to fetch subjects')
      }
      const data = await res.json()
    //   console.log(data)
      this.subjects = data || []
      console.log(this.subjects)    
    },
    editSubject(subject) {
            this.newSubject = subject.name;
            this.newSubjectDescription = subject.description;
            this.editingSubjectId = subject.id;
            this.showAddSubjectModal = true;
            },

    cancelSubjectForm() {
            this.newSubject = '';
            this.newSubjectDescription = '';
            this.editingSubjectId = null;
            this.showAddSubjectModal = false;
            },

    async submitSubject() {
            const token = localStorage.getItem('admin_token');

            const res = await fetch('http://localhost:5000/subject', {
                method: 'POST',
                headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                name: this.newSubject,
                description: this.newSubjectDescription
                })
            });

            const data = await res.json();
            if (res.ok) {
                this.fetchSubjects();
                this.cancelSubjectForm();
            } else {
                alert(data.message || 'Failed to add subject');
            }
    },
    async updateSubject() {
            const token = localStorage.getItem('admin_token');
            const res = await fetch('http://localhost:5000/subject', {
                method: 'PUT',
                headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                subject_id: this.editingSubjectId,
                name: this.newSubject,
                description: this.newSubjectDescription
                })
            });

            const data = await res.json();
            if (res.ok) {
                this.fetchSubjects();
                this.cancelSubjectForm();
            } else {
                alert(data.message || 'Failed to update subject');
            }
            },

    
    async deleteSubject(subjectId) {
            const token = localStorage.getItem('admin_token');
            if (confirm("Are you sure you want to delete this subject?")) {
            try {
                const res = await fetch('http://localhost:5000/subject', {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({ subject_id: subjectId })
                });

                const data = await res.json();
                if (res.ok) {
                this.fetchSubjects();
                } else {
                alert(data.message || 'Failed to delete subject');
                }
            } catch (err) {
                console.error('Error deleting subject:', err);
                alert('Server error while deleting subject.');
            }
        } else {
            alert('Subject deletion canceled.');
        }
    },


    ///////////////////////subject part done here ///////////////////////////////////////







    addChapter(subjectId) {
      this.chapterName = ''
      this.chapterDescription = ''
      this.editingChapter = null
      this.currentSubjectId = subjectId
      this.showChapterModal = true
    },

    editChapter(chapter, subjectId) {
      this.chapterName = chapter.name
      this.chapterDescription = chapter.description
      this.editingChapter = chapter.id
      this.currentSubjectId = subjectId
      this.showChapterModal = true
    },

    async submitChapter() {
      if (this.editingChapter) {
        const token = localStorage.getItem('admin_token');
        await fetch(`http://localhost:5000/edit_chapter/${this.editingChapter}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
          body: JSON.stringify({ name: this.chapterName, description: this.chapterDescription })
        })
      } else {
        const token = localStorage.getItem('admin_token');
        await fetch(`http://localhost:5000/add_chapter/${this.currentSubjectId}`, {
            
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
          body: JSON.stringify({ name: this.chapterName, description: this.chapterDescription })
        })
      }
      this.showChapterModal = false
      this.fetchSubjects()
    },

    async deleteChapter(chapId) {
      const token = localStorage.getItem('admin_token'); 
      if (confirm("Are you sure you want to delete this chapter?")) {
        await fetch(`http://localhost:5000/delete_chapter/${chapId}`, {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` }
      })
      this.fetchSubjects()
      } else {
          return
      }

    }
  },
  computed: {
  filteredSubjects() {
    // If search box is empty, show all subjects
    if (this.searchQuery === '') {
      return this.subjects;
    }

    // Convert the search text to lowercase
    const searchLower = this.searchQuery.toLowerCase();

    // Create a new list with only matching subjects
    const result = [];

    for (let i = 0; i < this.subjects.length; i++) {
    const subjectName = this.subjects[i].name.toLowerCase();
    if (subjectName.includes(searchLower)) {
        result.push(this.subjects[i]);
    }
    }

    // Return the matching subjects
    return result;
        }
    },

  mounted() {
    this.fetchSubjects()
  }
}
</script>

<style scoped>
.modal {
  background-color: rgba(0, 0, 0, 0.5);
}
.card-title {
  font-weight: 600;
}
.list-group-item {
  font-size: 0.95rem;
}
</style>
