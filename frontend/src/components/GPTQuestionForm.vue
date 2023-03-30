<template>
    <div class="gpt-question-form">
      <h2>Ask a question:</h2>
      <form @submit.prevent="submitQuestion">
        <input v-model="question" placeholder="Type your question here..." required />
        <button type="submit">Submit</button>
      </form>
      <p v-if="response">{{ response }}</p>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  
  export default {
    data() {
      return {
        question: "",
        response: "",
      };
    },
    methods: {
      async submitQuestion() {
        try {
          const { data } = await axios.get("http://localhost:5000/api/gpt-response", {
            params: {
              prompt: this.question,
            },
          });
          this.response = data.gpt_response;
        } catch (error) {
          console.error("Error fetching GPT response:", error);
          this.response = "An error occurred while fetching the response.";
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .gpt-question-form {
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  
  input {
    padding: 5px;
    width: 100%;
    max-width: 600px;
    margin-bottom: 10px;
  }
  </style>
  