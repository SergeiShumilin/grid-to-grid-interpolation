__doc__ = """Write triangular_grid to .dat file"""


def write_tecplot(grid, filename):
    """
    Write triangular_grid containing multiple zones to the file.

    :param grid: Grid object.
    :param filename: file to write in.
    :param merge: (bool) whether to merge triangular_grid.
    Use ids of the nodes in triangular_grid.Nodes instead of zone.Nodes.
    And the ids of faces from triangular_grid.Faces instead of zone.Faces.
    I.e. continuing numbering through the triangular_grid.
    """
    write_tecplot_header(filename, grid)
    write_zones(grid, filename)


def write_zones(grid, filename):
    """
    Print triangular_grid's zones to the filename.

    Warning! if you use this function to add zones
    to the existing tecplot file already containing zones
    then the numeration of zone titles should be handled manually.

    :param grid: Grid object.
    :param filename: file to plot zones in.
    """
    for i, z in enumerate(grid.Zones):
        write_zone_header(filename, 'ZONE {}'.format(i + 1), z.Nodes, z.Faces, grid)

        write_variables(filename, z.Nodes, z.Faces, grid)

        write_connectivity_list(filename, z.Faces)


def write_tecplot_header(filename, grid):
    """
    Write tecplot header containing the information
    about Title and number of variables.

    :param filename: file to write in.
    """
    with open(filename, 'w') as f:
        f.write('# EXPORT MODE: CHECK_POINT\n')
        f.write('TITLE = "GRID"\n')
        f.write('VARIABLES = "X", "Y", "Z", "T", "Hw", "Hi", "HTC", "Beta", "TauX", "TauY", "TauZ", "Alpha", ')
        for i, n in enumerate(grid.Nodes):
            if not n.fixed:
                continue
            f.write('"N{}", '.format(i + 1))
        f.write('\n')


def write_zone_header(filename, zone_name, nodes, faces, grid):
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
        f.write('VARLOCATION=([4-{}]=CELLCENTERED)\n'.format(grid.number_of_border_nodes + 12))


def write_variables(filename, nodes, faces, grid):
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

        for face in faces:
            f.write(str(face.alpha_quality_measure()) + ' ')
        f.write('\n')

        for n in grid.Nodes:
            if not n.fixed:
                continue
            for af in grid.adj_list_for_border_nodes[n.Id - 1, :]:
                assert af == 0 or af == 1
                f.write(str(af) + ' ')
            f.write('\n')


def write_connectivity_list(filename, faces):
    """
    Write tecplot connectivity list. c

    :param filename: file to write in.
    :param faces: faces with nodes.
    """
    with open(filename, 'a+') as f:
        # Connectivity list.
        for face in faces:
            for id in face.nodes_ids:
                f.write(str(id) + ' ')
            f.write('\n')
