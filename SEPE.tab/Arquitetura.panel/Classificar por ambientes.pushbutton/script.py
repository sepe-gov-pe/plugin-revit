# -*- coding: utf-8 -*-
#! ironpython3

"""Classifica todas as paredes por ambiente."""

from Autodesk.Revit.DB import (
    XYZ,
    BuiltInParameter,
    FilteredElementCollector,
    Transaction,
    Wall,
)

doc = __revit__.ActiveUIDocument.Document

OFFSET = 0.003
PARAM_AMBIENTE = "Ambiente"


def get_point(wall):
    """Retorna um ponto à frente da face externa da parede."""
    loc = wall.Location
    curve = loc.Curve

    tangent = curve.ComputeDerivatives(0.5, True).BasisX.Normalize()
    local_normal = XYZ(-tangent.Y, tangent.X, 0.0)

    if local_normal.DotProduct(wall.Orientation) < 0:
        local_normal = XYZ(-local_normal.X, -local_normal.Y, 0.0)

    offset = (wall.Width / 2.0) + OFFSET
    base_point = curve.Evaluate(0.5, True)
    point = base_point + local_normal.Multiply(offset)

    bbox = wall.get_BoundingBox(None)
    z_mid = (bbox.Min.Z + bbox.Max.Z) / 2.0

    return XYZ(point.X, point.Y, z_mid)


def get_walls(doc):
    """Lista com todas as paredes do projeto."""
    return (
        FilteredElementCollector(doc)
        .OfClass(Wall)
        .WhereElementIsNotElementType()
        .ToElements()
    )


def get_phase(wall, doc):
    """Pega fase de criação da parede."""
    phase_id = wall.get_Parameter(BuiltInParameter.PHASE_CREATED).AsElementId()
    return doc.GetElement(phase_id)


def get_ambient(point, phase, doc):
    """Retorna o ambiente (room) no ponto dado."""
    return doc.GetRoomAtPoint(point, phase)


def get_element_level(room):
    """Retorna o nome do nível do ambiente."""

    level = room.Level

    if level:
        return level.Name

    return None


def get_element_name(element):
    """Retorna o nome do ambiente."""

    name_param = element.get_Parameter(BuiltInParameter.ROOM_NAME)

    if name_param and name_param.HasValue:
        return name_param.AsString()

    return "AMBIENTE SEM NOME"


def set_ambient(wall, nome):
    """Define o parâmetro Ambiente da parede."""
    param = wall.LookupParameter(PARAM_AMBIENTE)
    if param and not param.IsReadOnly:
        param.Set(nome)
        return True
    return False


def main(doc):
    """Função principal."""
    walls = get_walls(doc)

    with Transaction(doc, "SEPE - Identificar Ambiente") as t:
        t.Start()
        try:
            for wall in walls:
                phase = get_phase(wall, doc)
                if phase is None:
                    continue

                point = get_point(wall)
                if point is None:
                    continue

                ambient = get_ambient(point, phase, doc)
                if ambient is None:
                    continue

                ambient_level = get_element_level(ambient)
                ambient_name = get_element_name(ambient)

                ambient_string = "{} - {}".format(ambient_level, ambient_name)
                set_ambient(wall, ambient_string)

            t.Commit()

        except Exception as ex:
            t.RollBack()
            print("Erro durante o processamento: {}".format(str(ex)))
            raise


if __name__ == "__main__":
    main(doc)
