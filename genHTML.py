import os
import time

header = """
        <header>总计成本: CCCOST</header>
"""

mainContain = """
        <li>
          <h2>DOC_NAME  <img src="./resource/icon-ICON_TYPE.png" width="40"></h2>
          <div>
            <table align="center">
              <tr>
                <td><img src="IMG1" border="0" /></td>
                <td><img src="IMG2" border="0" /></td>
              </tr>
              <tr>
                <td><img src="IMG3" border="0" /></td>
                <td><img src="IMG4" border="0" /></td>
              </tr>
            </table>
          </div>
          <div align="center">
            <table border="1">
              <tr>
                <th>结果</th>
                <th>值</th>
              </tr>
              <tr>
                <td>总成本</td>
                <td>TOTAL_COST</td>
              </tr>
              <tr>
                <td>运行时间</td>
                <td>ELAPSED_TIME</td>
              </tr>
              <tr>
                <td>硬件成本</td>
                <td>HARD_COST</td>
              </tr>
              <tr>
                <td>能源成本</td>
                <td>ENERGY_COST</td>
              <tr>
                <td>平均闲置率</td>
                <td>EMPTY_RATIO</td>
              </tr>
              <tr>
                <td>平均每日能源成本</td>
                <td>ENERGY_AVG</td>
              </tr>
              <tr>
                <td>总迁移次数</td>
                <td>MIG_TIMES</td>
              </tr>
            </table>
          </div>
          BOMBINFO
        </li>
"""

bombContain = """
          <div align="center">
            <table border="1">
              <tr>
                <th>错误类型</th>
                <th>错误信息</th>
                <th>错误请求</th>
                <th>错误服务器ID</th>
                <th>挂载虚拟机列表(仅显示最后5个虚拟机)</th>
              </tr>
              BOMBINNER
            </table>
          </div>
"""

bombStyle = """
              <tr>
                <td>BOMB_TYPE</td>
                <td>BOMB_INFO</td>
                <td>BOMB_REQ</td>
                <td>BOMB_SERVER_ID</td>
                <td>BOMB_SERVER_VM</td>
              </tr>
"""


def gen(ls, showHeader=False):
    timeFormat = '%m_%d_%H_%M_%S'
    htmlName = time.strftime(timeFormat, time.localtime(time.time())) + '.html'
    with open(htmlName, 'w', encoding='utf-8') as out:
        with open('meta', encoding='utf-8') as file:
            line = file.readline()
            while line:
                if '&&&&&&&&' not in line:
                    out.write(line)
                else:
                    existHeader = False
                    for (ioName, hardCost, energyCost, timeCost, emptyRate, energyAVG, folder, mig, bombInfo,
                         migOverInfo) in ls:
                        contain = mainContain
                        if showHeader and not existHeader:
                            contain = header.replace('CCCOST', str(sum([k[1] + k[2] for k in ls]))) + contain
                            existHeader = True
                        contain = contain.replace('DOC_NAME', ioName)
                        contain = contain.replace('ICON_TYPE', 'warning' if bombInfo or migOverInfo else 'right')
                        contain = contain.replace('IMG1', os.path.join(folder, '1.png'))
                        contain = contain.replace('IMG2', os.path.join(folder, '2.png'))
                        contain = contain.replace('IMG3', os.path.join(folder, '3.png'))
                        contain = contain.replace('IMG4', os.path.join(folder, '4.png'))
                        contain = contain.replace('TOTAL_COST', str(hardCost + energyCost))
                        contain = contain.replace('ELAPSED_TIME', str(round(timeCost, 4)) + 's')
                        contain = contain.replace('HARD_COST', str(hardCost))
                        contain = contain.replace('ENERGY_COST', str(energyCost))
                        contain = contain.replace('EMPTY_RATIO', str(round(emptyRate * 100, 6)) + ' % ')
                        contain = contain.replace('ENERGY_AVG', str(energyAVG))
                        contain = contain.replace('MIG_TIMES', str(mig))
                        if bombInfo or migOverInfo:
                            totalBombInfo = """"""
                            if migOverInfo:
                                for b in migOverInfo[:10 if len(migOverInfo) > 10 else len(migOverInfo)]:
                                    bs = bombStyle
                                    bs = bs.replace('BOMB_TYPE', '虚拟机迁移超过上限')
                                    bs = bs.replace('BOMB_INFO',
                                                    '发生于第{}天的第{}条迁移操作，允许迁移次数最大为{}'.format(b[1], b[2], b[4]))
                                    if b[3][1][1]:
                                        bs = bs.replace('BOMB_REQ',
                                                        '({},{},{})'.format(b[3][0], b[3][1][0], b[3][1][1]))
                                    else:
                                        bs = bs.replace('BOMB_REQ', '({},{})'.format(b[3][0], b[3][1][0]))
                                    bs = bs.replace('BOMB_SERVER_ID', '')
                                    bs = bs.replace('BOMB_SERVER_VM', '')
                                    totalBombInfo += bs
                            if bombInfo:
                                for b in bombInfo[:50 if len(bombInfo) > 50 else len(bombInfo)]:
                                    bs = bombStyle
                                    bs = bs.replace('BOMB_TYPE', '资源分配溢出')
                                    bs = bs.replace('BOMB_INFO', '发生于第{}天的第{}条{}操作'.format(b[1], b[2], b[0]))
                                    if b[3][0] == 'add':
                                        bs = bs.replace('BOMB_REQ', '({},{},{})'.format(b[3][0], b[3][2], b[3][1]))
                                    else:
                                        if b[3][1][1]:
                                            bs = bs.replace('BOMB_REQ',
                                                            '({},{},{})'.format(b[3][0], b[3][1][0], b[3][1][1]))
                                        else:
                                            bs = bs.replace('BOMB_REQ', '({},{})'.format(b[3][0], b[3][1][0]))
                                    bs = bs.replace('BOMB_SERVER_ID', '{} ({},{})'.format(b[4], b[5], b[6]))
                                    bs = bs.replace('BOMB_SERVER_VM', '{}'.format(b[7]))
                                    totalBombInfo += bs
                            bc = bombContain.replace('BOMBINNER', totalBombInfo)
                            contain = contain.replace('BOMBINFO', bc)
                        else:
                            contain = contain.replace('BOMBINFO', '')
                        for l in contain.split('\n'):
                            out.write(l + '\n')
                line = file.readline()
    return htmlName


if __name__ == '__main__':
    print(mainContain.split('\n'))
