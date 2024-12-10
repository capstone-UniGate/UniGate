<script setup lang="ts">
import { ref, onMounted } from "vue";

const userInfo = ref();
const isLoading = ref(false);
const isError = ref(false);

async function loadUserInfo() {
  try {
    isError.value = false;
    isLoading.value = true;
    //TODO
    userInfo.value = await fetch("").then((res) => {
      if (!res.ok) {
        throw new Error("Failed to fetch user info");
      }
      return res.json();
    });
  } catch (error) {
    isError.value = true;
  } finally {
    isLoading.value = false;
  }
}

onMounted(() => {
  loadUserInfo();
});
</script>

<template>
  <div class="p-4">
    <!-- Error Message -->
    <div v-if="isError" class="text-red-500">
      An error occurred.
      <button @click="loadUserInfo" class="text-blue-500 underline">
        Retry
      </button>
    </div>

    <div v-if="isLoading" class="text-gray-500">Loading user info...</div>

    <!-- Welcome Message -->
    <div v-if="!isLoading && !isError">
      <h2 class="text-xl font-bold">
        Welcome, {{ userInfo?.name || "Guest" }}!
      </h2>
    </div>
  </div>
</template>
