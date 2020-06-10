__doc__ = """Write grid to .dat file"""


def write_tecplot(grid, filename):
    """
    Write grid containing multiple zones to the file.

    :param grid: Grid object.
    :param filename: file to write in.
    :param merge: (bool) whether to merge grid.
    Use ids of the nodes in grid.Nodes instead of zone.Nodes.
    And the ids of faces from grid.Faces instead of zone.Faces.
    I.e. continuing numbering through the grid.
    """
    write_tecplot_header(filename)
    write_zones(grid, filename)


def write_zones(grid, filename):
    """
    Print grid's zones to the filename.

    Warning! if you use this function to add zones
    to the existing tecplot file already containing zones
    then the numeration of zone titles should be handled manually.

    :param grid: Grid object.
    :param filename: file to plot zones in.
    """
    for i, z in enumerate(grid.Zones):
        write_zone_header(filename, 'ZONE {}'.format(i + 1), z.Nodes, z.Faces)

        write_variables(filename, z.Nodes, z.Faces)

        write_connectivity_list(filename, z.Faces)


def write_tecplot_header(filename):
    """
    Write tecplot header containing the information
    about Title and number of variables.

    :param filename: file to write in.
    """
    with open(filename, 'w') as f:
        f.write('# EXPORT MODE: CHECK_POINT\n')
        f.write('TITLE = "GRID"\n')
        f.write('VARIABLES = "X", "Y", "Z", "T", "Hw", "Hi", "HTC", "Beta", "TauX", "TauY", "TauZ"\n')


def write_zone_header(filename, zone_name, nodes, faces):
    """
    Write information about zone into the file.

    :param filename: file to write in.
    :param zone_name: name of the zone.
    :param nodes: nodes.
    :param faces: faces.
    """
    with open(filename, 'a+') as f:
        f.write('ZONE T="{}"\n'.format(zone_name))
        f.write('NODES={}\n'.format((len(nodes))))
        f.write('ELEMENTS={}\n'.format((len(faces))))
        f.write('DATAPACKING=BLOCK\n')
        f.write('ZONETYPE=FETRIANGLE\n')
        f.write('VARLOCATION=([4-11]=CELLCENTERED)\n')


def write_variables(filename, nodes, faces):
    """
    Write variables values in tecplot file.

    :param filename: file to write in.
    :param nodes: nodes containing values.
    """
    with open(filename, 'a+') as f:
        # Variables' values.
        for node in nodes:
            f.write(str(node.x) + ' ')
        f.write('\n')

        for node in nodes:
            f.write(str(node.y) + ' ')
        f.write('\n')

        for node in nodes:
            f.write(str(node.z) + ' ')
        f.write('\n')

        for face in faces:
            f.write(str(face.T) + ' ')
        f.write('\n')

        for face in faces:
            f.write(str(face.Hw) + ' ')
        f.write('\n')

        for face in faces:
            f.write(str(face.Hi) + ' ')
        f.write('\n')

        for face in faces:
            f.write(str(face.HTC) + ' ')
        f.write('\n')

        for face in faces:
            f.write(str(face.Beta) + ' ')
        f.write('\n')

        for face in faces:
            f.write(str(face.TauX) + ' ')
        f.write('\n')

        for face in faces:
            f.write(str(face.TauY) + ' ')
        f.write('\n')

        for face in faces:
            f.write(str(face.TauZ) + ' ')
        f.write('\n')


def write_connectivity_list(filename, faces):
    """
    Write tecplot connectivity list.

    :param filename: file to write in. check2
    :param faces: faces with nodes.
    """
    with open(filename, 'a+') as f:
        # Connectivity list.
        for face in faces:
            for id in face.nodes_ids:
                f.write(str(id) + ' ')
            f.write('\n')
