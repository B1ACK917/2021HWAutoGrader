import json
import os
from tqdm import tqdm
import time
import copy
import matplotlib.pyplot as plt
from genHTML import gen


def check_bomb(server, VMList, serverDict, VMDict, serverIDMap, VMIDMap):
    serverCPU, serverMEM = serverDict[serverIDMap[server]]['cpu'], serverDict[serverIDMap[server]]['memory']
    for VM in VMList:
        serverCPU -= VMDict[VMIDMap[VM]]['cpu']
        serverMEM -= VMDict[VMIDMap[VM]]['memory']
        if serverCPU < 0 or serverMEM < 0:
            return False
    return True


def grader(testCmd, ioData):
    serverDict = {}
    VMDict = {}
    with open(ioData) as file:
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
        operateInfo = []
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
    endTime = time.perf_counter()
    result = result.read().split('\n')[:-1]
    fullInfo = []
    for i in range(len(result)):
        if 'purchase' in result[i]:
            singleDayInfo = {'purchase': {}}
            _, serverBought = result[i][1:-1].split(',')
            serverBought = eval(serverBought.strip())
            for j in range(i + 1, i + serverBought + 1):
                serverName, serverNum = result[j][1:-1].split(',')
                singleDayInfo['purchase'].update({serverName: eval(serverNum)})
            fullInfo.append(singleDayInfo)
        elif 'migration' in result[i]:
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
            for j in range(i + migrationNum + 1, len(result)):
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
    for day_i in range(len(fullInfo)):
        day = fullInfo[day_i]
        for server in day['purchase']:
            for i in range(day['purchase'][server]):
                serverIDMap.update({IDInd: server})
                dayServerInfo[IDInd] = []
                IDInd += 1
        cnt = 0
        for mig in day['migration']:
            cnt += 1
            source = mig[0]
            target = mig[1][0]
            dayServerInfo[VMIDMap[source]].remove(source)
            dayServerInfo[target].append(source)
            VMIDMap[source] = target
            migTot += 1
            if not check_bomb(target, dayServerInfo[target], serverDict, VMDict, serverIDMap, VMIDTypeMap):
                bombInfo.append(('Migration', day_i, cnt - 1))
        migHappenTime.append(cnt)
        opInd = 0
        for op in day['operate']:
            if op[0] == 'add':
                dayServerInfo[day['request'][opInd][0]].append(op[1])
                VMIDMap[op[1]] = day['request'][opInd][0]
                VMIDTypeMap[op[1]] = op[2].strip()
                if not check_bomb(day['request'][opInd][0], dayServerInfo[day['request'][opInd][0]], serverDict, VMDict,
                                  serverIDMap, VMIDTypeMap):
                    bombInfo.append(('Add', day_i, opInd))
                opInd += 1
            else:
                try:
                    dayServerInfo[VMIDMap[op[1]]].remove(op[1])
                except KeyError:
                    raise RuntimeError('Trying to del an unexist server')
        fullInfo[day_i].update({'info': copy.deepcopy(dayServerInfo)})

    energyCost = []
    emptyRate = []
    hardCost = 0.0
    serverNums = {}
    for serverID, _ in dayServerInfo.items():
        hardCost += serverDict[serverIDMap[serverID]]['hardCost']
        if serverIDMap[serverID] not in serverNums:
            serverNums[serverIDMap[serverID]] = 1
        else:
            serverNums[serverIDMap[serverID]] += 1
    for day in fullInfo:
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
        emptyRate.append(empty / (inUse + empty))

    timeFormat = '%m_%d_%H_%M_%S'
    folderName = os.path.join('./resource', time.strftime(timeFormat, time.localtime(time.time())))
    os.mkdir(folderName)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.plot(range(len(fullInfo)), emptyRate, label='Empty Ratio')
    plt.xlabel('Days')
    plt.ylabel('Ratio')
    plt.title('闲置率')
    plt.legend()
    plt.savefig(os.path.join(folderName, '1.png'))
    plt.clf()

    plt.plot(range(len(fullInfo)), energyCost, label='Energy Cost')
    plt.xlabel('Days')
    plt.ylabel('Money')
    plt.title('运行成本')
    plt.legend()
    plt.savefig(os.path.join(folderName, '2.png'))
    plt.clf()

    plt.plot(range(len(fullInfo)), migHappenTime, label='Migration Times')
    plt.xlabel('Days')
    plt.ylabel('Times')
    plt.title('迁移次数')
    plt.legend()
    plt.savefig(os.path.join(folderName, '3.png'))
    plt.clf()

    labels = ['{}\n{}cpu\n{}mem'.format(s, serverDict[s]['cpu'], serverDict[s]['memory']) for s in serverNums.keys()]
    sizes = list(serverNums.values())
    plt.pie(sizes, labels=labels, autopct='%1.2f%%')
    plt.title('服务器占比')
    plt.savefig(os.path.join(folderName, '4.png'))
    plt.clf()

    return os.path.split(ioData)[-1], hardCost, sum(energyCost), endTime - beginTime, sum(emptyRate) / len(
        emptyRate), sum(energyCost) / len(energyCost), folderName, migTot, bombInfo


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
        ioDataList = config['ioData']
        print('AutoGrader Running with args: {}'.format([language, pypyPath, exe, sourceCode, ioDataList]))

        for d in tqdm(ioDataList, ncols=40):
            if language == 'c' or language == 'c++':
                testCmd = '\"{}\"<\"{}\"'.format(exe, d)
            elif language == 'python':
                if pypyPath:
                    testCmd = '\"{}\" \"{}\"<\"{}\"'.format(pypyPath, sourceCode, d)
                else:
                    testCmd = 'python \"{}\"<\"{}\"'.format(pypyPath, sourceCode, d)
            else:
                raise ValueError('unsupport language')
            _ = grader(testCmd, d)
            l.append(_)
    res = gen(l)

    os.popen('start chrome.exe {}'.format(os.path.join(os.path.dirname(os.path.abspath(__file__)), res)))
