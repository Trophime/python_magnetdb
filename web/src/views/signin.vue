<template>
  <div class="mx-auto w-full max-w-sm">
    <div class="display-1 text-center mb-6">
      Sign in to MagnetDB
    </div>

    <Card>
      <Alert v-if="error" :error="error" class="alert alert-danger" />
      <div v-else class="display-2 text-center">
        {{ $route.query.code ? 'Loading' : 'Redirecting' }}...
      </div>
    </Card>
  </div>
</template>

<script>
import * as sessionService from '@/services/sessionService'
import Card from '@/components/Card'
import Alert from "@/components/Alert";

export default {
  name: 'SignIn',
  components: {
    Alert,
    Card,
  },
  data() {
    return {
      error: null,
    }
  },
  async mounted() {
    try {
      const redirectUri = `${window.location.origin}/sign_in`
      if (this.$route.query.code) {
        const res = await sessionService.create({
          code: this.$route.query.code,
          redirect_uri: redirectUri,
        })
        this.$store.commit('setToken', res.token)
        this.$router.push('/')
        return
      }

      const res = await sessionService.getAuthorizationUrl({ redirect_uri: redirectUri })
      window.location.href = res.url
    } catch (error) {
      this.error = error
    }
  },
}
</script>
