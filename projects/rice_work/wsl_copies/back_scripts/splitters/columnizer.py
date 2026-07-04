print('running columnizer.py ...')


with open("/home/treed777/move/part1.txt", "w") as w:
    with open("/home/treed777/move/C1.ndb", "r") as r:
        count = 0
        for line in r:
            if not line.startswith("SEQCHR"):
                r.close()
                break
            #columnizer assumes characters to first A1, B2, NA, etc is consistent
            line = line[21:].rstrip()
            # print(line)
            ln = line.split(' ')
            # print(ln)
            for cState in ln:
                w.write(f'{count} {cState}\n')
                count += 1


with open("/home/treed777/move/part2.txt", "w") as w:
    with open("/home/treed777/move/C2.ndb", "r") as r:
        count = 0
        for line in r:
            if not line.startswith("SEQCHR"):
                r.close()
                break
            #columnizer assumes characters to first A1, B2, NA, etc is consistent
            line = line[21:].rstrip()
            # print(line)
            ln = line.split(' ')
            # print(ln)
            for cState in ln:
                w.write(f'{count} {cState}\n')
                count += 1