<template>
  <div class="gpt-chat">
    <h2>Chat with Vancouver Realestate AI:</h2>
    <div class="chat-container">
      <div v-for="(message, index) in messages" :key="index" :class="`message ${message.type}`">
        {{ message.content }}
      </div>
    </div>
    <form @submit.prevent="submitQuestion" class="input-form">
      <input v-model="question" placeholder="Type your question here..." required />
      <button type="submit">Submit</button>
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

    // 将之前的消息连接为一个字符串，作为新问题的上下文
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

  },
};
</script>

<style scoped>
.gpt-chat {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.chat-container {
  background-color: #f0f0f0;
  padding: 10px;
  width: 100%;
  max-width: 600px;
  height: 400px;
  overflow-y: scroll;
  margin-bottom: 10px;
}

.message {
  padding: 5px;
  margin-bottom: 5px;
  border-radius: 5px;
}

.user {
  background-color: #c0c0ff;
  align-self: flex-end;
}

.gpt {
  background-color: #c0ffc0;
  align-self: flex-start;
}

.error {
  background-color: #ffc0c0;
  align-self: flex-start;
}

.input-form {
  display: flex;
  justify-content: space-between;
  width: 100%;
  max-width: 600px;
}

input {
  padding: 5px;
  flex-grow: 1;
  margin-right: 10px;
}
</style>
