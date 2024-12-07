<template>
  <Toaster />
  <!-- Error Message Component -->
  <ErrorMessage v-if="isError" @retry="loadGroup" />

  <!-- Loading Indicator Component -->
  <LoadingIndicator v-if="isLoading" />
  <div v-if="group">
    <!-- Avatar Modal -->
    <div
      v-if="isAvatarModalOpen"
      class="fixed inset-0 flex items-center justify-center bg-gray-900 bg-opacity-50 z-50"
    >
      <div class="bg-white rounded-lg shadow-xl p-6 w-80 text-center relative">
        <!-- Close Button -->
        <button
          @click="closeAvatarModal"
          class="absolute top-3 right-3 text-gray-500 hover:text-gray-700"
        >
          ✖
        </button>
        <!-- Enlarged Avatar -->
        <img
          :src="group.avatar"
          alt="Group Avatar"
          class="w-40 h-40 mx-auto rounded-full mb-4"
        />
        <!-- Group Name -->
        <h2 class="text-lg font-semibold text-gray-800">{{ group.name }}</h2>
      </div>
    </div>

    <div
      class="p-6 md:p-10 flex flex-col lg:flex-row items-center lg:items-start text-center lg:text-left gap-10"
    >
      <!-- Left Side: Group Details or Members -->
      <div class="flex-grow w-full lg:w-2/3">
        <!-- Show members if in the "members" section -->
        <div v-if="isViewingMembers">
          <h1 class="text-2xl font-semibold text-gray-800 mb-6">
            Members of
            <span class="text-primary-600">{{ group.name || "Group" }}</span>
          </h1>
          <ScrollArea
            class="h-[300px] lg:h-[400px] bg-white border border-gray-200 p-4 rounded-lg shadow-sm"
          >
            <ul>
              <li
                v-for="member in group.members"
                :key="member.id"
                class="flex items-center gap-4 mb-4"
              >
                <Avatar class="w-10 h-10">
                  <AvatarImage
                    src="https://via.placeholder.com/50"
                    alt="Member Avatar"
                  />
                  <AvatarFallback>NA</AvatarFallback>
                </Avatar>
                <router-link
                  :to="`/groups/${groupId}`"
                  class="text-gray-700 hover:text-primary-500 font-medium"
                >
                  {{ member.name }}
                </router-link>
              </li>
            </ul>
          </ScrollArea>
        </div>

        <!-- Group Details (if not viewing members) -->
        <div v-else>
          <div
            class="flex items-center gap-4 mb-6 justify-center lg:justify-start"
          >
            <Avatar
              class="cursor-pointer w-20 h-20 rounded-full border border-gray-300 hover:shadow-lg hover:scale-105 transition-all"
              @click="openAvatarModal"
            >
              <AvatarImage
                src="https://github.com/radix-vue.png"
                alt="Group Avatar"
              />
              <AvatarFallback>GN</AvatarFallback>
            </Avatar>
            <div>
              <h1 class="text-3xl font-bold text-gray-800">
                {{ group.name || "Group" }}
              </h1>
              <p class="text-sm text-gray-500 mt-1">Course</p>
            </div>
          </div>

          <div class="mb-6">
            <p class="text-gray-600">
              Number of
              <NuxtLink
                :to="`/groups/${groupId}/members`"
                class="text-blue-500 hover:underline"
              >
                members
              </NuxtLink>
              : <span class="font-semibold">{{ group.members_count }}</span>
            </p>
          </div>

          <div
            v-if="group.is_super_student && group.type == 'Private'"
            class="text-left mb-6"
          >
            <Button
              @click="navigateToRequests"
              class="bg-blue-500 text-white font-semibold py-2 px-4 rounded-lg shadow-lg hover:bg-blue-600 hover:shadow-xl active:scale-95 transition-all"
            >
              Manage Requests
            </Button>
          </div>

          <div class="text-left mb-6">
            <p class="text-sm text-gray-500">Description</p>
            <p
              class="text-gray-700 text-base bg-gray-50 border border-gray-200 rounded-lg p-4"
            >
              {{ group.description || "No description available." }}
            </p>
          </div>

          <div class="text-left mb-6">
            <p class="text-sm text-gray-500">Tags</p>
            <p
              class="text-gray-700 text-base bg-gray-50 border border-gray-200 rounded-lg p-4"
            >
              [tag1], [tag2]
            </p>
          </div>

          <div>
            <div v-if="isLoadingStatus">
              <LoadingIndicator />
            </div>
            <div v-else-if="isErrorStatus">
              <p class="text-red-500">
                Failed to load request status. Please try again.
              </p>
            </div>
            <div v-else>
              <p
                v-if="
                  userRequestStatus && userRequestStatus.includes('PENDING')
                "
              >
                Your request status: <strong>{{ userRequestStatus }}</strong>
              </p>
            </div>
          </div>

          <div class="text-center mt-6">
            <Button
              v-if="group.is_member_of || group.is_super_student"
              @click="leaveGroup"
              class="bg-red-500 text-white font-semibold py-2 px-4 rounded-lg shadow-lg hover:bg-red-600 hover:shadow-xl active:scale-95 transition-all"
              id="leave-group-button"
            >
              Leave Group
            </Button>
            <Button
              v-else-if="group.type != 'Private'"
              @click="joinGroup"
              class="bg-indigo-500 text-white font-semibold py-2 px-4 rounded-lg shadow-lg hover:bg-indigo-600 hover:shadow-xl active:scale-95 transition-all"
              id="join-group-button"
            >
              Join Group
            </Button>

            <Button
              v-else-if="
                userRequestStatus == null ||
                userRequestStatus.includes('REJECTED')
              "
              @click="askToJoinGroup"
              class="bg-yellow-500 text-white font-semibold py-2 px-4 rounded-lg shadow-lg hover:bg-yellow-600 hover:shadow-xl active:scale-95 transition-all"
              id="ask-to-join-button"
            >
              Ask to Join
            </Button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Toaster } from "@/components/ui/toast";
import { useToast } from "@/components/ui/toast/use-toast";
import { computed, ref } from "vue";
import { Button } from "@/components/ui/button";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { ScrollArea } from "@/components/ui/scroll-area";
import { useRoute, useRouter } from "vue-router";

const route = useRoute();
const router = useRouter();
const { toast } = useToast();

const groupId = route.params.id;
const isLoading = ref(false);
const isError = ref(false);
const group = ref();

const isViewingMembers = ref(false);
const isAvatarModalOpen = ref(false);
const studentId = "a00808e8-9447-4fa5-b9cd-87e355032c57";
const userRequestStatus = ref(null);
const isLoadingStatus = ref(true);
const isErrorStatus = ref(false);

async function loadGroup() {
  try {
    isError.value = false;
    isLoading.value = true;
    group.value = await useApiFetch(`/groups/${groupId}`);
  } catch (error) {
    isError.value = true;
  } finally {
    isLoading.value = false;
  }
}

onMounted(() => {
  loadGroup();
  fetchUserRequestStatus();
});

const openAvatarModal = () => {
  isAvatarModalOpen.value = true;
};

const closeAvatarModal = () => {
  isAvatarModalOpen.value = false;
};

const navigateToRequests = () => router.push(`/groups/${groupId}/requests`);

const askToJoinGroup = async () => {
  try {
    const response = await useApiFetch(`/groups/join_private_group`, {
      method: "POST",
      query: {
        student_id: studentId,
        group_id: groupId,
      },
    });

    // Check response string and display the appropriate toast
    if (response === "Join request submitted successfully") {
      toast.toast({
        title: "Joined Group",
        description: response,
      });
    } else {
      toast.toast({
        title: "Join Failed",
        description: response,
        variant: "destructive",
      });
    }
  } catch (error) {
    const errorMessage = extractErrorMessage(error);
    toast.toast({
      title: "Join Failed",
      description: errorMessage,
      variant: "destructive",
    });
  }
};

const joinGroup = async () => {
  try {
    const response = await useApiFetch(`/groups/join_public_group`, {
      method: "POST",
      query: {
        student_id: studentId,
        group_id: groupId,
      },
    });

    // Check response string and display the appropriate toast
    if (response === "Insert successful") {
      toast.toast({
        title: "Joined Group",
        description: response,
      });
    } else {
      toast.toast({
        title: "Join Failed",
        description: response,
        variant: "destructive",
      });
    }
  } catch (error) {
    const errorMessage = extractErrorMessage(error);
    toast.toast({
      title: "Join Failed",
      description: errorMessage,
      variant: "destructive",
    });
  }
};

async function fetchUserRequestStatus() {
  try {
    isLoadingStatus.value = true;
    isErrorStatus.value = false;

    // Fetch the requests
    const requests = await useApiFetch(`/groups/${groupId}/requests`);

    // Find the logged-in user's request
    const userRequest = requests.find(
      (request) => request.student_id === studentId,
    );
    // Update the status if found
    userRequestStatus.value = userRequest ? userRequest.status : null;
    //
  } catch (error) {
    isErrorStatus.value = true;
    toast.toast({
      title: "Error",
      description: "Failed to fetch request status. Please try again.",
    });
  } finally {
    isLoadingStatus.value = false;
  }
}

async function leaveGroup() {
  try {
    isError.value = false;
    isLoading.value = true;
    let string_message = await useApiFetch(`/groups/${groupId}/leave`, {
      method: "POST",
      params: {
        student_id: "24d06a00-d9b4-4e18-b1ff-20501cc762df",
        group_id: groupId,
      },
    });
    console.log(string_message);
    if (string_message === "The student has been removed successfully") {
      toast({
        variant: "success",
        description: "You have left the group",
        duration: 1000,
      });
      setTimeout(() => {
        router.push("/groups");
      }, 1500);
    } else {
      toast({
        variant: "destructive",
        description: string_message,
        duration: 1000,
      });
    }
  } catch (error) {
    toast({
      variant: "destructive",
      description: "You have NOT left the group",
      duration: 1000,
    });
    isError.value = true;
  } finally {
    isLoading.value = false;
  }
}
</script>
