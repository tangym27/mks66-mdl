import mdl
from display import *
from matrix import *
from draw import *

def run(filename):
    """
    This function runs an mdl script
    """
    p = mdl.parseFile(filename)

    if p:
        (commands, symbols) = p
    else:
        print "Parsing failed."
        return

    view = [0,
            0,
            1];
    ambient = [50,
               50,
               50]
    light = [[0.5,
              0.75,
              1],
             [255,
              255,
              255]]

    color = [0, 0, 0]
    tmp = new_matrix()
    ident( tmp )

    stack = [ [x[:] for x in tmp] ]
    screen = new_screen()
    zbuffer = new_zbuffer()
    tmp = []
    step_3d = 100
    consts = ''
    coords = []
    coords1 = []
    symbols['.white'] = ['constants',
                         {'red': [0.2, 0.5, 0.5],
                          'green': [0.2, 0.5, 0.5],
                          'blue': [0.2, 0.5, 0.5]}]
    reflect = '.white'

    for line in commands:
        print line
        c = line['op']
        args = line['args']


        if (not args == None):
            args = line['args'][:]

        if (not args ==  None) and 'knob' in line and (not line['knob'] == None) and (c == "move" or c == "scale" or c == "rotate"):
            k = line['knob']
            for i in range(len(args)):
                if not isinstance(args[i], basestring):
                    args[i] = args[i] * symbols[k][1]


        if c == 'box':
            if isinstance(args[0], str):
                consts = args[0]
                args = args[1:]
            if isinstance(args[-1], str):
                coords = args[-1]
            add_box(tmp,
                    args[0], args[1], args[2],
                    args[3], args[4], args[5])
            matrix_mult( stack[-1], tmp )
            draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, reflect)
            tmp = []
        elif c == 'sphere':
            add_sphere(tmp, args[0], args[1], args[2], args[3], step_3d)
            matrix_mult( stack[-1], tmp )
            draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, reflect)
            tmp = []
        elif c == 'torus':
            add_torus(tmp,
                  args[0], args[1], args[2], args[3], args[4], step_3d)
            matrix_mult( stack[-1], tmp )
            draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, reflect)
            tmp = []
        elif c == 'line':
            if isinstance(args[0], str):
                consts = args[0]
                args = args[1:]
            if isinstance(args[3], str):
                coords = args[3]
                args = args[:3] + args[4:]
            if isinstance(args[-1], str):
                coords1 = args[-1]
            add_edge(tmp,
                 args[0], args[1], args[2], args[3], args[4], args[5])
            matrix_mult( stack[-1], tmp )
            draw_lines(tmp, screen, zbuffer, color)
            tmp = []
        elif c == 'move':
            tmp = make_translate(args[0], args[1], args[2])
            matrix_mult(stack[-1], tmp)
            stack[-1] = [x[:] for x in tmp]
            tmp = []
        elif c == 'scale':
            tmp = make_scale(args[0], args[1], args[2])
            matrix_mult(stack[-1], tmp)
            stack[-1] = [x[:] for x in tmp]
            tmp = []
        elif c == 'rotate':
            theta = args[1] * (math.pi/180)
            if args[0] == 'x':
                tmp = make_rotX(theta)
            elif args[0] == 'y':
                tmp = make_rotY(theta)
            else:
                tmp = make_rotZ(theta)
            matrix_mult( stack[-1], tmp )
            stack[-1] = [ x[:] for x in tmp]
            tmp = []
        elif c == 'push':
            stack.append([x[:] for x in stack[-1]] )
        elif c == 'pop':
            stack.pop()
        elif c == 'display':
            display(screen)
        elif c == 'save':
            save_extension(screen, args[0]+".png")
