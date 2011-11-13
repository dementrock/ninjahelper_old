import urllib

    
def find_info(number):
    f = urllib.urlopen("http://infobears.berkeley.edu:3400/osc/?_InField1=RESTRIC&_InField2=%d&_InField3=12B4" % number)
    temp = f.read()
    a , b  = temp.find('<blockquote>'), temp.find('</blockquote>')
    temp_string = temp[a : b]
    has_wait_list = (temp_string.find('does not use a Waiting List') == -1)
    return analyze_num(temp_string), has_wait_list  


def analyze_num(s):
    l = len(s)
    num_list = []
    i = 0
    while i < l: 
        try:
            n = int(s[i])
            flag = True
            t = 2
            while flag:
                try:
                    n = int(s[i:i + t])
                    t += 1
                except ValueError:
                    num_list.append(n)
                    i += t
                    flag = False
        except ValueError:
            i += 1
    return num_list


def debug():

    print(temp_string)
    print(len(temp_string))
    print(analyze_num(temp_string))
    print(has_wait_list)
print find_info(26449)






        
        
    
    
    
        

