import re
import socket
import threading
import time

mapList = {}

def deleteStr(s,start,end):
    s_ = ''
    for i in range(len(s)):
        if i >= start and i <= end:
            s_ += '1'
            continue
        s_ += s[i]
    # print(s_)
    return s_
def FormatPlayer(a_):
    # print(a_)
    i_1 = -1
    i_2 = -1
    for i in range(len(a_) - 1):
        s = a_[i:i + 2]
        if s == '00':
            if i_1 == -1:
                i_1 = i
            elif i_1 != -1 and i_2 == -1:
                i_2 = i
            if i_1 != -1 and i_2 != -1:
                a_ = deleteStr(a_, i_2 + 2, i_2 + 16)
                i_1 = -1
                i_2 = -1
    return a_
def PingNMRIH(gid, ip, port, USERNAME, count,MODE,uid):
    try:
        a = bytes.fromhex("ffffffff54536f7572636520456e67696e6520517565727900")
        other_addr = (ip, int(port))
        net = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        net.sendto(a, other_addr)
        reply, other = net.recvfrom(1024)
        # print(reply.hex())
        reply = reply.hex().split('ffffffff41')[1]
        # print(reply)
        a = bytes.fromhex("ffffffff54536f7572636520456e67696e6520517565727900" + reply)
        # print(a)
        net.sendto(a, other_addr)
        reply1, other = net.recvfrom(5000)
        try:
            abc = bytes.fromhex(bytes.hex(reply1).split('006e6d72696800')[0].split('00')[1]).decode('utf-8','ignore')
        except:
            abc = '未获取得到地图'
        # print(reply)
        # print(reply.decode('utf-8', 'ignore'))
        a = bytes.fromhex("ffffffff5500000000")
        net.sendto(a, other_addr)
        reply, other = net.recvfrom(3000)
        # print(reply.hex())
        reply = bytes.fromhex("ffffffff55" + reply.hex()[10:])
        # print(reply)
        net.sendto(reply, other_addr)
        reply, other = net.recvfrom(3000)
        # print(reply.__str__())
        # print(reply.decode('utf-8', 'ignore'))
        if MODE == '1':
            if reply.decode('utf-8', 'ignore').__contains__(USERNAME):
                # print(reply1.decode('utf-8', 'replace'))
                # print(reply.decode('utf-8', 'replace'))
                # 测试功能，不需要直接删
                a_= FormatPlayer(bytes.hex(reply)[12:])
                # print(a_)
                a = re.findall('00(.*?)00',a_)
                # print(bytes.hex(reply)[12:])
                s = ''
                for i in a:
                    try:
                        # print(bytes.fromhex(str(i)).decode('utf-8', 'ignore'))
                        s += bytes.fromhex(str(i)).decode('utf-8', 'ignore').replace('#','/') + '\r\n'
                    except:
                        if len(i) % 2 == 1:
                            # print(bytes.fromhex(str(i)+'0').decode('utf-8', 'ignore'))
                            s += bytes.fromhex(str(i) + '0').decode('utf-8', 'ignore').replace('#','/') + '\r\n'
                # print(s)
                # requests.get(url='http://127.0.0.1:5700/send_group_msg?group_id=%s&message=%s' % (
                #     gid, '[CQ:at,qq='+str(uid)+']'+'可能在：' + reply1.decode('utf-8', 'replace').__str__().replace('#', '-')))
                try:
                    serverName = bytes.fromhex(bytes.hex(reply1)[12:].split('00')[0]).decode('utf-8').replace('#', '-')
                except:
                    serverName = '未获取到服务器名，但是在线'
                print('%s' % (
                    serverName+'\r\nmaps：' + abc+'\r\n'+'在线人数:'+str(int(reply.hex()[10:].split('00')[0],16))+' / '+str(int(bytes.hex(reply1).split('0064')[0][-2:],16))+'\r\n快速连接:connect '+ip+':'+port+'\r\n——————————————\r\n不准确的名单如下:\r\n'+s))
                # requests.get(url='http://127.0.0.1:5700/send_group_msg?group_id=%s&message=%s' % (
                #     gid, '不准确的名单如下:\r\n'+s))
                #
        elif MODE == '2':
            map = bytes.fromhex(bytes.hex(reply1).split('006e6d72696800')[0].split('00')[1]).decode('utf-8', 'ignore')
            # print(map)
            if map.__contains__(USERNAME):
                # s = reply1.decode('utf-8', 'replace').__str__().replace('#', '-')+'%0a可能包含此地图?'
                # requests.get(url='http://127.0.0.1:5700/send_group_msg?group_id=%s&message=%s' % (
                #     gid, s))
                # 测试功能，不需要直接删
                a_ = FormatPlayer(bytes.hex(reply)[12:])
                # 两个00不得小于14
                # print(a_)
                a = re.findall('00(.*?)00',a_)
                # print(bytes.hex(reply)[12:])
                s = ''
                for i in a:
                    try:
                        # print(bytes.fromhex(str(i)).decode('utf-8', 'ignore'))
                        s += bytes.fromhex(str(i)).decode('utf-8', 'ignore').replace('#','/') + '\r\n'
                    except:
                        if len(i) % 2 == 1:
                            # print(bytes.fromhex(str(i)+'0').decode('utf-8', 'ignore'))
                            s += bytes.fromhex(str(i) + '0').decode('utf-8', 'ignore').replace('#','/') + '\r\n'
                # print(s)
                if str(int(reply.hex()[10:].split('00')[0],16) if reply.hex()[10:].split('00')[0] else '0') != '0':
                    print('%s' % (
                        bytes.fromhex(bytes.hex(reply1)[12:].split('00')[0]).decode(
                            'utf-8').replace('#', '-') + '\r\nmaps：' + abc + '\r\n在线人数:' + str(
                            int(reply.hex()[10:].split('00')[0], 16) if reply.hex()[10:].split('00')[
                                0] else '0') + ' / ' + str(
                            int(bytes.hex(reply1).split('0064')[0][-2:], 16)) + '\r\n快速连接:connect ' + ip + ':' + port+'\r\n——————————————\r\n不准确的名单如下:\r\n'+s))
                else:
                    print('%s' % (
                        bytes.fromhex(bytes.hex(reply1)[12:].split('00')[0]).decode(
                            'utf-8').replace('#', '-') + '\r\nmaps：' + abc + '\r\n在线人数:' + str(
                            int(reply.hex()[10:].split('00')[0], 16) if reply.hex()[10:].split('00')[
                                0] else '0') + ' / ' + str(
                            int(bytes.hex(reply1).split('0064')[0][-2:], 16)) + '\r\n快速连接:connect ' + ip + ':' + port))
        elif MODE == '3':
            map = bytes.fromhex(bytes.hex(reply1).split('006e6d72696800')[0].split('00')[1]).decode('utf-8', 'ignore')
            # print(map)
            try:
                testHave = mapList[map]
                mapList[map] = testHave + 1
            except:
                mapList[map] = 1
            print(mapList)
    except Exception as e:
        # print(f'{ip}:{port}Ping失败重试中...2s\n')
        # traceback.print_exc()
        if count < 0:
            return
        count = count - 1
        # print('剩余重试机会:', count, ' byIP ', ip,':',port)
        time.sleep(2.5)
        PingNMRIH(gid, ip, port, USERNAME, count,MODE,uid)
def NMRIHPing_Thread(gid,s,Trycount,MODE,uid):
    with open('SERVER.txt') as file:
        files = file.readlines()
    for server in files:
        a = server.split(':')
        threading.Thread(target=PingNMRIH, args=(gid, a[0].strip(), a[1].strip(), s, Trycount,MODE,uid)).start()
if __name__ == '__main__':
    m = input('MODE 1(查人) 2(查找地图) 3(Test)\n选择你的模式?:')
    s = ''
    ts = [
        '输入查找玩家名称:','输入查找地图名称:'
    ]
    if m == '1' or m == '2' or m == '3':
        if m != '3':
            s = input(ts[int(m) - 1])
        NMRIHPing_Thread('0', s, 7, m, 0)
    else:
        print('输入内容错误.')
        exit()