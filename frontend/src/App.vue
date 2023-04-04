<template>
  <div id="app">
    <GPTQuestionForm />
  </div>
</template>

<script>
import GPTQuestionForm from "./components/GPTQuestionForm.vue";

export default {
  name: "App",
  components: {
    GPTQuestionForm,
  },
};
</script>


<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  margin-top: 60px;
}
</style>