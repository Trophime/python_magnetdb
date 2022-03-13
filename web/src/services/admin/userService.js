import client from "../client";

export function list({ query, page, perPage, sortBy, sortDesc } = {}) {
  return client.get('/api/admin/users', {
    params: {
      page,
      query,
      sort_by: sortBy,
      sort_desc: sortDesc,
      per_page: perPage,
    },
  }).then((res) => res.data)
}

export function find({ id }) {
  return client.get(`/api/admin/users/${id}`).then((res) => res.data)
}

export function update({ id, ...values }) {
  const form = new FormData()
  for (const [key, value] of Object.entries(values)) {
    if (value) {
      form.append(key, value)
    }
  }
  return client.patch(`/api/admin/users/${id}`, form).then((res) => res.data)
}
