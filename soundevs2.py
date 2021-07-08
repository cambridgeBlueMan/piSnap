soundDevs=list()
handle = open('soundevs.txt')
for line in handle:
    if line.startswith('hw:CARD='):
        line=line.replace('hw:CARD=','')
        ix=line.find(',')
        devname=(line[0:ix])
        endix=(len(line)-1)
        startix=line.rfind('=')+1
        devnum=(line[startix:endix])
        dev=('hw:'+devname+','+devnum)
        soundDevs.append(dev)
print(soundDevs)