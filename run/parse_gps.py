import sys

gps_output_file = 'detected_gps_coords.txt'
if __name__ == "__main__":
    gps_location_file = sys.argv[1]
    with open(gps_location_file, 'r') as open_file:
        # only one line
        line = open_file.readlines()[0]
        with open(gps_output_file, 'a') as out_file:
            out_file.write(line)
        coords = line.split(',')
        print coords
