<template>
  <div class="container">
    <h2 class="text-left">Chat with AI:</h2>
    <SystemRoleSelector
      v-if="showSystemRoleSelector"
      :disabled="disableRoleChange"
      @update-system-role="updateSystemRole"
      @role-selected="onRoleSelected"
    />
    <h3 v-else>Current Role: {{ currentRole }}</h3>
    <div class="chat-container p-3 bg-light mb-3 overflow-auto">
      <div
        v-for="(message, index) in messages"
        :key="index"
        :class="`message ${message.type} p-2 mb-2 rounded text-white`"
      >
        {{ message.content }}
      </div>
    </div>
    <form @submit.prevent="submitQuestion" class="input-form d-flex mb-3">
      <input
        v-model="question"
        class="form-control me-2"
        placeholder="Type your question here..."
        required
      />
      <button type="submit" class="btn btn-primary">Submit</button>
      <button type="button" @click="resetChat" class="btn btn-secondary ms-2">
        Clear
      </button>
    </form>
  </div>
</template>



<script>
import SystemRoleSelector from "./SystemRoleSelector.vue";
import axios from "axios";

export default {
  computed: {
    disableRoleChange() {
      return this.messages.length > 0;
    },
  },
  components: {
    SystemRoleSelector,
  },
  data() {
    return {
      question: "",
      messages: [],
      currentRole: "Helpful Assistant",
      showSystemRoleSelector: true,
    };
  },
  methods: {
    async submitQuestion() {
      if (this.showSystemRoleSelector) {
        this.onRoleSelected();
      }
  try {
    this.messages.push({ type: "user", content: this.question });

    // 将之前的消息连接为一个字符串，作为新问题的上下文
    const prompt = this.messages
      .map((message, index) => `${index % 2 === 0 ? "User:" : "GPT:"} ${message.content}`)
      .join("\n") + `\nUser: ${this.question}`;

    const { data } = await axios.get("http://localhost:5000/api/gpt-response", {
      params: {
        prompt: prompt,
        systemRole: this.currentRole,
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
      this.showSystemRoleSelector = true;
    },
    updateSystemRole(newRole) {
      this.currentRole = newRole;
    },
    onRoleSelected() {
      this.showSystemRoleSelector = false;
    },
  },
};
</script>



<style scoped>
.chat-container {
  width: 100%;
  height: 400px;
  margin-bottom: 10px;
}

.user {
  background-color: #0d6efd;
  align-self: flex-end;
}

.gpt {
  background-color: #198754;
  align-self: flex-start;
}

.error {
  background-color: #dc3545;
  align-self: flex-start;
}
</style>