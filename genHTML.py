import os

contain = """
    <li>
          <h2>******</h2>
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
        </li>
"""


def gen(ls):
    with open('index.html', 'w', encoding='utf-8') as out:
        with open('meta', encoding='utf-8') as file:
            line = file.readline()
            while line:
                if '&&&&&&&&' not in line:
                    out.write(line)

                else:
                    for (ioName, hardCost, energyCost, timeCost, emptyRate, energyAVG, folder, mig) in ls:
                        cs = contain.split('\n')
                        i = -1
                        while i < len(cs):
                            i += 1
                            if '******' not in cs[i]:
                                out.write(cs[i] + '\n')
                            else:
                                out.write(cs[i].replace('******', ioName) + '\n')
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
                        while i < len(cs) - 1:
                            i += 1
                            out.write(cs[i] + '\n')
                line = file.readline()


if __name__ == '__main__':
    print(contain.split('\n'))
