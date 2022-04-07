from fastapi import APIRouter, HTTPException, Depends, Form
from fastapi.responses import StreamingResponse

from ...dependencies import get_user
from ...models.attachment import Attachment
from ...models.magnet import Magnet
from ...models.material import Material

router = APIRouter()


@router.get("/api/magnets/{id}/config")
def show(id: int):
    magnet = Magnet.with_('magnet_parts.part.geometry', 'magnet_parts.part.material', 'site_magnets.site', 'cao', 'geometry').find(id)
    if not magnet:
        raise HTTPException(status_code=404, detail="Magnet not found")

    def format_material(material):
        return {
            "Tref": material.t_ref,
            "VolumicMass": material.volumic_mass,
            "alpha": material.alpha,
            "ElectricalConductivity": material.electrical_conductivity,
            "MagnetPermeability": material.magnet_permeability,
            "Poisson": material.poisson,
            "Rpe": material.rpe,
            "SpecificHeat": material.specific_heat,
            "ThermalConductivity": material.thermal_conductivity,
            "Young": material.young,
            "CoefDilatation": material.expansion_coefficient,
            "nuance": material.nuance
        }

    def format_attachment(attachment):
        return {
            "id": attachment.id,
            "filename": attachment.filename,
        }

    payload = {'geom': magnet.geometry.id}
    insulator_payload = format_material(Material.where('name', 'MAT_ISOLANT').first())

    for magnet_part in magnet.magnet_parts:
        if not magnet_part.active:
            continue

        if magnet_part.part.type.capitalize() not in payload:
            payload[magnet_part.part.type.capitalize()] = []
        payload[magnet_part.part.type.capitalize()].append({
            'geom': format_attachment(magnet_part.part.geometry),
            'material': format_material(magnet_part.part.material),
            'insulator': insulator_payload
        })

    return payload


@router.post("/api/simulations")
def create(magnet_id: int = Form(...), method: str = Form(...), model: str = Form(...),
           geometry: str = Form(...), cooling: str = Form(...), user=Depends(get_user('create'))):
    attachment = Attachment.find(id)
    if not attachment:
        raise HTTPException(status_code=404, detail="Attachment not found")

    return StreamingResponse(attachment.download(), media_type=attachment.content_type)
