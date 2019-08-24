def ip4check(value):
    ip4check = value.split('.')
    c=0
    for n in ip4check:
        try:
            int(n)
        except:
            break
        else:
            if int(n)>=0 and int(n)<=255:
                c+=1
                #print (int(n))
                #print (c)
            else:
                c-=1
    #print (c,'is c')
    #print (ip4check)
    #print (len(ip4check),'is value')
    if c==len(ip4check) and c==4:
        return True
    else:
        return False

def ip6check(value):
    ip6check = value.split(':')
    t=0
    #print(ip6check)
    #print(len(ip6check))
    for val in ip6check:
        #print (val,'is val')
        try:
            int(val,16)
        except:
            t-=1
        else:
            t+=1

    #print (ip6check,'asda')
    #print (t,'sd')
    #print (len(ip6check),'oi')
    if t==len(ip6check):
        return True
    else:
        return False




def checkIPs(ip_array):
    output=[]
    for ips in ip_array:
        if ip4check(ips):
            output.append ("IP4")
        else:
            if ip6check(ips):
                output.append ("IP6")
            else:
                output.append ("Neither")
    return output


if __name__ == '__main__':
    print ("\n".join(checkIPs(['This is just a asd.','12.0.54.255','55.21:54:54:87:152','2001:db8:1234:0000:0000:0000:0000:0000:0000'])))
