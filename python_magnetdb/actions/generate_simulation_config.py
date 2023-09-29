from python_magnetdb.models.site import Site

from python_magnetdb.models.magnet import Magnet
from python_magnetdb.models.material import Material


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
        "nuance": material.nuance,
    }


def generate_magnet_config(magnet_id):
    magnet = Magnet.with_(
        "magnet_parts.part.geometries.attachment",
        "magnet_parts.part.material",
        "site_magnets.site",
        "geometry",
    ).find(magnet_id)
    print(
        f"generate_magnet_config[{magnet_id}]: magnet={magnet.name}, geometry={magnet.geometry}"
    )
    payload = {"geom": magnet.geometry.filename}
    insulator_payload = format_material(Material.where("name", "MAT_ISOLANT").first())
    for magnet_part in magnet.magnet_parts:
        # if not magnet_part.active:
        #     continue
        if magnet_part.part.type.capitalize() not in payload:
            payload[magnet_part.part.type.capitalize()] = []
        geom = None
        for geometry in magnet_part.part.geometries:
            if geometry.type == "default":
                geom = geometry.attachment.filename
        payload[magnet_part.part.type.capitalize()].append(
            {
                "geom": geom,
                "material": format_material(magnet_part.part.material),
                "insulator": insulator_payload,
            }
        )
    # print(f'generate_magnet_config: {payload}')
    return payload


def generate_site_config(site_id):
    site = Site.with_("site_magnets").find(site_id)
    payload = {"name": site.name, "magnets": []}
    for site_magnet in site.site_magnets:
        print(
            f"generate_site_config({site_id}): magnet={site_magnet}, site_magnet={site_magnet.active}"
        )
        # if not site_magnet.active:
        #     continue
        payload["magnets"].append(generate_magnet_config(site_magnet.magnet_id))
    # print(f'generate_site_config: {payload}')
    return payload


def generate_simulation_config(simulation):
    if simulation.resource_type == "magnets":
        return generate_magnet_config(simulation.resource_id)
    elif simulation.resource_type == "sites":
        return generate_site_config(simulation.resource_id)
    raise Exception("Unsupported resource type")
