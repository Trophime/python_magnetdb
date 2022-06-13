<template>
  <div class="mx-auto w-full max-w-sm">
    <div class="display-1 text-center mb-6">
      Sign in to MagnetDB
    </div>

    <Card>
      <template v-if="$route.query.code">
        <Alert v-if="error" :error="error" class="alert alert-danger" />
        <div v-else class="display-2 text-center">
          Loading...
        </div>
      </template>
      <div v-else class="space-y-4 flex flex-col items-center">
        <Alert v-if="error" :error="error" class="alert alert-danger" />
        <div class="text-center">
          To sign in to MagnetDB, click on the button below
        </div>
        <Button class="btn btn-primary" @click="redirect">
          Sign In
        </Button>
      </div>
    </Card>
  </div>
</template>

<script>
import * as sessionService from '@/services/sessionService'
import Card from '@/components/Card'
import Alert from "@/components/Alert";
import Button from "@/components/Button";

export default {
  name: 'SignIn',
  components: {
    Button,
    Alert,
    Card,
  },
  data() {
    return {
      error: null,
      redirectUri: `${window.location.origin}/sign_in`,
    }
  },
  methods: {
    async redirect() {
      this.error = null
      try {
        const res = await sessionService.getAuthorizationUrl({ redirect_uri: this.redirectUri })
        window.location.href = res.url
      } catch (error) {
        this.error = error
      }
    }
  },
  async mounted() {
    if (!this.$route.query.code) {
      return
    }

    try {
      const res = await sessionService.create({
        code: this.$route.query.code,
        redirect_uri: this.redirectUri,
      })
      this.$store.commit('setToken', res.token)
      this.$router.push('/')
    } catch (error) {
      this.error = error
    }
  },
}
</script>
