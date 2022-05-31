from typing import List

from fastapi import APIRouter, Depends, Form
from pydantic import BaseModel

from ...actions.compute_bmap_chart import compute_bmap_chart, prepare_bmap_chart_params
from ...dependencies import get_user

router = APIRouter()


class BMapPayload(BaseModel):
    i_h: float = None
    i_b: float = None
    i_s: float = None
    n: int = None
    r0: float = None
    z0: float = None
    r: List[float] = None
    z: List[float] = None
    pkey: str = None
    command: str = None


@router.post("/api/visualisations/bmap")
def bmap(payload: BMapPayload, user=Depends(get_user('create'))):
    (i_h, i_b, i_s, n, r0, z0, r, z, pkey, command) = prepare_bmap_chart_params(
        payload.i_h, payload.i_b, payload.i_s, payload.n, payload.r0, payload.z0, payload.r, payload.z,
        payload.pkey, payload.command
    )
    return {
        'params': {
            'i_h': i_h,
            'i_b': i_b,
            'i_s': i_s,
            'n': n,
            'r0': r0,
            'z0': z0,
            'r': r,
            'z': z,
            'pkey': pkey,
            'command': command,
        },
        'results': compute_bmap_chart(i_h, i_b, i_s, n, r0, z0, r, z, pkey, command),
    }
