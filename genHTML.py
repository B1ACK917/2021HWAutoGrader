import os
import time

contain = """
    <li>
          <h2>******  <img src="./resource/icon-@@@@@.png" width="40"></h2>
          <div>
            <table align="center">
              <tr>
                <td><img src="******" border="0" /></td>
                <td><img src="******" border="0" /></td>
              </tr>
              <tr>
                <td><img src="******" border="0" /></td>
                <td><img src="******" border="0" /></td>
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
                <td>******</td>
              </tr>
              <tr>
                <td>运行时间</td>
                <td>******</td>
              </tr>
              <tr>
                <td>硬件成本</td>
                <td>******</td>
              </tr>
              <tr>
                <td>能源成本</td>
                <td>******</td>
              <tr>
                <td>平均闲置率</td>
                <td>******</td>
              </tr>
              <tr>
                <td>平均每日能源成本</td>
                <td>******</td>
              </tr>
              <tr>
                <td>总迁移次数</td>
                <td>******</td>
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
              </tr>
              BOMBINNER
            </table>
          </div>
"""

bombStyle = """
              <tr>
                <td>*****</td>
                <td>@@@@@</td>
              </tr>
"""


def gen(ls):
    timeFormat = '%m_%d_%H_%M_%S'
    htmlName = time.strftime(timeFormat, time.localtime(time.time())) + '.html'
    with open(htmlName, 'w', encoding='utf-8') as out:
        with open('meta', encoding='utf-8') as file:
            line = file.readline()
            while line:
                if '&&&&&&&&' not in line:
                    out.write(line)

                else:
                    for (ioName, hardCost, energyCost, timeCost, emptyRate, energyAVG, folder, mig, bombInfo) in ls:
                        cs = contain.split('\n')
                        i = -1
                        while i < len(cs):
                            i += 1
                            if '******' not in cs[i]:
                                out.write(cs[i] + '\n')
                            else:
                                if not bombInfo:
                                    out.write(cs[i].replace('******', ioName).replace('@@@@@', 'right') + '\n')
                                else:
                                    out.write(cs[i].replace('******', ioName).replace('@@@@@', 'warning') + '\n')
                                break
                        while i < len(cs):
                            i += 1
                            if '******' not in cs[i]:
                                out.write(cs[i] + '\n')
                            else:
                                out.write(cs[i].replace('******', os.path.join(folder, '1.png')) + '\n')
                                break
                        while i < len(cs):
                            i += 1
                            if '******' not in cs[i]:
                                out.write(cs[i] + '\n')
                            else:
                                out.write(cs[i].replace('******', os.path.join(folder, '2.png')) + '\n')
                                break
                        while i < len(cs):
                            i += 1
                            if '******' not in cs[i]:
                                out.write(cs[i] + '\n')
                            else:
                                out.write(cs[i].replace('******', os.path.join(folder, '3.png')) + '\n')
                                break
                        while i < len(cs):
                            i += 1
                            if '******' not in cs[i]:
                                out.write(cs[i] + '\n')
                            else:
                                out.write(cs[i].replace('******', os.path.join(folder, '4.png')) + '\n')
                                break
                        while i < len(cs):
                            i += 1
                            if '******' not in cs[i]:
                                out.write(cs[i] + '\n')
                            else:
                                out.write(cs[i].replace('******', str(hardCost + energyCost)) + '\n')
                                break
                        while i < len(cs):
                            i += 1
                            if '******' not in cs[i]:
                                out.write(cs[i] + '\n')
                            else:
                                out.write(cs[i].replace('******', str(round(timeCost, 4)) + 's') + '\n')
                                break
                        while i < len(cs):
                            i += 1
                            if '******' not in cs[i]:
                                out.write(cs[i] + '\n')
                            else:
                                out.write(cs[i].replace('******', str(hardCost)) + '\n')
                                break
                        while i < len(cs):
                            i += 1
                            if '******' not in cs[i]:
                                out.write(cs[i] + '\n')
                            else:
                                out.write(cs[i].replace('******', str(energyCost)) + '\n')
                                break
                        while i < len(cs):
                            i += 1
                            if '******' not in cs[i]:
                                out.write(cs[i] + '\n')
                            else:
                                out.write(cs[i].replace('******', str(round(emptyRate, 6) * 100) + ' % ') + '\n')
                                break
                        while i < len(cs):
                            i += 1
                            if '******' not in cs[i]:
                                out.write(cs[i] + '\n')
                            else:
                                out.write(cs[i].replace('******', str(energyAVG) + '\n'))
                                break
                        while i < len(cs):
                            i += 1
                            if '******' not in cs[i]:
                                out.write(cs[i] + '\n')
                            else:
                                out.write(cs[i].replace('******', str(mig) + '\n'))
                                break

                        if bombInfo:
                            while i < len(cs):
                                i += 1
                                if 'BOMBINFO' not in cs[i]:
                                    out.write(cs[i] + '\n')
                                else:
                                    j = -1
                                    bc = bombContain.split('\n')
                                    while j < len(bc) - 1:
                                        j += 1
                                        if 'BOMBINNER' not in bc[j]:
                                            out.write(bc[j] + '\n')
                                        else:
                                            for b in bombInfo:
                                                out.write(bombStyle.replace('*****', '资源分配溢出').replace('@@@@@',
                                                                                                       '发生于第{}天的第{}条{}操作'.format(
                                                                                                           b[1], b[2],
                                                                                                           b[
                                                                                                               0])) + '\n')
                                    break
                        while i < len(cs) - 1:
                            i += 1
                            if 'BOMBINFO' in cs[i]:
                                continue
                            out.write(cs[i] + '\n')
                line = file.readline()
    return htmlName


if __name__ == '__main__':
    print(contain.split('\n'))
