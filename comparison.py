import math

with open("log.txt", "r") as profData:

    profCoords = [line.split(", ") for line in profData.readlines()]

with open("log2.txt", "r") as userData:

    userCoords = [line.split(", ") for line in userData.readlines()]

threshold = 500

missing = []
flagged = []

for frame in range(len(profCoords)):

    for part in range(24):

        if not (profCoords[frame][part] and userCoords[frame][part]):

            missing.append((frame, part))

        if abs(float(profCoords[frame][part]) - float(userCoords[frame][part])) >= threshold:

            flagged.append((frame, part))