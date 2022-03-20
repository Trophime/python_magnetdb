import client from "./client";

export function getAuthorizationUrl(values) {
  const form = new FormData()
  for (const [key, value] of Object.entries(values)) {
    if (value) {
      form.append(key, value)
    }
  }
  return client.post(`/api/sessions/authorization_url`, form)
    .then((res) => res.data)
}

export function create(values) {
  const form = new FormData()
  for (const [key, value] of Object.entries(values)) {
    if (value) {
      form.append(key, value)
    }
  }
  return client.post(`/api/sessions`, form)
    .then((res) => res.data)
}
