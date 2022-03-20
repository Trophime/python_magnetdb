import client from "../client";

export function list({ query, page, perPage, sortBy, sortDesc } = {}) {
  return client.get('/api/admin/audit_logs', {
    params: {
      page,
      query,
      sort_by: sortBy,
      sort_desc: sortDesc,
      per_page: perPage,
    },
  }).then((res) => res.data)
}
