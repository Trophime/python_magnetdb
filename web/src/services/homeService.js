import client from "./client";

export function find() {
  return client.get('/api/home').then((res) => res.data)
}
