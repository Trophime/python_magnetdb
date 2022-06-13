import client from "./client";

export function list({ query, page, perPage, sortBy, sortDesc } = {}) {
  return client.get('/api/materials', {
    params: {
      page,
      query,
      sort_by: sortBy,
      sort_desc: sortDesc,
      per_page: perPage,
    },
  })
    .then((res) => res.data)
}

export function find({ id }) {
  return client.get(`/api/materials/${id}`)
    .then((res) => res.data)
}

export function create(values) {
  return client.post(`/api/materials`, values)
    .then((res) => res.data)
}

export function update({ id, ...values }) {
  return client.patch(`/api/materials/${id}`, values)
    .then((res) => res.data)
}

export function destroy({ id }) {
  return client.delete(`/api/materials/${id}`)
    .then((res) => res.data)
}
