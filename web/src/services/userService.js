import client from "./client";

export function find() {
  return client.get('/api/user').then((res) => res.data)
}

export function update(values) {
  const form = new FormData()
  for (const [key, value] of Object.entries(values)) {
    if (value) {
      form.append(key, value)
    }
  }
  return client.patch('/api/user', form).then((res) => res.data)
}
