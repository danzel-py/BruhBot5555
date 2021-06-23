from tabulate import tabulate
import re

def tablerFunction(msg):
    cmd =  msg.split('\n')[0]
    param1 = cmd.split(' ')
    header = False
    number = False
    width = 0
    for x in param1:
        if(x == "header"):
            header = True
        elif(x == "number"):
            number = True
        elif(re.match("[0-9]+",x)):
            width = int(x)
    linebyline = msg.split('\n')[1:]
    for i in range(len(linebyline)):
        linebyline[i] = linebyline[i].split('-')
    ix = 0
    width = min(width,30)
    if width != 0:
        
        linebyline[ix][0] = f'{linebyline[ix][0]: <{width}}⠀'
    headeropt = ""
    if(header):
        headeropt = "firstrow"
    
    return tabulate(linebyline,headers=headeropt,showindex=number,tablefmt="fancy_grid",)
    