ua_list = []
try:
    with open('chrome.txt', 'r') as f:
        for line in f.readlines():
            ua_list.append("\'" + line.strip() + "\'" + ',' + '\n')

    with open('ua_list.txt', 'w') as f:
        f.writelines(ua_list)
except Exception as e:
    print(e)
