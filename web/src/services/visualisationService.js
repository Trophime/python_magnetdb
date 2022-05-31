import client from "./client";

export function bmap(params) {
  return client.post('/api/visualisations/bmap', params)
    .then((res) => res.data)
}
