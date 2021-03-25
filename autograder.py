"""
@Version 0.3.3
@Author B1ACK917
@Contributor YuanWind
"""

import json
import os
from tqdm import tqdm
import time
import copy
import matplotlib.pyplot as plt
from genHTML import gen
import platform


def check_bomb(server, VMList, serverDict, VMDict, serverIDMap, VMIDMap, vmid2node):
    """
    判断一个服务器是否发生资源溢出
    :param server: 服务器ID
    :param VMList: 服务器上挂载的虚拟机
    :param serverDict: 服务器型号到服务器详细信息的映射
    :param VMDict: 虚拟机ID到虚拟机详细信息的映射
    :param serverIDMap: 从服务器ID到服务器型号的映射
    :param VMIDMap: 虚拟机ID到虚拟机型号的映射
    :param vmid2node: 虚拟机节点信息
    :return:
    """
    serverCPU, serverMEM = serverDict[serverIDMap[server]]['cpu'], serverDict[serverIDMap[server]]['memory']
    serverCPU_A, serverMEM_A = serverCPU / 2, serverMEM / 2
    serverCPU_B, serverMEM_B = serverCPU / 2, serverMEM / 2
    for VM in VMList:
        node = vmid2node[VM]
        if node == 'A':
            serverCPU_A -= VMDict[VMIDMap[VM]]['cpu']
            serverMEM_A -= VMDict[VMIDMap[VM]]['memory']
        elif node == 'B':
            serverCPU_B -= VMDict[VMIDMap[VM]]['cpu']
            serverMEM_B -= VMDict[VMIDMap[VM]]['memory']
        elif node == None:
            serverCPU_A -= VMDict[VMIDMap[VM]]['cpu'] / 2
            serverMEM_A -= VMDict[VMIDMap[VM]]['memory'] / 2
            serverCPU_B -= VMDict[VMIDMap[VM]]['cpu'] / 2
            serverMEM_B -= VMDict[VMIDMap[VM]]['memory'] / 2
        if serverCPU_A < 0 or serverMEM_A < 0 or serverCPU_B < 0 or serverMEM_B < 0:
            return False
    return True


def grader(testCmd, ioData):
    vmid2node = {}
    serverDict = {}
    VMDict = {}
    operateInfo = []

    """
    所有处理后的数据将存放在下文中的fullInfo中，每一个字段在后面的注释都有说明。
    """

    with open(ioData) as file:
        """
        从输入文件中获取服务器信息和每一天的操作序列
        operateInfo中按天存储了当天的操作序列
        """
        serverNums = eval(file.readline())
        for i in range(serverNums):
            _type, _cpus, _mem, _hardCost, _energyCost = file.readline()[1:-2].split(',')
            serverDict.update({_type: {'cpu': eval(_cpus),
                                       'memory': eval(_mem),
                                       'hardCost': eval(_hardCost),
                                       'energyCost': eval(_energyCost)}})
        VMNums = eval(file.readline())
        for i in range(VMNums):
            _type, _cpus, _mem, doubleNode = file.readline()[1:-2].split(',')
            VMDict.update({_type: {'cpu': eval(_cpus),
                                   'memory': eval(_mem),
                                   'double': eval(doubleNode)}})
        days = eval(file.readline())
        for i in range(days):
            dayOperateInfo = {'operate': []}
            nums = eval(file.readline())
            for j in range(nums):
                tmp = file.readline().strip()[1:-1]
                if tmp[:3] == 'add':
                    _op, _, _id = tmp.split(',')
                    dayOperateInfo['operate'].append((_op, eval(_id), _))
                else:
                    _op, _id = tmp.split(',')
                    dayOperateInfo['operate'].append((_op, eval(_id)))
            operateInfo.append(dayOperateInfo)

    beginTime = time.perf_counter()
    result = os.popen(testCmd)
    result = result.read().strip().split('\n')
    endTime = time.perf_counter()  # 计时器
    fullInfo = []
    for i in range(len(result)):
        if 'purchase' in result[i]:  # 整理每天的购买信息
            singleDayInfo = {'purchase': {}}
            _, serverBought = result[i][1:-1].split(',')
            serverBought = eval(serverBought.strip())
            for j in range(i + 1, i + serverBought + 1):
                serverName, serverNum = result[j][1:-1].split(',')
                singleDayInfo['purchase'].update({serverName: eval(serverNum)})
            fullInfo.append(singleDayInfo)
        elif 'migration' in result[i]:  # 整理每天的迁移信息
            migrationInfo = {'migration': []}
            _, migrationNum = result[i][1:-1].split(',')
            migrationNum = eval(migrationNum.strip())
            for j in range(i + 1, i + migrationNum + 1):
                sp = result[j][1:-1].split(',')
                if len(sp) == 2:
                    sourceID, targetID = sp
                    migrationInfo['migration'].append((eval(sourceID), (eval(targetID), None)))
                else:
                    sourceID, targetID, targetNode = sp
                    migrationInfo['migration'].append((eval(sourceID), (eval(targetID), targetNode)))
            fullInfo[-1].update(migrationInfo)
            requestInfo = {'request': []}
            for j in range(i + migrationNum + 1, len(result)):  # 超过迁移行数以后的部分被认为是部署信息，直到遇到purchase为止
                if 'purchase' in result[j]:
                    break
                sp = result[j][1:-1].split(',')
                if len(sp) == 1:
                    serverID, serverNode = sp[0], None
                    requestInfo['request'].append((eval(serverID), serverNode))
                else:
                    serverID, serverNode = sp
                    requestInfo['request'].append((eval(serverID), serverNode.strip()))
            fullInfo[-1].update(requestInfo)

    for i in range(len(fullInfo)):
        fullInfo[i].update(operateInfo[i])

    serverIDMap = {}
    IDInd = 0
    dayServerInfo = {}
    VMIDMap = {}
    VMIDTypeMap = {}
    migTot = 0
    migHappenTime = []
    bombInfo = []
    migOverInfo = []
    for day_i in range(len(fullInfo)):
        day = fullInfo[day_i]
        for server in day['purchase']:
            for i in range(day['purchase'][server]):
                serverIDMap.update({IDInd: server})
                dayServerInfo[IDInd] = []
                IDInd += 1
        cnt = 0
        for mig in day['migration']:
            try:
                cnt += 1
                source = mig[0]
                target = mig[1][0]
                vmid2node[source] = mig[1][1]
                dayServerInfo[VMIDMap[source]].remove(source)
                dayServerInfo[target].append(source)
                VMIDMap[source] = target
                migTot += 1
                if cnt > int(len(VMIDMap) / 200):
                    migOverInfo.append(('migOverflow', day_i + 1, cnt, mig, int(len(VMIDMap) / 200)))
                if not check_bomb(target, dayServerInfo[target], serverDict, VMDict, serverIDMap, VMIDTypeMap,
                                  vmid2node):
                    bombInfo.append(
                        ('Migration', day_i + 1, cnt, mig, target, serverIDMap[target], serverDict[serverIDMap[target]],
                         dayServerInfo[target][-5 if len(
                             dayServerInfo[target]) > 5 else -len(dayServerInfo[target]):]))
            except KeyError:
                raise RuntimeError(('migration error', mig))
        migHappenTime.append(cnt)
        opInd = 0
        for op in day['operate']:
            if op[0] == 'add':
                try:
                    dayServerInfo[day['request'][opInd][0]].append(op[1])
                    VMIDMap[op[1]] = day['request'][opInd][0]
                    vmid2node[op[1]] = day['request'][opInd][1]
                    VMIDTypeMap[op[1]] = op[2].strip()
                    if not check_bomb(day['request'][opInd][0], dayServerInfo[day['request'][opInd][0]], serverDict,
                                      VMDict, serverIDMap, VMIDTypeMap, vmid2node):
                        bombInfo.append(('Add', day_i + 1, opInd + 1, op, day['request'][opInd][0],
                                         serverIDMap[day['request'][opInd][0]],
                                         serverDict[serverIDMap[day['request'][opInd][0]]],
                                         dayServerInfo[day['request'][opInd][0]][-5 if len(
                                             dayServerInfo[day['request'][opInd][0]]) > 5 else -len(
                                             dayServerInfo[day['request'][opInd][0]]):]))
                    opInd += 1
                except KeyError:
                    raise RuntimeError(('server plant error', day['request'][opInd][0], (op[0], op[2], op[1])))
                except IndexError:
                    raise RuntimeError(('req error', (op[0], op[2], op[1])))
            else:
                dayServerInfo[VMIDMap[op[1]]].remove(op[1])
                vmid2node[op[1]] = 'del'
                # try:
                #
                # except KeyError:
                #     raise RuntimeError(('server plant error', VMIDMap[op[1]], op))
        fullInfo[day_i].update({'info': copy.deepcopy(dayServerInfo)})

    """
    经过以上操作后，所有的信息都将被存储到fullInfo中，获取信息可以按照以下方式：
    fullInfo['purchase']：长度为天数的一个列表，每一个元素是当天的购买信息，以键值对存储。
                            比如{'SERVER1':40}表示购买了40台SERVER1型号服务器。
                            
    fullInfo['migration']：长度为天数的一个列表，每一个元素是当天的迁移信息，迁移信息存储在列表中，每一个迁移操作以元组形式存储。
                            比如(12345,10,None)表示将12345号虚拟机迁移到10号服务器上，以双节点部署。
                            又比如(12345,10,A)则表示将12345号虚拟机迁移到10号服务器上的A节点。
                            
    fullInfo['operate']：长度为天数的一个列表，每一个元素是当天的操作信息，包括add和delete，存储在列表中，每一个操作信息以元组形式存储
                            如果元组第一个元素为'add'，则元组长度为3，分别为('add',虚拟机ID,虚拟机型号)
                            如果元组第一个元素为'del'，则元组长度为2，分别为('del',虚拟机ID)
                            
    fullInfo['request']：长度为天数的一个列表，每一个元素是当天的部署情况，以元组形式存储。
                            比如(4,A)表示将对应请求add的虚拟机部署到4号服务器的A节点上。
                            如果元组第二个元素即tuple[1]为None，则表示虚拟机双节点部署到该服务器上。
    
    fullInfo['info']：长度为天数的一个列表，每一个元素是当天结束时服务器以及挂载在其上的虚拟机，以键值对形式存储。
                            比如{5:[123,321,345,654]}表示5号服务器上挂载了4台虚拟机，ID分别为123，321，345，654
    """

    energyCost = []
    emptyRate = []
    hardCost = 0.0
    serverNums = {}
    for serverID, _ in dayServerInfo.items():
        """
        计算硬件成本，从最后一天的服务器信息中统计。
        """
        hardCost += serverDict[serverIDMap[serverID]]['hardCost']
        if serverIDMap[serverID] not in serverNums:
            serverNums[serverIDMap[serverID]] = 1
        else:
            serverNums[serverIDMap[serverID]] += 1
    for day in fullInfo:
        """
        计算每日运行成本。
        计算方式是每天结束时如果一台服务器上有虚拟机在挂载状态，就计算一天的运行费用。
        同时统计闲置率。
        """
        info = day['info']
        c = 0.0
        inUse, empty = 0, 0
        for serverID, _ in info.items():
            if _:
                c += serverDict[serverIDMap[serverID]]['energyCost']
                inUse += 1
            else:
                empty += 1
        energyCost.append(c)
        emptyRate.append((empty / (inUse + empty)) if inUse + empty else 0)

    timeFormat = '%m_%d_%H_%M_%S'
    folderName = os.path.join('./resource', time.strftime(timeFormat, time.localtime(time.time())))
    os.mkdir(folderName)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.plot(range(len(fullInfo)), emptyRate, label='Empty Ratio')
    plt.xlabel('Days')
    plt.ylabel('Ratio')
    plt.title('Empty Ratio (How many servers are not in use)')
    plt.legend()
    plt.savefig(os.path.join(folderName, '1.png'))
    plt.clf()

    plt.plot(range(len(fullInfo)), energyCost, label='Energy Cost')
    plt.xlabel('Days')
    plt.ylabel('Money')
    plt.title('Energy Cost (When a server is in use, it leads to energy cost)')
    plt.legend()
    plt.savefig(os.path.join(folderName, '2.png'))
    plt.clf()

    plt.plot(range(len(fullInfo)), migHappenTime, label='Migration Times')
    plt.xlabel('Days')
    plt.ylabel('Times')
    plt.title('Migration Times')
    plt.legend()
    plt.savefig(os.path.join(folderName, '3.png'))
    plt.clf()

    labels = ['{}\n{}cpu\n{}mem'.format(s, serverDict[s]['cpu'], serverDict[s]['memory']) for s in serverNums.keys()]
    sizes = list(serverNums.values())
    plt.pie(sizes, labels=labels, autopct='%1.2f%%')
    plt.title('Server Types')
    plt.savefig(os.path.join(folderName, '4.png'))
    plt.clf()

    return os.path.split(ioData)[-1], hardCost, sum(energyCost), endTime - beginTime, sum(emptyRate) / len(
        emptyRate), sum(energyCost) / len(energyCost), folderName, migTot, bombInfo, migOverInfo


if __name__ == '__main__':
    if not os.path.exists('./resource'):
        os.mkdir('./resource')
    l = []
    with open('config.json') as file:
        config = json.load(file)
        language = config['language']
        pypyPath = config['pythonInterpreter']
        exe = config['executable']
        sourceCode = config['sourceCode']
        javaPath = config['javaPath']
        javaJARFile = config['buildJARPath']
        ioDataList = config['ioData']  # 从config获取参数
        print('AutoGrader Running with args: {}'.format(
            [language, pypyPath, exe, sourceCode, javaPath, javaJARFile, ioDataList]))

        for d in tqdm(ioDataList, ncols=40):
            """
            根据语言生成测试指令testCmd
            """
            if language == 'c' or language == 'c++':
                testCmd = '\"{}\"<\"{}\"'.format(exe, d)
            elif language == 'python':
                if pypyPath:
                    testCmd = '\"{}\" \"{}\"<\"{}\"'.format(pypyPath, sourceCode, d)
                else:
                    testCmd = 'python \"{}\"<\"{}\"'.format(sourceCode, d)
            elif language == 'java':
                filePath, JARPath = os.path.split(javaJARFile)
                if javaPath:
                    testCmd = '\"{}\" -Djava.library.path=\"{}\" -classpath \"{}\" \"com.huawei.java.main.Main\"<\"{}\"'.format(
                        javaPath, filePath, javaJARFile, d)
                else:
                    testCmd = 'java -Djava.library.path=\"{}\" -classpath \"{}\" \"com.huawei.java.main.Main\"<\"{}\"'.format(
                        filePath, javaJARFile, d)
            else:
                raise ValueError('unsupport language')
            try:
                _ = grader(testCmd, d)
                l.append(_)
            except RuntimeError as e:
                if e.args[0][0] == 'server plant error':
                    print('服务器或虚拟机信息错误,服务器 ID 不存在')
                    print('发生错误的服务器ID为{}，你输出的操作为{}'.format(e.args[0][1], e.args[0][2]))

                elif e.args[0][0] == 'migration error':
                    print('虚拟机迁移错误,服务器 ID 不存在')
                    print('你输出的操作为{}'.format(e.args[0][1]))

                elif e.args[0][0] == 'req error':
                    print('请求错误')
                    print('找不到和{}对应的服务器部署操作'.format(e.args[0][1]))
                print('该问题导致分析器无法继续运行，报告中不会包含本次分析')
    res = gen(l)

    sys = platform.system()
    if sys == 'Windows' or sys == 'windows':
        os.popen('start chrome.exe {}'.format(os.path.join(os.path.dirname(os.path.abspath(__file__)), res)))
    elif sys == 'Linux' or sys == 'linux':
        os.popen('google-chrome {}'.format(os.path.join(os.path.dirname(os.path.abspath(__file__)), res)))
        print('你正在使用Linux系统，可能无法打开网页或报错，请尝试用默认浏览器打开目录下最新生成的html或者将html和resource拷贝到Windows下查看\n')
    elif sys == 'Darwin' or sys == 'darwin':
        os.popen('open -a Safari {}'.format(os.path.join(os.path.dirname(os.path.abspath(__file__)), res)))
        print('你正在使用Mac系统，可能无法打开网页或报错，请尝试用默认浏览器打开目录下最新生成的html或者将html和resource拷贝到Windows下查看\n')
