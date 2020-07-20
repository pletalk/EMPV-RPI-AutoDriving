
def degree2range(degree, minvi=-1, maxv=1):
    diff = degree-90
    interval = diff*(1/90)
    #print(diff)
    return interval
    

if __name__ == '__main__':
    rvalue = degree2range(122)
    print(rvalue)








