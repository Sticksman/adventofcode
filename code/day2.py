def calculate_necessary_area(*dimensions):
    areas = []
    for i, val in enumerate(dimensions):
        for j in dimensions[(i+1):]:
            areas.append(val * j)
    areas.sort()
    total_area = areas[0]
    for area in areas:
        total_area += 2 * area
    return total_area

def calculate_bow_length(*dimensions):
    dimensions = list(dimensions)
    dimensions.sort()

    perimeter = 2 * dimensions[0] + 2 * dimensions[1]
    volume = dimensions[0] * dimensions[1] * dimensions[2]
    return perimeter + volume

if __name__ == '__main__':
    with open('adventofcode/inputs/day2') as f:
        total_area = 0
        length = 0
        for line in f.readlines():
            line = line.strip()
            dimensions = line.split('x')
            dimensions = [int(d) for d in dimensions]
            total_area += calculate_necessary_area(*dimensions)
            length += calculate_bow_length(*dimensions)


    print total_area
    print length
