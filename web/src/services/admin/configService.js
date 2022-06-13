import client from "../client";

export function find() {
  return client.get('/api/admin/config').then((res) => res.data)
}
