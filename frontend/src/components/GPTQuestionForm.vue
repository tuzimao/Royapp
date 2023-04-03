<template>
  <div class="gpt-chat">
    <h2>Chat with AI:</h2>
    <div class="chat-container">
      <div v-for="(message, index) in messages" :key="index" :class="`message ${message.type}`">
        {{ message.content }}
      </div>
    </div>
    <form @submit.prevent="submitQuestion" class="input-form">
      <input v-model="question" placeholder="Type your question here..." required />
      <button type="submit">Submit</button>
      <button type="button" @click="resetChat" class="reset">Clear</button>
    </form>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      question: "",
      messages: [],
    };
  },
  methods: {
    async submitQuestion() {
      try {
        this.messages.push({ type: "user", content: this.question });

        const prompt = this.messages
          .map((message, index) => `${index % 2 === 0 ? "User:" : "GPT:"} ${message.content}`)
          .join("\n") + `\nUser: ${this.question}`;

        const { data } = await axios.get("http://localhost:5000/api/gpt-response", {
          params: {
            prompt: prompt,
          },
        });
        this.messages.push({ type: "gpt", content: data.gpt_response });

        this.question = "";
      } catch (error) {
        console.error("Error fetching GPT response:", error);
        this.messages.push({ type: "error", content: "An error occurred while fetching the response." });
      }
    },
    resetChat() {
      this.messages = [];
    },
  },
};
</script>


<style scoped>
.gpt-chat {
  display: flex;
  flex-direction: column;
  align-items: center;
  font-family: Arial, sans-serif;
}

h2 {
  color: #2c3e50;
  margin-bottom: 20px;
}

.chat-container {
  background-color: #f0f0f0;
  padding: 10px;
  width: 100%;
  max-width: 600px;
  height: 400px;
  overflow-y: scroll;
  margin-bottom: 10px;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.message {
  padding: 8px 10px;
  margin-bottom: 8px;
  border-radius: 5px;
  max-width: 100%;
  word-wrap: break-word;
}

.user {
  background-color: #3498db;
  color: #ffffff;
  align-self: flex-end;
}

.gpt {
  background-color: #2ecc71;
  color: #ffffff;
  align-self: flex-start;
}

.error {
  background-color: #e74c3c;
  color: #ffffff;
  align-self: flex-start;
}

.input-form {
  display: flex;
  justify-content: space-between;
  width: 100%;
  max-width: 600px;
}

input {
  padding: 8px;
  flex-grow: 1;
  margin-right: 10px;
  border-radius: 5px;
  border: 1px solid #bdc3c7;
}

button {
  background-color: #3498db;
  color: #ffffff;
  padding: 8px 12px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #2980b9;
}

button.reset {
  background-color: #3498db;
  margin-left: 10px;
}

button.reset:hover {
  background-color: #2980b9;
}
</style>