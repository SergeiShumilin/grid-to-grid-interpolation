from triangular_grid.node import Node
from triangular_grid.face import Face
from triangular_grid.edge import Edge
from triangular_grid.grid import Grid
from triangular_grid.zone import Zone

NUMBER_OF_LINES_BETWEEN_ELEMENTS_COUNT_AND_VALUES = 4
NUMBER_OF_VARIABLES = 11


def read_tecplot(grid, filename):
    """
    Read tecplot file.

    :param grid: Grid object.
    :param filename: file to read from.
    """
    with open(filename, 'r') as file_with_grid:

        lines = file_with_grid.readlines()

        if lines[0] != '# EXPORT MODE: CHECK_POINT\n':
            print(lines[0])
            raise ValueError('CHECK_POINT mode required')

        faces_count = list()
        indexes = list()

        # Find and remember all ELEMENTS words in the file.
        # They design a start of zone.
        for i, line in enumerate(lines):
            if line.find('ELEMENTS=') != -1:
                faces_count.append(number_of_faces(line))

                # +3 is the correction to start from the line
                # where the variables start.
                indexes.append(i + NUMBER_OF_LINES_BETWEEN_ELEMENTS_COUNT_AND_VALUES)

        # List of lists of nodes for each zone.
        nodes = list()
        # List of lists of faces for each zone.
        faces = list()

        # Extract each zone from certain lines using indexes of lines
        # obtained earlier.
        for f, i in zip(faces_count, indexes):
            # Create a zone.
            z = Zone()
            grid.Zones.append(z)

            # Return nodes and faces for the zone
            # by parcing the file.
            parces_nodes, parces_faces = parce_nodes_and_faces(lines[i: i + f + NUMBER_OF_VARIABLES])
            nodes.append(parces_nodes)
            faces.append(parces_faces)

            z.Nodes = parces_nodes
            z.Faces = parces_faces

            assert len(parces_faces) == f

        set_nodes(grid, nodes)
        for f, n in zip(faces, nodes):
            set_faces(grid, n, f)
            grid.Faces += f

        grid.init_adjacent_faces_list_for_border_nodes()


def set_faces(grid, nodes, faces):
    """
    Link faces and nodes according to the connectivity list.

    1 2 3  -> Face 1
    2 3 4  -> Face 2

    Also, edges are created and linked basing on their presence in triangular_grid.Edge.

    :param grid: Grid object.
    :param nodes: list : nodes to link.
    :param faces: list : faces to link.
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


def parce_nodes_and_faces(lines):
    """
    Parce node and faces from tecplot file.

    Creates list of nodes and list of faces.
    Set the x, y coordinates of nodes.

    Add list of nodes' ids to each face.

    :param lines: tecplot lines representing the
    value and connectivity lists.

    :return: tuple (list, list): nodes and faces for a zone.
    """
    # Read all nodes of zone 1.
    # x coords.
    xs = map(parcer, lines[0].split(' '))
    # y coords.
    ys = map(parcer, lines[1].split(' '))
    # z coords.
    zs = map(parcer, lines[2].split(' '))
    t = map(parcer, lines[3].split(' ')[:-1])
    hw = map(parcer, lines[4].split(' ')[:-1])
    hi = map(parcer, lines[5].split(' ')[:-1])
    htc = map(parcer, lines[6].split(' ')[:-1])
    beta = map(parcer, lines[7].split(' ')[:-1])
    taux = map(parcer, lines[8].split(' ')[:-1])
    tauy = map(parcer, lines[9].split(' ')[:-1])
    tauz = map(parcer, lines[10].split(' ')[:-1])

    # Nodes of zone 1.
    nodes = list()

    # Initialize node array for zone 1.
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
    for line in lines[NUMBER_OF_VARIABLES:]:
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
            raise ValueError('Identical ids in the triangular_grid')

    for f, t_, hw_, hi_, htc_, beta_, taux_, tauy_, tauz_ in zip(faces, t, hw, hi, htc, beta, taux, tauy, tauz):
        f.T = t_
        f.Hw = hw_
        f.Hi = hi_
        f.HTC = htc_
        f.Beta = beta_
        f.TauX = taux_
        f.TauY = tauy_
        f.TauZ = tauz_

    return nodes, faces


def parcer(s):
    """Parcing values algorithm."""
    if s == 'None':
        return None
    if s == '\n':
        return None
    else:
        return float(s)


def set_nodes(grid, nodes):
    """
    Fill triangular_grid.Nodes list with unique nodes from each zone.

    :param grid: Grid object.
    :param nodes: list of lists of nodes for each zone.
    """
    # Copy all nodes from zone 1 to the triangular_grid.
    grid.Nodes = [node for node in nodes[0]]
    grid.make_avl()

    for n in nodes[1:]:
        compose_node_list_nlogn_algorithm(grid, n)


def compose_node_list_nlogn_algorithm(grid, nodes_z2):
    """
    Compose triangular_grid.Nodes from the nodes from two zones to avoid repeating.

    The nodes are compared according to their coordinates (x, y).
    The algorithm does simple n^2 search through all nodes.

    :param grid: Grid object.
    :param nodes_z2: list: nodes of zone 2.
    """
    for i, n in enumerate(nodes_z2):
        found = grid.avl.find(n)
        if not found:
            grid.Nodes.append(n)
            grid.avl.insert(n)
        else:
            n = found


def number_of_zones(file):
    """
    Count the number of times the word ZONE occurs in the file.

    :param file: file to read.
    :return: number of zones.
    """
    return ' '.join(file).count('ZONE T')


def number_of_nodes(line):
    """
    Extract the number of nodes from te line.

    :param line: line with the word NODES
    :return: int number of nodes.
    """
    return int(line[line.find('NODES =') + 7: len(line)])


def number_of_faces(line):
    """
    Extract the number of nodes from te line.

    :param line: line with the word NODES
    :return: int number of nodes.
    """
    return int(line[line.find('ELEMENTS =') + 10: len(line)])