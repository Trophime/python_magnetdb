import client from "./client";

export function list({ query, page, perPage, sortBy, sortDesc, status } = {}) {
  return client.get('/api/magnets', {
    params: {
      page,
      query,
      sort_by: sortBy,
      sort_desc: sortDesc,
      per_page: perPage,
      status
    },
  })
    .then((res) => res.data)
}

export function find({ id }) {
  return client.get(`/api/magnets/${id}`)
    .then((res) => res.data)
}

export function create(values) {
  const form = new FormData()
  for (const [key, value] of Object.entries(values)) {
    if (value) {
      form.append(key, value)
    }
  }
  return client.post(`/api/magnets`, form)
    .then((res) => res.data)
}

export function update({ id, ...values }) {
  const form = new FormData()
  for (const [key, value] of Object.entries(values)) {
    if (value) {
      form.append(key, value)
    }
  }
  return client.patch(`/api/magnets/${id}`, form)
    .then((res) => res.data)
}

export function addPart({ magnetId, partId }) {
  const form = new FormData()
  form.append('part_id', partId)
  return client.post(`/api/magnets/${magnetId}/parts`, form)
    .then((res) => res.data)
}

export function defunct({ magnetId }) {
  return client.post(`/api/magnets/${magnetId}/defunct`)
    .then((res) => res.data)
}
