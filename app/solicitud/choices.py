departamentos = {
    ('LA PAZ', 'LA PAZ'),
    ('ORURO ', 'ORURO'),
    ('POTOSI', 'POTOSI'),
    ('CHUQUISACA', 'CHUQUISACA'),
    ('COCHABAMBA', 'COCHABAMBA'),
    ('TARIJA', 'TARIJA'),
    ('SANTA CRUZ', 'SANTA CRUZ'),
    ('BENI', 'BENI'),
    ('PANDO', 'PANDO'),
}

entidad_territorial_autonoma = {
    ('GOBIERNO AUTÓNOMO DEPARTAMENTAL', 'GOBIERNOS AUTÓNOMOS DEPARTAMENTALES'),
    ('GOBIERNO AUTÓNOMO MUNICIPAL', 'GOBIERNOS AUTÓNOMOS MUNICIPALES'),
    ('GOBIERNO AUTÓNOMO REGIONAL', 'GOBIERNOS AUTÓNOMOS REGIONAL'),
    ('GOBIERNO AUTÓNOMO INDIGENA ORIGINARIO CAMPESINO', 'GOBIERNO AUTÓNOMO INDIGENA ORIGINARIO CAMPESINO'),
}

estado_proyecto = {
    ('NINGUNO', 'NINGUNO'),
    ('SOLICITUD', 'SOLICITUD'),
    ('APROBADO', 'APROBADO'),
}

def departamento_s(numero):
    departamentos = {
        1: "LA PAZ",
        2: "BENI",
        3: "CHUQUISACA",
        4: "COCHABAMBA",
        5: "ORURO",
        6: "PANDO",
        7: "POTOSI",
        8: "SANTA CRUZ",
        9: "TARIJA"
    }
    return departamentos.get(numero, "Departamento no encontrado")

def entidad_s(numero):
    entidad = {
        1: "GOBIERNO AUTÓNOMO DEPARTAMENTAL",
        2: "GOBIERNO AUTÓNOMO MUNICIPAL",
        3: "GOBIERNO AUTÓNOMO REGIONAL",
        4: "GOBIERNO AUTÓNOMO INDIGENA ORIGINARIO CAMPESINO"
    }
    return entidad.get(numero, "entidad no encontrada")