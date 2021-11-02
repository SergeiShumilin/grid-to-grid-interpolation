from triangular_grid.node import Node
from triangular_grid.face import Face
from triangular_grid.edge import Edge
from triangular_grid.grid import Grid
from triangular_grid.zone import Zone

NUMBER_OF_LINES_BETWEEN_ELEMENTS_COUNT_AND_VALUES = 4
NUMBER_OF_COORDINATES = 3
NUMBER_OF_LINES_BETWEEN_X_COORD_AND_ZONE_TITILE = 6
NUMBER_OF_LINES_BETWEEN_X_COORD_AND_VARLOCATION = 1


def read_tecplot(grid, filename):
    """
    Read tecplot file.

    Parameters
    ----------
        grid : Grid object
            target grid
        filename : string
            source file
    """
    with open(filename, 'r') as file_with_grid:

        lines = file_with_grid.readlines()

        grid.export_mode = lines[0]

        grid.title = lines[1]

        grid.variables = lines[2]

        index_of_hi, num_of_variables = parce_variables(lines[2])

        grid.position_of_hi = index_of_hi - NUMBER_OF_COORDINATES

        faces_count = list()
        where_data_starts = list()

        # Find and remember all ELEMENTS words in the file.
        # They design a start of zone.
        for i, line in enumerate(lines):
            if line.find('ELEMENTS=') != -1:
                faces_count.append(number_of_faces(line))

                # +3 is the correction to start from the line
                # where the variables start.
                where_data_starts.append(i + NUMBER_OF_LINES_BETWEEN_ELEMENTS_COUNT_AND_VALUES)

        # List of lists of nodes for each zone.
        nodes = list()
        # List of lists of faces for each zone.
        faces = list()

        # Extract each zone from certain lines using indexes of lines
        # obtained earlier.
        for f, i in zip(faces_count, where_data_starts):
            # Create a zone.
            z = Zone()
            grid.Zones.append(z)

            # Remember data that is of no need
            z.variables = lines[i + NUMBER_OF_COORDINATES: i + num_of_variables]

            # Varlocation is a line before i
            z.varlocation = lines[i - NUMBER_OF_LINES_BETWEEN_X_COORD_AND_VARLOCATION]

            # Zone title is the ELEMENTS line minus 6
            z.title = lines[i - NUMBER_OF_LINES_BETWEEN_X_COORD_AND_ZONE_TITILE]

            # Return nodes and faces for the zone
            # by parcing the file.
            parced_nodes, parced_faces = parce_nodes_and_faces(lines[i: i + f + num_of_variables],
                                                               num_of_variables,
                                                               index_of_hi)
            nodes.append(parced_nodes)
            faces.append(parced_faces)

            z.Nodes = parced_nodes
            z.Faces = parced_faces



            assert len(parced_faces) == f

        set_nodes(grid, nodes)
        for f, n in zip(faces, nodes):
            set_faces(grid, n, f)
            grid.Faces += f


def parse_obj_node(line):
    """Parces coordinates of a node.

    Parameters
    ----------
        line : strings
            line with coordinates

    Returns
    -------
        Node obj with coords initialized
    """
    coords = line.split(' ')
    assert len(coords) == 4, print(coords)
    x = float(coords[1])
    y = float(coords[2])
    z = float(coords[3])
    return Node(x, y, z)


def parse_obj_face(line):
    """Parce ids of a face.

    Parameters
    ----------
        line : strings
            line with ids

    Returns
    -------
        Face obj with ids of adjacent nodes initialized
    """
    ids = line.split(' ')
    assert len(ids) == 4, print(ids)
    assert ids[0] == 'f'

    # To handle with such lines
    # 'f 34500/34446/34500 34501/34447/34501 49681/49530/49681'
    real_ids = []
    if len(ids[1].split('/')) != 0:
        for chank in ids[1:]:
            real_ids.append(chank.split('/')[0])
        id1 = int(real_ids[0])
        id2 = int(real_ids[1])
        id3 = int(real_ids[2])
    else:
        id1 = int(ids[1])
        id2 = int(ids[2])
        id3 = int(ids[3])
    f = Face()
    f.nodes_ids = [id1, id2, id3]
    return f


def parce_variables(line):
    """Parce variables in this file and identify where Hi is and count them.

    Parameters
    ----------
        line: string
          contains variables' list

    Returns
    -------
        tuple
        (Hi position, number of variables)

    Raises
    ------
    ValueError
        when no hi in the variables list
    """
    variables = line.split(" ")

    assert variables[0] == "VARIABLES=\"X\",", "list of variables doesn't start with X"

    for i, v in enumerate(variables):
        if v.find("\"Hi\"") != -1 or v.find("\"IceThickness\"") != -1:
            return i, len(variables)

    raise ValueError("No Hi in the variables' list")


def read_obj(grid, filename):
    """
    Read file in .OBJ data format.

    Parameters
    ----------
        grid: Grid object
            grid to read in

        filename: string
            file to read from
    """
    assert filename[-4:] == '.obj', 'not an .obj format'

    j = 0
    with open(filename, 'r') as file_with_grid:
        lines = file_with_grid.readlines()

        for line in lines:
            print(j)
            j += 1
            if line[0] == '#':
                continue
            if line[0:2] == 'v ':
                grid.Nodes.append(parse_obj_node(line))
            if line[0:2] == 'f ':
                grid.Faces.append(parse_obj_face(line))

        z = Zone()
        z.Nodes = grid.Nodes
        z.Faces = grid.Faces
        grid.Zones.append(z)
        set_faces(grid, grid.Nodes, grid.Faces)


def set_faces(grid, nodes, faces):
    """
    Link faces and nodes according to the connectivity list.

    Edges are created and linked based on their presence in the grid.Edges list.

    Parameters
    ----------
        grid: Grid object
            grid

        nodes: list
            nodes to link

        faces: list
            faces to link.
    """
    for f in faces:
        n1 = nodes[f.nodes_ids[0] - 1]
        n2 = nodes[f.nodes_ids[1] - 1]
        n3 = nodes[f.nodes_ids[2] - 1]

        # Link face and nodes.
        Grid.link_face_and_node(f, n1)
        Grid.link_face_and_node(f, n2)
        Grid.link_face_and_node(f, n3)

        # Link faces, nodes and edges.
        e = grid.is_edge_present(n1, n2)
        if e is None:
            e = Edge()
            grid.link_face_and_edge(f, e)
            grid.link_node_and_edge(n1, e)
            grid.link_node_and_edge(n2, e)
            grid.Edges.append(e)
        else:
            grid.link_face_and_edge(f, e)

        e = grid.is_edge_present(n2, n3)
        if e is None:
            e = Edge()
            grid.link_face_and_edge(f, e)
            grid.link_node_and_edge(n2, e)
            grid.link_node_and_edge(n3, e)
            grid.Edges.append(e)
        else:
            grid.link_face_and_edge(f, e)

        e = grid.is_edge_present(n3, n1)
        if e is None:
            e = Edge()
            grid.link_face_and_edge(f, e)
            grid.link_node_and_edge(n3, e)
            grid.link_node_and_edge(n1, e)
            grid.Edges.append(e)
        else:
            grid.link_face_and_edge(f, e)


def parser(s):
    """Safe conversion to float.

    Parameters
    ----------
        s : string
            a number

    Returns
    -------
        float or None
    """
    if s == 'None':
        return None
    if s == '\n':
        return None
    else:
        return float(s)


def parce_nodes_and_faces(lines, number_of_variables, index_of_hi):
    """
    Parse node and faces from tecplot file.

    Creates list of nodes and list of faces.
    Set the x, y coordinates of nodes.

    Add list of nodes' ids to each face.

    Parameters
    ----------
        lines : array of strings
            tecplot lines representing the
            value and connectivity lists.

        number_of_variables : int
            number of variables in the grid
            number of elements in VERIABLES line

        index_of_hi : int
            index of hi in variables list w.r.t. only faces' variables

    Returns:
        tuple : (list, list)
            nodes and faces for the zone.

    Raises:
        ValueError
            when can't convert sting id of a node to int
            when ids in one face coinside
    """
    # Read all nodes of zone 1.
    # x coords.
    xs = map(parser, lines[0].split(' '))
    # y coords.
    ys = map(parser, lines[1].split(' '))
    # z coords.
    zs = map(parser, lines[2].split(' '))
    # todo we make an assumption that T and Hw are followed by Hi.
    # t
    ts = map(parser, lines[index_of_hi - 2].split(' ')[:-1])
    # hw
    hws = map(parser, lines[index_of_hi - 1].split(' ')[:-1])
    # hi
    his = map(parser, lines[index_of_hi].split(' ')[:-1])

    # Nodes of zone 1.
    nodes = list()

    # Initialize node array.
    i = 1
    for x, y, z in zip(xs, ys, zs):
        if x is None:
            continue
        if y is None:
            continue
        if z is None:
            continue
        n = Node()
        n.x = x
        n.y = y
        n.z = z
        n.Id = i
        i += 1
        nodes.append(n)

    del xs, ys, zs

    faces = list()

    j = 0
    for line in lines[number_of_variables:]:
        f = Face(j)
        j += 1
        ids = line.split(' ')
        if len(ids) > 3:
            ids = ids[:-1]
        try:
            ids = list(map(int, ids))
        except ValueError:
            print('Unable to convert to int')

        f.nodes_ids = ids
        faces.append(f)

        if ids[0] == ids[1] or ids[1] == ids[2] or ids[0] == ids[2]:
            print(ids[0], ids[1], ids[2])
            raise ValueError('Identical ids of nodes in face')

    for f, t_, hw_, hi_ in zip(faces, ts, hws, his):
        f.T = t_
        f.Hw = hw_
        f.Hi = hi_

    return nodes, faces


def set_nodes(grid, nodes):
    """
    Fill the grid with nodes.

    Does iteration through the node list of lists.
    And subsequently adds new nodes to the existing by nlogn comparison.

    Parameters
    ----------
        grid: Grid object
            grid
        nodes: list of lists of Node obj
            nodes for each zone
    """
    # Copy all nodes from zone 1 to grid.
    grid.Nodes = [node for node in nodes[0]]
    grid.make_avl()

    for n in nodes[1:]:
        add_nodes_to_grid(grid, n)


def add_nodes_to_grid(grid, nodes):
    """
    Adds `nodes` a list of Node obj to the grid
    by AVL Tree. That is nlogn search.

    The nodes are compared according to their coordinates (x, y, z).

    Parameters
    ----------
        grid : Grid obj
            grid to add the nodes to
        nodes : list of Node obj
            nodes to be added to the grid
    """
    for i, n in enumerate(nodes):
        found = grid.avl.find(n)
        if not found:
            grid.Nodes.append(n)
            grid.avl.insert(n)
        else:
            nodes[i] = found


def number_of_zones(file):
    """
    Count the number of times the word ZONE occurs in the file.

    Parameters
    ----------
        file: list of strings
            file to read.

    Return
    ------
        number of zones
    """
    return ' '.join(file).count('ZONE T')


def number_of_nodes(line):
    """
    Extract the number of nodes from te line.

    Parameters
    ----------
        line: string
            line with the word NODES

    Return
    ------
        number of nodes
    """
    return int(line[line.find('NODES =') + 7: len(line)])


def number_of_faces(line):
    """
    Extract the number of nodes from te line.

    Parameters
    ----------
        line: line with the word NODES

    Return
    ------
        number of faces
    """
    return int(line[line.find('ELEMENTS =') + 10: len(line)])


def write_tecplot(grid, filename):
    """
    Write triangular grid containing multiple zones to the file.

    Parameters
    ----------
        grid: Grid object
            grid to write

        filename: string
            file to write in
    """
    write_tecplot_header(grid, filename)
    write_zones(grid, filename)


def write_zones(grid, filename):
    """
    Print triangular grid's zones to the file one by one.

    Parameters
    ----------
        grid : Grid obj
            grid to write in

        filename : string
            file to write in
    """
    for i, z in enumerate(grid.Zones):
        write_zone_header(z, filename)

        write_variables(filename, z, grid.position_of_hi)

        write_connectivity_list(z.Faces, filename)


def write_tecplot_header(grid, filename):
    """
    Write tecplot header.

    Parameters
    ----------
        grid : Grid
            grid

        filename : string
            file to write in
    """
    with open(filename, 'w') as f:
        f.write(grid.export_mode)
        f.write(grid.title)
        f.write(grid.variables)


def write_zone_header(zone, filename):
    """
    Write information about zone into the file.

    Parameters
    ----------
        zone : Zone
            zone

        filename : string
            file to write in
    """
    with open(filename, 'a+') as f:
        f.write(zone.title)
        f.write('NODES={}\n'.format((len(zone.Nodes))))
        f.write('ELEMENTS={}\n'.format((len(zone.Faces))))
        f.write('DATAPACKING=BLOCK\n')
        f.write('ZONETYPE=FETRIANGLE\n')
        f.write(zone.varlocation)


def write_variables(filename, zone, position_of_hi):
    """
    Write variables' values in tecplot file.

    Skips old values of Hi, inserting new ones.

    Parameters
    ----------
        filename : string
            output file

        zone : Zone object
            source zone

        position_of_hi : int
            index of hi w.r.t. faces' variables
    """
    with open(filename, 'a+') as f:
        for node in zone.Nodes:
            f.write(str(node.x) + ' ')
        f.write('\n')

        for node in zone.Nodes:
            f.write(str(node.y) + ' ')
        f.write('\n')

        for node in zone.Nodes:
            f.write(str(node.z) + ' ')
        f.write('\n')

        for i, vs in enumerate(zone.variables):
            # todo T
            if i == position_of_hi - 2:
                for face in zone.Faces:
                    f.write(str(face.T) + ' ')
                f.write('\n')
                continue
            # todo Hw
            if i == position_of_hi - 1:
                for face in zone.Faces:
                    f.write(str(face.Hw) + ' ')
                f.write('\n')
                continue
            if i == position_of_hi:
                for face in zone.Faces:
                    f.write(str(face.Hi) + ' ')
                f.write('\n')
                continue
            f.write(vs)


def write_connectivity_list(faces, filename):
    """
    Write tecplot connectivity list.

    Parameters
    ----------
        faces : list of Face
            faces

        filename : string
            output file
    """
    with open(filename, 'a+') as f:
        # Connectivity list.
        for face in faces:
            for id in face.nodes_ids:
                f.write(str(id) + ' ')
            f.write('\n')
