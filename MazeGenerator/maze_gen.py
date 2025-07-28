import argparse
import os.path
import random
from PIL import Image, ImageDraw


def init_argparser():
    """Initialize the command line parser."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "width",
        nargs="?",
        action="store",
        type=int,
        help="lenght of maze's width [INTEGER]",
    )

    parser.add_argument(
        "height",
        nargs="?",
        action="store",
        type=int,
        help="lenght of maze's height [INTEGER]",
    )

    parser.add_argument(
        "filename",
        nargs="?",
        action="store",
        type=str,
        help="filename of the maze to generate",
    )

    return parser


# Funzione per trovare il set di appartenenza di una cella
def find_set(cell, sets):
    if sets[cell] != cell:
        sets[cell] = find_set(sets[cell], sets)
    return sets[cell]

# Unisci due insiemi
def union_sets(set1, set2, sets):
    sets[set2] = set1



def generate_multipath_maze(width, height):
    # Inizializza la griglia del labirinto
    grid = [[{'N': True, 'S': True, 'E': True, 'W': True} for _ in range(width)] for _ in range(height)]

    # Lista di tutti i muri interni possibili
    ''' ha senso perchè crea quelli interni (non i bordi)'''
    walls = []
    for y in range(height):
        for x in range(width):
            if y > 0:
                walls.append((x, y, 'N'))  # Muro Nord
            if x > 0:
                walls.append((x, y, 'W'))  # Muro Ovest

    # Inizializza gli insiemi disgiunti
    sets = {(x, y): (x, y) for y in range(height) for x in range(width)}


    # Mescola casualmente i muri
    '''li mescola però ci sono ancora tutti i muri possibili'''
    random.shuffle(walls)


    '''da qui dino al return ____MI FIDO____'''

    # Algoritmo di Kruskal modificato per creare cicli
    for wall in walls:
        x, y, direction = wall
        if direction == 'N':
            neighbor = (x, y - 1)
        elif direction == 'W':
            neighbor = (x - 1, y)

        set1 = find_set((x, y), sets)
        set2 = find_set(neighbor, sets)

        # Aggiungi il muro solo se i due insiemi sono diversi
        if set1 != set2 or random.random() < 0.3:  # Probabilità di aggiungere un ciclo
            if direction == 'N':
                grid[y][x]['N'] = False
                grid[y - 1][x]['S'] = False
            elif direction == 'W':
                grid[y][x]['W'] = False
                grid[y][x - 1]['E'] = False

            union_sets(set1, set2, sets)

    return grid


def save_img(img, filename):
    filename='./maze_image/'+filename
    filename_new = filename

    i=1
    while os.path.isfile(filename_new+'.png'):
        filename_new=filename+str(i)
        i+=1

    filename_new=filename_new+'.png'
    img.save(filename_new)
    print("Labirinto salvato come '{}'".format(filename_new))


# questa sotto l'ho capita e modificata

def draw_maze(grid, cell_size, filename):
    width = len(grid[0])
    height = len(grid)
    img_width = width * cell_size + 1
    img_height = height * cell_size + 1

    # Crea un'immagine bianca
    img = Image.new("RGB", (img_width, img_height), "white")
    draw = ImageDraw.Draw(img)
    # Disegna i contorni esterni
    draw.rectangle([(0, 0), (img_width - 1, img_height - 1)], outline="black", width=1)

    ''' la griglia orizzontale è 0x400'''
    ''' la griglia verticale è 0x300'''


    # Disegna le pareti interne del labirinto
    for y in range(height):
        for x in range(width):
            cell = grid[y][x]
            x1 = x * cell_size
            y1 = y * cell_size
            x2 = x1 + cell_size
            y2 = y1 + cell_size

            # si studia un quadrato alla volta

            # da x1 a x2 è la lunghezza orizzontale del quadrato che stiamo studiando
            # da y1 a y2 è la lunghezza verticale del quadrato che stiamo studiando

            # nord è sopra (quadrato)
            # sud è sotto (quadrato)
            # ovest = [ è a sinistra (quadrato)
            # est = ] è a destra (quadrato)

            if cell['N']:  # Parete Nord T(va bhe sopra , su)
                draw.line([(x1, y1), (x2, y1)], fill="black", width=1)
            if cell['S']:  # Parete Sud __
                draw.line([(x1, y2), (x2, y2)], fill="black", width=1)
            if cell['W']:  # Parete Ovest [
                draw.line([(x1, y1), (x1, y2)], fill="black", width=1)
            if cell['E']:  # Parete Est ]
                draw.line([(x2, y1), (x2, y2)], fill="black", width=1)



    # Aggiungi uscita
    draw.line([(img_width - 1, img_height - cell_size // 2), (img_width - 1, img_height)], fill="red",
              width=2)  # Uscita

    # Aggiungi punto d'inizio (casuale)
    start_x = random.randrange(0,img_width-cell_size, cell_size)
    start_y = random.randrange(0, img_height-cell_size, cell_size)

    # ogni cella è di size 'cell_size' quindi il punto d'inizio dovrà essere posizionato al centro di una cella
    # (da 1/4 a 3/4, sia in altezza che lunghezza)
    quarter_cell_size = int(cell_size/4)

    draw.rectangle([(start_x+quarter_cell_size ,start_y+quarter_cell_size),(start_x+quarter_cell_size*3,
                                                                            start_y+quarter_cell_size*3)] , fill="red")

    # Mostra l'immagine
    img.show()

    # Salva l'immagine
    save_img(img, filename)


def main():
    parser = init_argparser()
    args = parser.parse_args()

    if args.width is None:
        parser.print_help()
        print(
            "\nWidth to perform maze's width is required, but is not specified."
        )
        return

    if args.height is None:
        parser.print_help()
        print(
            "\nWidth to perform maze's height is required, but is not specified."
        )
        return

    if args.filename is None:
        parser.print_help()
        print(
            "\nName to perform filename is required, but is not specified."
        )
        return

    # generate maze
    maze = generate_multipath_maze(width=args.width, height=args.height)

    # draw maze and save it
    draw_maze(maze, cell_size=20, filename=args.filename)



if __name__ == "__main__":
    main()