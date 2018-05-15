import math
from PIL import Image

def entropy(squares):
    count = 0
    res = 0
    for sq in squares:
        entr = 0
        for y in sq:
            for x in y:
                if x == 0:
                    continue
                p = 1.0 * x / (50 * 50)
                entr -= p * math.log(p, 256)
        res += entr
        count += 1
    res = res / count
    return res

def main(str):
    fig = Image.open(str)
    pix = fig.load()  # get pixel data
    width = fig.size[0]
    high = fig.size[1]
    imagesize = width * high
    # get information about each pixel
    red = [0 for x in range(0, imagesize)]
    green = [0 for x in range(0, imagesize)]
    blue = [0 for x in range(0, imagesize)]

    square_50_red = [[[] for j in range(50)] for k in range(imagesize // 50*50 + 1)]
    square_50_green = [[[] for j in range(50)] for k in range(imagesize // 50*50 + 1)]
    square_50_blue = [[[] for j in range(50)] for k in range(imagesize // 50*50 + 1)]

    i = 0
    for x in range(width):
        for y in range(high):
            square_num = (y // 50) * (width // 50 + 1) + (x // 50)
            pix_num_y = y % 50

            red[i], green[i], blue[i] = pix[x, y]
            square_50_red[square_num][pix_num_y].append(red[i])
            square_50_green[square_num][pix_num_y].append(green[i])
            square_50_blue[square_num][pix_num_y].append(blue[i])
            i += 1

    res_r = entropy(square_50_red)
    res_b = entropy(square_50_blue)
    res_g = entropy(square_50_green)

    return [round(res_r, 3), round(res_g, 3), round(res_b, 3)]

if __name__ == '__main__':
    print("Enter picture name")
    str = input()
    rgb_entropy = main(str)
    print(rgb_entropy)