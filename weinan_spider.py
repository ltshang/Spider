import requests
import json
from fake_useragent import UserAgent
import xlwt
import random
import pandas as pd
import xlrd
from pandas import DataFrame

wb = xlwt.Workbook()
ws = wb.add_sheet('预售项目信息', cell_overwrite_ok=True)
ws.write(0, 0, '开发商')
ws.write(0, 1, '项目名称')
ws.write(0, 2, '发证时间')
ws.write(0, 3, '项目位置')
ws.write(0, 4, '项目类型')
ws.write(0, 5, '预售证号')
#ws.write(0, 6, '土地使用权证')
ws.write(0, 6, '土地权证类型')
ws.write(0, 7, '起始日期')
ws.write(0, 8, '终止日期')
#ws.write(0, 10, '施工许可证')
#ws.write(0, 11, '规划许可证')
ws.write(0, 9, '预售面积(平方米)')
j = 1
# 页
for e in range(1, 2):
    url = 'http://www.wnfdc.com/estateTradeR01/portals/query!listSalePermitProject'
    para = {'page': e, 'limit': 10}
    response = requests.post(url, para)
    jsonData = json.loads(response.text)
    num = jsonData.get('total')
    data = jsonData.get('data')

    for i in range(0, 10):
        if len(data):
            oneData = data[i]
            id = oneData[0]
            xukezheng = oneData[1]
            date = oneData[2]
            name = oneData[3]
            company = oneData[4]
            address = oneData[5]
            url = 'http://www.wnfdc.com/estateTradeR01/portals/query!queryProjPermitSale'
            para = {'id': id}
            headers = {'User-Agent': str(UserAgent().random)}
            response = requests.post(url, para, headers=headers)
            text = response.text
            # 字符串转字典
            zidian = json.loads(text)["data"]
            if len(zidian):
                zidian = zidian[0]
                # 开发商
                kaifashang = zidian[0]
                # 项目名称
                xiangmumingcheng = zidian[1]
                # 发证时间
                fazhengshijian = zidian[3]
                # 项目位置
                xiangmuweizhi = zidian[4]
                # 项目类型
                xiangmuleixing = zidian[5]
                # 预售证号
                yushouzhenghao = zidian[7]
                # 土地使用权证
                tudishiyongquanzheng = zidian[8]
                # 土地权证类型
                tudiquanzhengleixing = zidian[9]
                # 起始日期
                qishiriqi = zidian[10]
                # 终止日期
                zhongzhiriqi = zidian[11]
                # 施工许可证
                shigongxukezheng = zidian[12]
                # 规划许可证
                guihuaxukezheng = zidian[13]
                # 预售面积
                yushoumianji = zidian[14]
                # 将数据写入excel
                ws.write(j, 0, kaifashang)
                ws.write(j, 1, xiangmumingcheng)
                ws.write(j, 2, fazhengshijian)
                ws.write(j, 3, xiangmuweizhi)
                ws.write(j, 4, xiangmuleixing)
                ws.write(j, 5, yushouzhenghao)
                #ws.write(j, 6, tudishiyongquanzheng)
                ws.write(j, 6, tudiquanzhengleixing)
                ws.write(j, 7, qishiriqi)
                ws.write(j, 8, zhongzhiriqi)
                #ws.write(j, 10, shigongxukezheng)
                #ws.write(j, 11, guihuaxukezheng)
                ws.write(j, 9, yushoumianji)
                j += 1
            # 楼盘表
            xiangmumingcheng2 = xiangmumingcheng.replace('·', '')
            xiangmumingcheng2 = xiangmumingcheng2.replace('（', '')
            xiangmumingcheng2 = xiangmumingcheng2.replace('）', '')
            ws1 = wb.add_sheet(xiangmumingcheng2 + '楼盘表' + str(i) + str(random.randint(0, 9)), cell_overwrite_ok=True)
            ws1.write(0, 0, '项目名称')
            ws1.write(0, 1, '项目位置')
            ws1.write(0, 2, '房间号')
            ws1.write(0, 3, '建筑面积')
            ws1.write(0, 4, '规划用途')
            ws1.write(0, 5, '可售状态')
            url = 'http://www.wnfdc.com/estateTradeR01/portals/query!listSalePermitBuild'
            para = {"jsonStr": "{\"cert_id\":\"" + str(id) + "\"}", "page": "1", "limit": "10"}
            headers = {'User-Agent': str(UserAgent().random)}
            response = requests.post(url, para, headers=headers)
            text = response.text
            zidian1 = json.loads(text)["data"]
            if len(zidian1):
                zidian1 = zidian1[0]
                # 楼栋坐落
                location = zidian[4]
                paraId = zidian1[0]
                url = 'http://www.wnfdc.com/estateTradeR01/portals/release!queryBldRoomForTable'
                para = {"jsonStr": "{\"buildId\":\"" + str(paraId) + "\"}"}
                headers = {'User-Agent': str(UserAgent().random)}
                response = requests.post(url, para, headers=headers)
                text = response.text
                zidian2 = json.loads(text)["data"]
                if len(zidian2):

                    louData = {}
                    length = len(zidian2)
                    for r in range(0, length):
                        # 楼层
                        louceng = zidian2[r][0]
                        # print(zidian2[r])
                        # if louceng in louData:
                        #     pass
                        # else:
                        #     louData[louceng]=[]
                        # [22, '-1-2201', '', '1-2201', '住宅', '三室二厅', 117.5, '期房', '无', '可售', 2037989, '2001202038072', '', '', 1, 22]
                        roomNo = zidian2[r][3]
                        # 规划用途
                        yongtu = zidian2[r][4]
                        # 建筑面积
                        jianzhumianji = zidian2[r][6]
                        zhuangtai = zidian2[r][9]
                        ws1.write(r + 1, 0, xiangmumingcheng2)
                        ws1.write(r + 1, 1, xiangmuweizhi)
                        ws1.write(r + 1, 2, roomNo)
                        ws1.write(r + 1, 3, jianzhumianji)
                        ws1.write(r + 1, 4, yongtu)
                        ws1.write(r + 1, 5, zhuangtai)

wb.save('./渭南房地产数据.xls')


file = '渭南房地产数据.xls'
# 处理数据，合并多个sheet，同时去除气化率为空的row
wb = xlrd.open_workbook(file)
# 获取全部的工作簿
sheets = wb.sheets()
df = DataFrame()
# 从第10个sheet开始合并
for i in range(1, len(sheets)):
    #header=1，那么数据会从第二行开始读取
    temp_df = pd.read_excel(file, sheet_name=i,index=False)
    # how='all'：只要存在数据为空的行都删除，还有其他的方法
    dropna_df = temp_df.dropna(how='all')
    df = df.append(dropna_df)
df.to_excel('渭南项目明细.xlsx',index = False)
df1 = pd.read_excel('渭南房地产数据.xls')
df1.to_excel('渭南项目信息.xlsx',index = False)